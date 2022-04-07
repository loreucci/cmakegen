import os
import argparse
from jinja2 import Environment, PackageLoader


def render_template(env, template_file, out_file, config):
    """
    Helper function to render a template

    :param env: jinja2 template environment
    :param template_file: name of the template file
    :param out_file: output file path
    :param config: variables
    """
    template = env.get_template(template_file)
    with open(out_file, "w") as file:
        file.write(template.render(**config))


def create_project(project,
                   library=None,
                   populate=False,
                   namespace=None,
                   project_version="0.0.1",
                   cppstd=None,
                   defaultrelease=True,
                   defaultshared=True,
                   tests=False):
    """
    Create project directory structure and library files

    If populate is False, the library will not be able to be compiled straight away as there will be no source files.

    :param project: name of the project (main folder)
    :param library: name of the library
    :param populate: if true, populate the library with sample files
    :param namespace: add C++ namespace to sample files
    :param project_version: project version string
    :param cppstd: set C++ standard in CMake
    :param defaultrelease: if true add code to CMAke to default to a Release build
    :param defaultshared: if true add code to CMAke to default to a shared library
    :param tests: if true create tests folder and enable googletests (a sample test will be added with populate=True)
    """

    # default library name to project name
    if library is None:
        library = project

    # filename equals to library
    filename = library

    # create dictionary for jinja
    config = {
        "project": project,
        "library": library,
        "populate": populate,
        "filename": filename,
        "namespace": namespace,
        "version": project_version,
        "cppstd": cppstd,
        "defaultrelease": defaultrelease,
        "defaultshared": defaultshared,
        "tests": tests
    }

    # load templates environment (should use PackageLoader instead of this hack)
    env = Environment(
        loader=PackageLoader("cmakegen"),
        trim_blocks=True,
        lstrip_blocks=True
    )

    # create directory structure
    os.mkdir(project)
    os.makedirs(f"{project}/include/{library}")

    # source files
    os.makedirs(f"{project}/src")
    render_template(env, "CMakeLists.src.txt", f"{project}/src/CMakeLists.txt", config)
    if populate:
        render_template(env, "source.cpp", f"{project}/src/{filename}.cpp", config)
        render_template(env, "header.h", f"{project}/include/{library}/{filename}.h", config)

    # main CMake file
    render_template(env, "CMakeLists.main.txt", f"{project}/CMakeLists.txt", config)

    # cmake dir
    os.makedirs(f"{project}/cmake")
    render_template(env, "Config.cmake.in", f"{project}/cmake/{library}Config.cmake.in", config)
    render_template(env, "ConfigVersion.cmake.in", f"{project}/cmake/{library}ConfigVersion.cmake.in", config)

    # tests
    if tests:
        os.makedirs(f"{project}/tests")
        render_template(env, "CMakeLists.tests.txt", f"{project}/tests/CMakeLists.txt", config)
        if populate:
            render_template(env, "test.cpp", f"{project}/tests/{filename}.test.cpp", config)


def run_cmakegen():
    """
    Main entry point for cmakegen
    """
    # setup args
    parser = argparse.ArgumentParser(prog="cmakegen", description="Generate a cmake-based C++ project")
    parser.add_argument("project", type=str, help="name of the project (folder)")
    parser.add_argument("-l", "--library", type=str, default=None, help="name of the library")
    parser.add_argument("-p", "--populate", action="store_true", help="add example file to library")
    parser.add_argument("--namespace", type=str, default=None,
                        help="namespace of the library (only if library has been populated with -p)")
    parser.add_argument("--project_version", type=str, default="0.0.1",
                        help="version of the project")
    parser.add_argument("--cppstd", type=str, default=None,
                        help="C++ standard used by the project")
    parser.add_argument("--no_default_release", action="store_false",
                        help="avoid setting default configuration to Release")
    parser.add_argument("--no_default_shared", action="store_false",
                        help="avoid setting option and default configuration to shared library")
    parser.add_argument("-t", "--tests", action="store_true",
                        help="add tests with googletest (only if library has been populated with -p")

    args = parser.parse_args()

    create_project(
        project=args.project,
        library=args.library,
        populate=args.populate,
        namespace=args.namespace,
        project_version=args.project_version,
        cppstd=args.cppstd,
        defaultrelease=args.no_default_release,
        defaultshared=args.no_default_shared,
        tests=args.tests
    )
