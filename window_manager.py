# https://stackoverflow.com/questions/19695214/python-screenshot-of-inactive-window-printwindow-win32gui/24352388#24352388
import win32gui
import win32com.client
import win32ui
import winsound
import re
import time
from ctypes import windll
from PIL import Image

class window_manager:
	_hwnd = None
	origin_left = None
	origin_top = None

	def _enumHandler(self, hwnd, window_name):
		if window_name in win32gui.GetWindowText(hwnd):
			self._hwnd = hwnd
			print('Found: {}'.format(win32gui.GetWindowText(self._hwnd)))

	def bring_window_to_front(self, window_name):     
		win32gui.EnumWindows(self._enumHandler, window_name)    
		win32gui.SetWindowPos(self._hwnd, 0, self.origin_left, self.origin_top, 0, 0, 1)	
		win32gui.ShowWindow(self._hwnd, 3)
		
		# Weird workaround: 
		# https://stackoverflow.com/questions/14295337/win32gui-setactivewindow-error-the-specified-procedure-could-not-be-found
		shell = win32com.client.Dispatch("WScript.Shell")
		shell.SendKeys('%')

		win32gui.SetForegroundWindow(self._hwnd)
		

	def minimize_window(self, window_name):
		win32gui.EnumWindows(self._enumHandler, window_name)   
		win32gui.ShowWindow(self._hwnd, 2)

	def beep(self, frequency, duration):
		winsound.Beep(frequency, duration)

	def grab_window_image(self, window_name):
		win32gui.EnumWindows(self._enumHandler, window_name)		
		win32gui.ShowWindow(self._hwnd, 3)

		# Change the line below depending on whether you want the whole window
		# or just the client area. 
		#left, top, right, bot = win32gui.GetClientRect(self._hwnd)
		left, top, right, bot = win32gui.GetWindowRect(self._hwnd)
		w = right - left
		h = bot - top
		print(left, top, right, bot)
		self.origin_left = left
		self.origin_top = top
		# Workaround - activate the window at the bottom
		#win32gui.SetWindowPos(self._hwnd, 1, 0, 0, 0, 0, 1)		
		win32gui.SetWindowPos(self._hwnd, 1, self.origin_left, self.origin_top, 0, 0, 1)	

		hwndDC = win32gui.GetWindowDC(self._hwnd)
		mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
		saveDC = mfcDC.CreateCompatibleDC()

		saveBitMap = win32ui.CreateBitmap()
		saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

		saveDC.SelectObject(saveBitMap)

		# Change the line below depending on whether you want the whole window
		# or just the client area. 
		#result = windll.user32.PrintWindow(self._hwnd, saveDC.GetSafeHdc(), 1)
		result = windll.user32.PrintWindow(self._hwnd, saveDC.GetSafeHdc(), 0)

		bmpinfo = saveBitMap.GetInfo()
		bmpstr = saveBitMap.GetBitmapBits(True)

		im = Image.frombuffer(
			'RGB',
			(bmpinfo['bmWidth'], bmpinfo['bmHeight']),
			bmpstr, 'raw', 'BGRX', 0, 1)

		win32gui.DeleteObject(saveBitMap.GetHandle())
		saveDC.DeleteDC()
		mfcDC.DeleteDC()
		win32gui.ReleaseDC(self._hwnd, hwndDC)

		return (im, bmpinfo['bmWidth'], bmpinfo['bmHeight'])