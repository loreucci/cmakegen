import os
from jinja2 import Environment, FileSystemLoader


def render_template(env, template_file, out_file, config):
    template = env.get_template(template_file)
    with open(out_file, "w") as file:
        file.write(template.render(**config))


def main():

    # load templates environment (should use PackageLoader instead of this hack)
    env = Environment(
        loader=FileSystemLoader(f"{os.path.dirname(__file__)}/templates"),
        trim_blocks=True,
        lstrip_blocks=True
    )

    # to be read from command line
    config = {
        "project": "foo",
        "library": "foolib",  # these two should be equal to project by default
        "filename": "foo",  # from populate
        "namespace": "bar",
        "function": "foof",  # default: filename_function
        "version": "0.0.1",
        "cppver": 17,
        "defaultrelease": True,
        "defaultshared": True,
        "tests": True
    }

    # create directory structure
    os.mkdir(config['project'])
    os.chdir(config['project'])
    os.makedirs(f"include/{config['library']}")
    os.mkdir("src")

    # source files
    render_template(env, "source.cpp", f"src/{config['filename']}.cpp", config)
    render_template(env, "header.h", f"include/{config['library']}/{config['filename']}.h", config)
    render_template(env, "CMakeLists.src.txt", "src/CMakeLists.txt", config)

    # main CMake file
    render_template(env, "CMakeLists.main.txt", "CMakeLists.txt", config)

    # cmake dir
    os.mkdir("cmake")
    render_template(env, "Config.cmake.in", f"cmake/{config['library']}Config.cmake.in", config)
    render_template(env, "ConfigVersion.cmake.in", f"cmake/{config['library']}ConfigVersion.cmake.in", config)

    # tests
    os.mkdir("tests")
    render_template(env, "CMakeLists.tests.txt", "tests/CMakeLists.txt", config)
    render_template(env, "test.cpp", f"tests/{config['filename']}.test.cpp", config)


if __name__ == '__main__':
    main()
