import os
from shutil import move
from shutil import rmtree
import time

def create_gui():
	os.system("pyinstaller -wF octoflu.py")

	move(os.path.join(os.getcwd(),"dist\\octoflu.exe"), "octoflu.exe")
	time.sleep(2)
	rmtree("build")
	rmtree("dist")

if __name__ == '__main__':
	create_gui()