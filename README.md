# cmakegen

A generator of CMake-based C++ projects, made in Python.

Generates a skeleton of a C++ project using CMake as the build generator.
The generated project is ready to be compiled, installed and included in another CMake-based projects as it will include
all the necessary CMake modules.

## Install

The executable can be installed from sources:

```commandline
git clone https://github.com/loreucci/cmakegen.git
cd cmakegen
pip install .
```

## Usage

The program can be invoked with:

```commandline
cmakegen -p -t foo 
```

This will create a project `foo`, containing a library (also called `foo` and populated with some sample files).
The created project includes also basic unit tests, resulting in the following folder structure:

<pre>
foo
|-- CMakeLists.txt
|-- cmake
│   |-- fooConfig.cmake.in
│   |-- fooConfigVersion.cmake.in
|-- include
│   |-- foo
│       |-- foo.h
|-- src
│   |-- CMakeLists.txt
│   |-- foo.cpp
|-- tests
    |-- CMakeLists.txt
    |-- foo.test.cpp
</pre>

The library can be used with the normal `cmake` workflow:
```commandline
cd foo
mkdir build && cd build
cmake ..
make
make test
make install
```

By default, this will also install the necessary CMake files so that the library can be included in other projects by:

```cmake
find_package(foo REQUIRED)

add_executable(test-app main.cpp)
target_include_directories(test-app PRIVATE ${FOO_INCLUDE_DIRS})
target_link_libraries(test-app ${FOO_LIBRARIES})
```


For other options see

```commandline
cmakegen --help 
```