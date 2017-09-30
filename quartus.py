import pyautogui
import time

from window_manager import window_manager

def translate_to_center_cord(x, y, w, h):
	# For some reason the y-cord needs to be compensated
	#return (x + w/2 , y + h/2 + (image_h - screen_h))
	return (x + w/2 , y + h/2)
	#return (x, y)

def start_compile():
	result = pyautogui.locate('pic/compile_button.png', image)	
	if result is None:
		print("Cannot start compiling")
		exit()

	print(result)
	(x, y, w, h) = result
	(center_x, center_y) = translate_to_center_cord(x, y, w, h)
	pyautogui.click(center_x, center_y)

def is_compile_success():
	result = pyautogui.locate('pic/compile_complete.png', image)
	if result is not None:
		print(result)
		return True
	return False

def is_compile_failed():
	result = pyautogui.locate('pic/compile_error.png', image)
	if result is not None:
		print(result)
		return True
	return False

WM = window_manager()

(image, image_w, image_h) = WM.grab_window_image('Quartus')
(screen_w, screen_h) = pyautogui.size()

print(screen_w, screen_h, image_w, image_h)

if image is None:
	print('Cannot find Quartus')
	exit()

WM.bring_window_to_front('Quartus')

start_compile()

WM.minimize_window('Quartus')

# Wait for the compiler to start
time.sleep(5)
timeout = time.time() + 60*5

while True:
	(image, image_w, image_h) = WM.grab_window_image('Quartus')
	if abs(image_w-screen_w) > 200:
		print("Capture size error")		
		break

	if time.time() > timeout:
		print("Timeout")
		break

	success = is_compile_success()
	if success:
		print("Compile Success")
		break
	failed = is_compile_failed()
	if failed:
		print("Compile Error")
		break
	time.sleep(1)


WM.bring_window_to_front('Quartus')
WM.beep(450, 500)