from cmakegen import create_project
import unittest
import tempfile
import os
import subprocess


class TestCmakegen(unittest.TestCase):

    def test_create_and_build(self):
        with tempfile.TemporaryDirectory() as td:

            # create project
            os.chdir(td)
            create_project(
                project="foo",
                library="foolib",
                cppstd="17",
                tests=True,
                populate=True,
                namespace="bar"
            )

            # create install directory
            os.mkdir("usr")

            # build it
            os.mkdir("build-lib")
            os.chdir("build-lib")
            subprocess.check_output(["cmake",
                                     "-DBUILD_TEST=ON",
                                     f"-DCMAKE_INSTALL_PREFIX={td + '/usr'}",
                                     f"{td + '/foo'}"])
            subprocess.check_output(["make"])
            subprocess.check_output(["make", "test"])
            subprocess.check_output(["make", "install"])

            os.chdir("..")

            # build sample app
            os.mkdir("build-app")
            os.chdir("build-app")
            modified_env = os.environ.copy()
            modified_env["CMAKE_PREFIX_PATH"] = td + "/usr"
            subprocess.check_output(["cmake",
                                     f"{os.path.dirname(__file__)}/app"],
                                    env=modified_env)
            subprocess.check_output(["make"], cwd=td + "/build-app")
            output = subprocess.check_output(["./test-app"], cwd=td + "/build-app").decode().strip()
            self.assertEqual(output, "7")
