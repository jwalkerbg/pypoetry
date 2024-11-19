import os
import shutil
from pathlib import Path

# Uncomment if library can still function if extensions fail to compile (e.g. slower, python fallback).
# Don't allow failure if cibuildwheel is running.
# allowed_to_fail = os.environ.get("CIBUILDWHEEL", "0") != "1"
allowed_to_fail = False

def build_cython_extensions():
    # when using setuptools, you should import setuptools before Cython,
    # otherwise, both might disagree about the class to use.
    from setuptools import Extension  # noqa: I001
    from setuptools.dist import Distribution  # noqa: I001
    import Cython.Compiler.Options  # pyright: ignore [reportMissingImports]
    from Cython.Build import build_ext, cythonize  # pyright: ignore [reportMissingImports]

    Cython.Compiler.Options.annotate = True

    if os.name == "nt":  # Windows
        extra_compile_args = [
            "/O2",
        ]
    else:  # UNIX-based systems
        extra_compile_args = [
            "-O3",
            "-Werror",
            "-Wno-unreachable-code-fallthrough",
            "-Wno-deprecated-declarations",
            "-Wno-parentheses-equality",
            "-Wno-unreachable-code",  # TODO: This should no longer be necessary with Cython>=3.0.3
        ]
    extra_compile_args.append("-UNDEBUG")  # Cython disables asserts by default.
    # Relative to project root director
    include_dirs = [
        "pypoetry/",
        "pypoetry/cyth"
        "pypoetry/c_src",
    ]

    c_files = [str(x) for x in Path("pypoetry/c_src").rglob("*.c")]
    extensions = [
        Extension(
            # Your .pyx file will be available to cpython at this location.
            "hello_world",
            [
                # ".c" and ".pyx" source file paths
                "src/pypoetry/cyth/hello_world.pyx",
                *c_files,
            ],
            include_dirs=include_dirs,
            extra_compile_args=extra_compile_args,
            language="c",
        ),
    ]

    print(f"extensions[0] = {extensions[0]}")

    include_dirs = set()
    for extension in extensions:
        include_dirs.update(extension.include_dirs)
    include_dirs = list(include_dirs)

    ext_modules = cythonize(extensions, include_path=include_dirs, language_level=3, annotate=True)
    dist = Distribution({"ext_modules": ext_modules})
    cmd = build_ext(dist)
    cmd.ensure_finalized()
    cmd.run()

    for output in cmd.get_outputs():
        output = Path(output)
        relative_extension = output.relative_to(cmd.build_lib)
        shutil.copyfile(output, relative_extension)

try:
    build_cython_extensions()
except Exception:
    if not allowed_to_fail:
        raise

