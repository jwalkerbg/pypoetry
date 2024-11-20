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
        "src/pypoetry/",
        "src/pypoetry/cyth/",
        "src/pypoetry/c_src/",
    ]

    c_files = [str(x) for x in Path("pypoetry/c_src").rglob("*.c")]
    pyx_file = "src/pypoetry/cyth/hello_world.pyx"  # Path to the .pyx file
    extensions = [
        Extension(
            # Your .pyx file will be available to cpython at this location.
            "hello_world",
            [
                # ".c" and ".pyx" source file paths
                pyx_file
            ],
            include_dirs=include_dirs,
            extra_compile_args=extra_compile_args,
            language="c",
        ),
    ]

    print(f"type of extensions[0] = {type(extensions[0])}")
    print(f"attributes = {dir(extensions[0])}")
    print(f"sources = {extensions[0].sources}")

    include_dirs = set()
    for extension in extensions:
        include_dirs.update(extension.include_dirs)
    include_dirs = list(include_dirs)

    print(f"include_dirs = {include_dirs}")

    ext_modules = cythonize(extensions, include_path=include_dirs, language_level=3, annotate=True)
    dist = Distribution({"ext_modules": ext_modules})
    cmd = build_ext(dist)
    cmd.ensure_finalized()
    cmd.run()

    # Dynamically determine the destination directory
    pyx_path = Path(pyx_file)
    target_dir = pyx_path.parent  # Use the parent directory of the .pyx file
    target_dir.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists

    for output in cmd.get_outputs():
        print(f"output = {output}")
        output = Path(output)
        print(f"output = {output}")

        # Copy the .pyd file to the target directory
        target_path = target_dir / output.name
        shutil.copyfile(output, target_path)
        print(f"Moved {output} to {target_path}")

        # print(f"cmd.build_lib = {cmd.build_lib}")
        # relative_extension = output.relative_to(cmd.build_lib)
        # shutil.copyfile(output, relative_extension)
        # print(f"output = {output}, relative_extension = {relative_extension}")

def build(setup_kwargs):
    try:
        build_cython_extensions()
    except Exception:
        if not allowed_to_fail:
            raise

