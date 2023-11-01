import keyboard
import sys

def addEvent(callBack):
	print(callBack)
	print(callBack.scan_code)
def quitProg():
	sys.exit(0)
keyboard.hook(addEvent)
keyboard.add_hotkey('ctrl+z', quitProg)


