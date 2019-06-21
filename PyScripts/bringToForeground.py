from pywinauto.findwindows import find_window
from pywinauto.win32functions import SetForegroundWindow
SetForegroundWindow(find_window(title='BlueStacks'))
