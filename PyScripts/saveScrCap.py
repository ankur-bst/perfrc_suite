from PIL import ImageGrab

def saveCurrent(path):
	img = ImageGrab.grabclipboard()
	img.save(path, 'PNG')
#saveCurrent('C:\\Users\\Administrator\\Desktop\\perf_rc_suite\\PyScripts\\testimg.png')