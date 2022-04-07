cmake_minimum_required(VERSION 3.3)

project(test-app VERSION 0.1.0 LANGUAGES CXX)

find_package(foolib REQUIRED)

add_executable(test-app main.cpp)
target_include_directories(test-app PRIVATE ${FOOLIB_INCLUDE_DIRS})
target_link_libraries(test-app ${FOOLIB_LIBRARIES})