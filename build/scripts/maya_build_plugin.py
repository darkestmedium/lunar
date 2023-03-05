# Built-in imports
import platform
import subprocess
import time
import logging

# Third-party imports

# Custom imports
import maya_quit




class LMBuildPlugin():
	"""Class for automating the development of a maya plugin.
	"""
	def __init__(self,
		projectName="mlunar",
		mayaVersion=2023, 
		buildType="Release",
		buildTarget="all",
		clean=True,
		) -> None:
		self.getPlatformData()

		self.projectName=projectName
		self.mayaVersion=mayaVersion
		self.buildType=buildType
		self.buildTarget=buildTarget

		self.mayaName = "Maya"

		# Paths
		self.pathProject = __file__[:-35]
		self.pathBuild = f"{self.pathProject}/build"
		self.pathBuildScripts = f"{self.pathBuild}/scripts"
		self.pathBuildMaya = f"{self.pathBuild}/maya"
		self.pathBuildMayaOs = f"{self.pathBuildMaya}/{self.nameOs}"
		self.pathBuildMayaOsVersion = f"{self.pathBuildMayaOs}/{self.mayaVersion}"
		self.pathBuildMayaOsVersionType = f"{self.pathBuildMayaOsVersion}/{self.buildType}"
		self.pathPluginTarget = f"{self.pathProject}/lunar/maya/resources/plug-ins/{self.nameOs}/{self.mayaVersion}"

		# Plugin Info
		self.pluginName = f"{self.projectName}{self.pluginExt}"
		self.pathBuiltPlugin = f"{self.pathBuildMayaOsVersionType}/src/maya/{self.pluginName}"

		# Run commands
		if clean:
			print("Perform clean build, removing existing files...")
			output = subprocess.run(["rm", "-rf", self.pathBuildMaya], capture_output=True, text=True)
			print("Removed previous build files!")
		output = subprocess.run(["mkdir", "-p", self.pathBuildMayaOsVersionType], capture_output=True, text=True)
		output = subprocess.run(["cd", self.pathBuildMayaOsVersionType], capture_output=True, text=True)

		maya_quit.quitMayaRemotley()

		# Cmake
		print("Starting cmake configuration...")
		output = subprocess.run(
			[
				"cmake",
				f"-G {self.generator}",
				f"-DMAYA_VERSION={self.mayaVersion}",
				f"-DCMAKE_BUILD_TYPE:STRING={self.buildType}",
				self.pathProject,
			],
			cwd=self.pathBuildMayaOsVersionType, capture_output=True, text=True, check=True
		)

		print("Starting cmake build...")
		output = subprocess.run(
			[
				"cmake",
				"--build", ".",
				"--config", self.buildType, 
			],
			cwd=self.pathBuildMayaOsVersionType, capture_output=True, text=True, check=True
		)

		output = subprocess.run(["cp", "-f", self.pathBuiltPlugin, self.pathPluginTarget], capture_output=True, text=True)


		isAppRunning = False
		while not isAppRunning:
			# time.sleep(3)
			isAppRunning = subprocess.run(['pgrep', self.mayaName], capture_output=True)
			if isAppRunning.returncode == 0:
				print(f"{self.mayaName} is running")
				isAppRunning = True
			else:
				print(f"Launching {self.mayaName}")
				subprocess.run(['open', '-a', 'maya'])


	@classmethod
	def getPlatformData(cls):
		namePlatform = platform.system()
		if namePlatform == "Darwin": 
			cls.nameOs = "macos"
			cls.generator = "Unix Makefiles"
			cls.pluginExt = ".bundle"
		if namePlatform == "Linux": 
			cls.nameOs = "linux"
			cls.generator = "Unix Makefiles"
			cls.pluginExt = ".so"
		if namePlatform == "Windows": 
			cls.nameOs = "windows"
			cls.generator = "Visual Studio 17 2022"
			cls.pluginExt = ".mll"




if __name__ == "__main__":

	build = LMBuildPlugin(
		# projectName="mlunar",
		# mayaVersion=2023, 
		# buildType="Debug",
		# buildTarget="all",
		# clean=True,
	)
