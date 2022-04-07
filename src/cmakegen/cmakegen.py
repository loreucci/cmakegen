import os
import argparse
from jinja2 import Environment, PackageLoader


def render_template(env, template_file, out_file, config):
    template = env.get_template(template_file)
    with open(out_file, "w") as file:
        file.write(template.render(**config))


def create_project(config):

    # convenience variables
    populate_lib = config["populate"]
    filename = config["filename"]
    library = config["library"]
    project = config["project"]

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
    if populate_lib:
        render_template(env, "source.cpp", f"{project}/src/{filename}.cpp", config)
        render_template(env, "header.h", f"{project}/include/{library}/{filename}.h", config)

    # main CMake file
    render_template(env, "CMakeLists.main.txt", f"{project}/CMakeLists.txt", config)

    # cmake dir
    os.makedirs(f"{project}/cmake")
    render_template(env, "Config.cmake.in", f"{project}/cmake/{library}Config.cmake.in", config)
    render_template(env, "ConfigVersion.cmake.in", f"{project}/cmake/{library}ConfigVersion.cmake.in", config)

    # tests
    if config["tests"]:
        os.makedirs(f"{project}/tests")
        render_template(env, "CMakeLists.tests.txt", f"{project}/tests/CMakeLists.txt", config)
        if populate_lib:
            render_template(env, "test.cpp", f"{project}/tests/{filename}.test.cpp", config)


def run_cmakegen():
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

    # create configuration
    config = {
        "project": args.project,
        "library": args.project if args.library is None else args.library,  # default to project name
        "populate": args.populate,
        "filename": None,  # depends on library
        "namespace": args.namespace,
        "version": args.project_version,
        "cppstd": args.cppstd,
        "defaultrelease": args.no_default_release,
        "defaultshared": args.no_default_shared,
        "tests": args.tests
    }
    if config["populate"]:
        config["filename"] = config["library"]

    create_project(config)