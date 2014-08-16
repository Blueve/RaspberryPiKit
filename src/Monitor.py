import commands

class SysInfo():

	@staticmethod
	def getCpuInfo():
		cmdResult = commands.getoutput("top -bn1").split('\n')
		if len(cmdResult) >= 3:
			cpuInfo = cmdResult[2].split()
			if len(cpuInfo) >= 8:
				return {
					'used' : 100 - float(cpuInfo[7]),
					'free' : float(cpuInfo[7])
				}
		else:
			cpuInfo = cmdResult[0].split()
			return {
				'used' : 'UNKNOWN',
				'free' : 'UNKNOWN'
			}

	@staticmethod
	def getMemInfo():
		cmdResult = commands.getoutput('free').split('\n')
		memInfo = (cmdResult[1].split()[1:8])
		return {
			'total'  : int(memInfo[0]),
			'used'   : int(memInfo[1]),
			'free'   : int(memInfo[2]),
			'shared' : int(memInfo[3]),
			'buffers': int(memInfo[4]),
			'cached' : int(memInfo[5])
		}

	@staticmethod
	def getCpuTemperature():
		with open("/sys/class/thermal/thermal_zone0/temp") as f:
			cpuTemperature = f.read()
		return round(float(cpuTemperature) / 1000, 1)

	@staticmethod	
	def getGpuTemperature():
		gpuTemperature = commands.getoutput('/opt/vc/bin/vcgencmd measure_temp')
		return float(gpuTemperature.replace('temp=', '').replace('\'C', ''))

	@staticmethod
	def getNetInfo():
		result = []
		cmdResult = commands.getoutput('ifconfig').split('\n')
		netName = ''
		for line in cmdResult:
			temp = line.split()
			if len(temp) > 3:
				if temp[0] == 'inet':
					result.append({
							'name':netName,
							'ip'  :temp[1].replace('addr:', '')
						})
				elif temp[2] == 'encap:Ethernet':
					netName = temp[0]
		return result

	@staticmethod
	def getDiskInfo():
		cmdResult = commands.getoutput('df -h /').split('\n')
		diskInfo = cmdResult[1].split()
		return {
			'size':float(diskInfo[1].replace('G', '')),
			'used':float(diskInfo[2].replace('G', '')),
			'use%':int(diskInfo[4].replace('%', ''))
		}


if __name__ == "__main__":
	print "CPU Temperature: ", str(SysInfo.getCpuTemperature())
	print "GPU Temperature: ", str(SysInfo.getGpuTemperature())
	print "CPU Used: ", str(SysInfo.getCpuInfo()['used'])
	print "MEM Total: ", str(SysInfo.getMemInfo()['total'])
	print "IP Info: ", SysInfo.getNetInfo()[0]['name'], SysInfo.getNetInfo()[0]['ip']