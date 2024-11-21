import os
import sys
import shutil
from pathlib import Path
# Check Python version at runtime

if sys.version_info >= (3, 11):
    import tomllib as toml  # Use the built-in tomllib for Python 3.11+
else:
    import tomli as toml    # Use the external tomli for Python 3.7 to 3.10

# Uncomment if library can still function if extensions fail to compile (e.g. slower, python fallback).
# Don't allow failure if cibuildwheel is running.
# allowed_to_fail = os.environ.get("CIBUILDWHEEL", "0") != "1"
allowed_to_fail = False

def read_cython_path():
    # TODO: Add exception handling
    # TODO: Add c_ext path return
    # Open pyproject.toml and read the cython_path setting
    with open("pyproject.toml", "rb") as f:
        pyproject_data = toml.load(f)
    return pyproject_data.get("tool", {}).get("pypoetry", {}).get("config", {}).get("cython_path", "src/pypoetry/cyth")

def build_cython_extensions():
    # when using setuptools, you should import setuptools before Cython,
    # otherwise, both might disagree about the class to use.
    from setuptools import Extension  # noqa: I001
    from setuptools.dist import Distribution  # noqa: I001
    import Cython.Compiler.Options  # pyright: ignore [reportMissingImports]
    from Cython.Build import build_ext, cythonize  # pyright: ignore [reportMissingImports]

    Cython.Compiler.Options.annotate = True

    cython_path = read_cython_path()
    print(f"Using Cython path: {cython_path}")

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
    # Dynamically find all .pyx files in the cyth directory
    pyx_files = list(Path(cython_path).rglob("*.pyx"))
    extensions = [
        Extension(
            pyx_file.stem,  # The module name (e.g., "hello_world" from "hello_world.pyx")
            [str(pyx_file)],
            include_dirs=include_dirs,
            extra_compile_args=extra_compile_args,
            language="c",
        )
        for pyx_file in pyx_files
    ]

    # Log discovered extensions
    print(f"Discovered .pyx files: {pyx_files}")
    print(f"Creating Extensions: {[ext.name for ext in extensions]}")

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
        print(f"Generated file: {output}")
        src_relative_path = Path(cython_path) / output.name
        shutil.copyfile(output, src_relative_path)
        print(f"Copied {output} to {src_relative_path}")

def build(setup_kwargs):
    try:
        build_cython_extensions()
    except Exception:
        if not allowed_to_fail:
            raise
