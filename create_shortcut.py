import os
import winshell
from win32com.client import Dispatch


def create_octoflu_shortcut():
	"""creates a shortcut to use the hotkey functionality"""
	 
	desktop = winshell.desktop()
	path = os.getcwd()
	target = os.getcwd() + "\\octoflu.exe"
	wDir = os.getcwd()
	icon = os.getcwd() + "\\octoflu_icon.ico"
	 
	shell = Dispatch('WScript.Shell')
	shortcut = shell.CreateShortCut("OctoFLU_Gui.lnk")
	shortcut.Targetpath = target
	shortcut.WorkingDirectory = wDir
	shortcut.IconLocation = icon
	shortcut.save()

if __name__ == '__main__':
	create_octoflu_shortcut()