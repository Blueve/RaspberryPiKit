from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from Monitor import SysInfo
import thread

class Display():

	CHAR_SET = [
				[0b00000, # 0 <-
				 0b00010,
				 0b00110,
				 0b01110,
				 0b00110,
				 0b00010,
				 0b00000,
				 0b00000],
				[0b00000, # 1 ->
				 0b01000,
				 0b01100,
				 0b01110,
				 0b01100,
				 0b01000,
				 0b00000,
				 0b00000],
				[0b00000, # 2 ^
				 0b00000,
				 0b00100,
				 0b01110,
				 0b11111,
				 0b00000,
				 0b00000,
				 0b00000],
				[0b00000, # 3 v
				 0b00000,
				 0b11111,
				 0b01110,
				 0b00100,
				 0b00000,
				 0b00000,
				 0b00000],
				[0b00110, # 4 Degree
				 0b01001,
				 0b01001,
				 0b00110,
				 0b00000,
				 0b00000,
				 0b00000,
				 0b00000],
				[0b11111, # 5 Black Block
				 0b11111,
				 0b11111,
				 0b11111,
				 0b11111,
				 0b11111,
				 0b11111,
				 0b11111],
				[0b10101, # 6 Gray Block
				 0b01010,
				 0b10101,
				 0b01010,
				 0b10101,
				 0b01010,
				 0b10101,
				 0b01010]
			   ]

	AUTO_REFRESH_PERIOD = 5

	OPSET = (Adafruit_CharLCDPlate.LEFT,
			 Adafruit_CharLCDPlate.RIGHT,
			 Adafruit_CharLCDPlate.UP,
			 Adafruit_CharLCDPlate.DOWN,
			 Adafruit_CharLCDPlate.SELECT)

	OPLANG = {Adafruit_CharLCDPlate.LEFT:'LEFT',
			  Adafruit_CharLCDPlate.RIGHT:'RIGHT',
			  Adafruit_CharLCDPlate.UP:'UP',
			  Adafruit_CharLCDPlate.DOWN:'DOWN',
			  Adafruit_CharLCDPlate.SELECT:'SELECT'}

	MENU = ('     SELECT ' + chr(1) + '   \nSystem Info',
			'   ' + chr(0) + ' SELECT ' + chr(1) + '   \nNetwork Info',
			'   ' + chr(0) + ' SELECT ' + chr(1) + '   \nTemperature',
			'   ' + chr(0) + ' SELECT ' + chr(1) + '   \nDisk Info',
			'   ' + chr(0) + ' SELECT ' + chr(1) + '   \nSystem Tools',
			'   ' + chr(0) + ' SELECT ' + chr(1) + '   \nSetting',
			'   ' + chr(0) + ' SELECT     \nExit')

	# State transition table
	STT = {
		# MENU_0 SYSTEM INFO
		0:{
			0:{
				Adafruit_CharLCDPlate.RIGHT : (1, 0),
				Adafruit_CharLCDPlate.SELECT: (0, 1)
			},
			# DEFAULT
			1:{
				Adafruit_CharLCDPlate.LEFT: (0, 0)
			}
		},
		# MENU_1 NETWORK INFO
		1:{
			0:{
				Adafruit_CharLCDPlate.LEFT  : (0, 0),
				Adafruit_CharLCDPlate.RIGHT : (2, 0),
				Adafruit_CharLCDPlate.SELECT: (1, 1)
			},
			# DEFAULT
			1:{
				Adafruit_CharLCDPlate.LEFT: (1, 0),
				Adafruit_CharLCDPlate.UP    : (1, 2),
				Adafruit_CharLCDPlate.DOWN  : (1, 3)
			},
			# PAGE UP
			2:{
				Adafruit_CharLCDPlate.LEFT: (1, 0),
				Adafruit_CharLCDPlate.UP    : (1, 2),
				Adafruit_CharLCDPlate.DOWN  : (1, 3)
			},
			# PAGE DOWN
			3:{
				Adafruit_CharLCDPlate.LEFT: (1, 0),
				Adafruit_CharLCDPlate.UP    : (1, 2),
				Adafruit_CharLCDPlate.DOWN  : (1, 3)
			}
		},
		# MENU_2 TEMPERATURE
		2:{
			0:{
				Adafruit_CharLCDPlate.LEFT  : (1, 0),
				Adafruit_CharLCDPlate.RIGHT : (3, 0),
				Adafruit_CharLCDPlate.SELECT: (2, 1)
			},
			# DEFAULT
			1:{
				Adafruit_CharLCDPlate.LEFT: (2, 0)
			}
		},
		# MENU_3 DISK INFO
		3:{
			0:{
				Adafruit_CharLCDPlate.LEFT  : (2, 0),
				Adafruit_CharLCDPlate.RIGHT : (4, 0),
				Adafruit_CharLCDPlate.SELECT: (3, 1)
			},
			# DEFAULT
			1:{
				Adafruit_CharLCDPlate.LEFT: (3, 0)
			}
		},
		# MENU_4 SYSTEM TOOLS
		4:{
			0:{
				Adafruit_CharLCDPlate.LEFT  : (3, 0),
				Adafruit_CharLCDPlate.RIGHT : (5, 0),
				Adafruit_CharLCDPlate.SELECT: (4, 1)
			},
			# DEFAULT
			1:{
				Adafruit_CharLCDPlate.LEFT: (4, 0)
			}
		},
		# MENU_5 SETTING
		5:{
			0:{
				Adafruit_CharLCDPlate.LEFT  : (4, 0),
				Adafruit_CharLCDPlate.RIGHT : (6, 0),
				Adafruit_CharLCDPlate.SELECT: (5, 1)
			},
			# DEFAULT
			1:{
				Adafruit_CharLCDPlate.LEFT: (5, 0)
			}
		},
		# MENU_6 EXIT
		6:{
			0:{
				Adafruit_CharLCDPlate.LEFT  : (5, 0),
				Adafruit_CharLCDPlate.SELECT: (6, 1)
			},
			# NO
			1:{
				Adafruit_CharLCDPlate.SELECT: (6, 0),
				Adafruit_CharLCDPlate.RIGHT : (6, 2)
			},
			# YES
			2:{
				Adafruit_CharLCDPlate.SELECT: (6, 3),
				Adafruit_CharLCDPlate.LEFT  : (6, 1)
			},
			# EXIT
			3:{
			}
		}
	}
	
	def __init__(self, curMenu = 0, debug = False):
		# Init EventMethods
		self.EventMethods = {
			'EventMethods_01': self.EventMethods_SystemInfo,
			'EventMethods_11': self.EventMethods_NetworkInfo,
			'EventMethods_12': self.EventMethods_NetworkInfo_Up,
			'EventMethods_13': self.EventMethods_NetworkInfo_Down,
			'EventMethods_21': self.EventMethods_Temperature,
			'EventMethods_31': self.EventMethods_DiskInfo,
			'EventMethods_61': self.EventMethods_Exit_No,
			'EventMethods_62': self.EventMethods_Exit_Yes,
			'EventMethods_63': self.EventMethods_Exit
		}
		# Init LCD
		self.lcd = Adafruit_CharLCDPlate()
		self.lcd.begin(16, 2)
		self.lcd.backlight(Adafruit_CharLCDPlate.RED)
		sleep(1)
		self.lcd.backlight(Adafruit_CharLCDPlate.GREEN)
		sleep(1)
		self.lcd.backlight(Adafruit_CharLCDPlate.BLUE)
		sleep(1)
		self.lcd.backlight(Adafruit_CharLCDPlate.ON)
		# Init Char Set
		for i, item in enumerate(self.CHAR_SET):
			self.lcd.createChar(i, item)
		# Set default screen
		self.curMenu = curMenu
		self.curPage = 0
		self.debug = debug
		# Init AutoRefeashMethods
		self.AutoRefreshMethod = None
		thread.start_new_thread(self.autoRefresh, ())

	def autoRefresh(self):
		if(self.debug):
			print 'Auto refresh thread started!'
		while True:
			if self.AutoRefreshMethod != None:
				self.EventMethods[self.AutoRefreshMethod]()
				if(self.debug):
					print self.AutoRefreshMethod, ' fired!'
			sleep(self.AUTO_REFRESH_PERIOD)
		
	def clear(self):
		self.lcd.noBlink()
		self.lcd.noCursor()
		self.lcd.clear()

	def message(self, message):
		self.clear()
		self.lcd.message(message)

	def blink(self, col, row):
		self.lcd.setCursor(col, row)
		self.lcd.cursor()
		self.lcd.blink()

	def show(self):
		if self.curPage == 0:
			self.message(self.MENU[self.curMenu])
		else:
			try:
				self.EventMethods['EventMethods_' + str(self.curMenu) + str(self.curPage)]()
			except Exception, e:
				if(self.debug):
					self.lcd.message(str(e))
				else:
					self.lcd.message('ERROR!\nPlease try again')
			
	def changeState(self, op):
		if self.debug:
			print 'Op: ', str(op)
		self.AutoRefreshMethod = None
		if op in self.STT[self.curMenu][self.curPage]:
			(self.curMenu, self.curPage) = self.STT[self.curMenu][self.curPage][op]
			if self.debug:
				print 'Change state to:', str(self.curMenu), ' - ' , str(self.curPage)

	def begin(self):
		# Init screen
		self.show()
		# Handle operations
		self.running = True
		while self.running:
			for op in self.OPSET:
				if self.lcd.buttonPressed(op):
					self.changeState(op)
					self.show()
					# Set a delay time to avoid run continuously
					sleep(.2)
		self.exit()

	def exit(self):
		self.clear()
		self.lcd.backlight(Adafruit_CharLCDPlate.OFF)

	def EventMethods_SystemInfo(self):
		self.AutoRefreshMethod = 'EventMethods_01'
		self.message('CPU Used: ' + str(SysInfo.getCpuInfo()['used']) + '%\nMEM FREE: ' + str(SysInfo.getMemInfo()['free']/1024) + 'MB')

	def getNetworkInfo(self, networkInfo):
		if len(networkInfo) > 0:
			self.message(SysInfo.getNetInfo()[self.NetworkPageId ]['name'] + ':\n' + SysInfo.getNetInfo()[self.NetworkPageId ]['ip'])
		else:
			self.message('NONE')

	def EventMethods_NetworkInfo(self):
		self.NetworkPageId = 0
		self.getNetworkInfo(SysInfo.getNetInfo())

	def EventMethods_NetworkInfo_Up(self):
		networkInfo = SysInfo.getNetInfo()
		self.NetworkPageId = (self.NetworkPageId + 1) % len(networkInfo)
		self.getNetworkInfo(networkInfo)

	def EventMethods_NetworkInfo_Down(self):
		networkInfo = SysInfo.getNetInfo()
		self.NetworkPageId = (self.NetworkPageId - 1) % len(networkInfo)
		self.getNetworkInfo(networkInfo)

	def EventMethods_Temperature(self):
		self.AutoRefreshMethod = 'EventMethods_21'
		self.message('CPU: ' + str(SysInfo.getCpuTemperature()) + chr(4) + 'C\nGPU: ' + str(SysInfo.getGpuTemperature()) + chr(4) + 'C')

	def EventMethods_DiskInfo(self):
		blackGridNum = (10 * SysInfo.getDiskInfo()['use%'] + 50) / 100
		line_2 = ''
		for i in range(0, blackGridNum):
			line_2 = line_2 + chr(5)
		for i in range(0, 10 - blackGridNum):
			line_2 = line_2 + chr(6)
		self.message('Disk used: ' + str(SysInfo.getDiskInfo()['used']) + 'GB\n' + line_2 + ' ' + str(SysInfo.getDiskInfo()['use%']) + '%')

	def EventMethods_Exit_No(self):
		self.message('Exit?\n(No/Yes)')
		self.blink(1, 1)

	def EventMethods_Exit_Yes(self):
		self.message('Exit?\n(No/Yes)')
		self.blink(4, 1)

	def EventMethods_Exit(self):
		self.message('Exiting...\nBye! :)')
		sleep(1.5)
		self.running = False

if __name__ == '__main__':
	display = Display(0, True)
	display.begin()