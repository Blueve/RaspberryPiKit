RaspberryPiKit
==============

Design for Raspberry Pi! 
Base on Adafruit CharLCDPlate and Raspbian System.

## src
### Monitor.py
You can retrieve system information such as: CPU used/ CPU Temperature/ Mem used/ Disk used/ Network infomation/... by use this moudle.

```python
# Example
print "CPU Temperature: ", str(SysInfo.getCpuTemperature())
print "CPU Used: ", str(SysInfo.getCpuInfo()['used'])
print "MEM Total: ", str(SysInfo.getMemInfo()['total'])
```

### Display.py
This is a LCD GUI moudle that have many convenient feature for your Pi:

1. A menu included `System Info` `Network Info`..etc which allow you controlling by key pad.
1. You can add `sudo python Display.py` script to `/etc/rc/loacl` then you can run it automatic during system boot.
1. You can get your Pi's IP address without use additional screen or search on routing table! That was a big reason why I made it:)
