# -*- coding: utf-8 -*-
import urllib
import json

class Weather():
	
	def __init__(self, cityCode = '101010100'):
		self.cityCode = cityCode
		request = urllib.urlopen('http://www.weather.com.cn/data/sk/' + cityCode + '.html')
		self.weather = json.loads(request.read())

	def getTemperature(self):
		return int(self.weather['weatherinfo']['temp'])

	def getRH(self):
		return self.weather['weatherinfo']['SD']

	def getUpdateTime(self):
		return self.weather['weatherinfo']['time']

if __name__ == "__main__":
	weather = Weather()
	print "BEGING: " + str(weather.getTemperature()) + ' ' + weather.getRH() + ' ' + weather.getUpdateTime()