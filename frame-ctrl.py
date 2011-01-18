#!/usr/bin/env python

import os
import sys
import time
import usb.core
from usb.util import *

vendorId = 0x04e8
models = {'SPF-87H': (0x2033, 0x2034), 'SPF-107H': (0x2027, 0x2028) }

chunkSize = 0x4000
bufferSize = 0x20000

def expect(result, verifyList):
  resultList = result.tolist()
  if resultList != verifyList:
    print "Warning: Expected " + str(verifyList) + " but got " + str(resultList)

def storageToDisplay(dev):
  print "Setting device to display mode"
  try:
    dev.ctrl_transfer(CTRL_TYPE_STANDARD | CTRL_IN | CTRL_RECIPIENT_DEVICE, 0x06, 0xfe, 0xfe, 254)
  except usb.core.USBError as e:
    errorStr = str(e)
    if errorStr != 'No such device (it may have been disconnected)':
      raise e

def displayModeSetup(dev):
  print "Sending setup commands to device"
  dev.set_configuration()
  result = dev.ctrl_transfer(CTRL_TYPE_VENDOR | CTRL_IN | CTRL_RECIPIENT_DEVICE, 0x04, 0x00, 0x00, 1)
  expect(result, [ 0x03 ])
#  result = dev.ctrl_transfer(CTRL_TYPE_VENDOR | CTRL_IN | CTRL_RECIPIENT_DEVICE, 0x01, 0x00, 0x00, 2)
#  expect(result, [ 0x09, 0x04 ])
#  result = dev.ctrl_transfer(CTRL_TYPE_VENDOR | CTRL_IN | CTRL_RECIPIENT_DEVICE, 0x02, 0x00, 0x00, 1)
#  expect(result, [ 0x46 ])

def chunkyWrite(dev, buf):
  pos = 0
  while pos < bufferSize:
    dev.write(0x02, buf[pos:pos+chunkSize])
    pos += chunkSize

def writeImage(dev, path):
#  result = dev.ctrl_transfer(CTRL_TYPE_STANDARD | CTRL_IN | CTRL_RECIPIENT_DEVICE, 0x06, 0x0300, 0x00, 255)
#  expect(result, [ 0x04, 0x03, 0x09, 0x04 ])

#  result = dev.ctrl_transfer(CTRL_TYPE_STANDARD | CTRL_IN | CTRL_RECIPIENT_DEVICE, 0x06, 0x0301, 0x0409, 255)

  size = os.path.getsize(path)
  f = open(path)

  buf = bytearray(bufferSize)

  header = bytearray([ 0xa5, 0x5a, 0x09, 0x04, size & 0xff, size >> 8 & 0xff, size >> 16 & 0xff, size >> 24 & 0xff, 0x46, 0x00, 0x00, 0x00 ])

  headerSize = len(header)

  data = f.read(bufferSize - headerSize)
  buf[0:headerSize] = header
  buf[headerSize:headerSize + len(data)] = data
  chunkyWrite(dev, buf)
  
  while True:
    data = f.read(bufferSize)
    if data == "":
      break    
    buf[0:len(data)] = data
    for i in xrange(len(data), len(buf)):
      buf[i] = 0
    chunkyWrite(dev, buf)

#  result = dev.ctrl_transfer(CTRL_TYPE_VENDOR | CTRL_IN | CTRL_RECIPIENT_DEVICE, 0x06, 0x00, 0x00, 2)
#  expect(result, [ 0x00, 0x00 ])

  f.close()

for k, v in models.iteritems():
  dev = usb.core.find(idVendor=vendorId, idProduct=v[0])
  if dev:
    print "Found " + k + " in storage mode"
    storageToDisplay(dev)
    time.sleep(1)
  dev = usb.core.find(idVendor=vendorId, idProduct=v[1])
  if dev:
    print "Found " + k + " in display mode"
    displayModeSetup(dev)
    writeImage(dev, sys.argv[1])
