from conans import ConanFile, CMake, tools
import glob
import os
import shutil

class Box2dConan(ConanFile):
    name = "Box2D"
    # Version from Box2D/Common/b2Settings.cpp
    # -
    # package iteration
    # +
    # corresponding Box2D git hash
    # When the next release gets tagged officially we can remove the hash
    # and package iteration
    version = "2.3.2-1+ac9aaf2"
    license = "Zlib"
    url = "https://github.com/erincatto/Box2D"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    generators = "cmake"
    exports = "CMakeLists.txt", "patch/*"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def source(self):
        base_url = "https://github.com/erincatto/Box2D/archive/{}.zip"
        commit = self.version.split("+")[1]
        tools.download(base_url.format(commit), "box2d.zip")
        tools.unzip("box2d.zip")
        os.remove("box2d.zip")
        os.rename('Box2D-{}'.format(commit), self.source_subfolder)
        for f in glob.glob("patch/*.patch"):
            tools.patch(patch_file=f, base_path=self.source_subfolder)

    def build(self):
        shutil.copy("CMakeLists.txt", self.source_subfolder)
        cmake = CMake(self)
        if self.options.fPIC and self.settings.compiler != "Visual Studio":
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = True
        cmake.configure(source_folder=self.source_subfolder, build_folder=self.build_subfolder)
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self.source_subfolder)
        include_dir = os.path.join(self.source_subfolder, "Box2D")
        self.copy("*.h", dst="include/Box2D", src=include_dir)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["box2d"]
