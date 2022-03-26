#!/usr/bin/env python
#
# PyKMM - KMM and keyloading for Python
# GPLv2 Open Source. Use is subject to license terms.
# DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS FILE HEADER.
#
# @package PyKMM
#
###############################################################################
#   Copyright (C) 2022 Natalie Moore <natalie@natnat.xyz>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software Foundation,
#   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
###############################################################################

from struct import unpack
import serial
from enum import Enum
import time

from pykmm.kmm.items import KeyItem

class DLI():
    def __init__(self):
        self.ip = "0.0.0.0"
        self.port = 1234

class OPKFD():
    '''A generic class for communication with open source hardware keyloaders'''
    CMD_READ_REQ = 0x11
    CMD_WRITE_REQ = 0x12
    CMD_ENTER_BOOTLOADER = 0x13
    CMD_RESET = 0x14
    CMD_SELF_TEST = 0x15
    CMD_SEND_KEY_SIG = 0x16
    CMD_SEND_BYTE = 0x17

    REPLY_ERROR = 0x20
    REPLY_READ = 0x21
    REPLY_WRITE = 0x22
    REPLY_ENTER_BSL_MODE = 0x23
    REPLY_RESET = 0x24
    REPLY_SELF_TEST = 0x25
    REPLY_SEND_KEYSIG = 0x26
    REPLY_SEND_BYTE = 0x27

    READ_ADAPTER_VER = 0x01
    READ_FW_VER = 0x02
    READ_UID = 0x03
    READ_MODEL = 0x04
    READ_HW_REV = 0x05
    READ_SN = 0x06

    WRITE_MODEL = 0x01
    WRITE_SN = 0x02

    ERROR_OTHER = 0x00
    ERROR_INVALID_CMD_LENGTH = 0x01
    ERROR_INVALID_CMD_OPCODE = 0x02
    ERROR_INVALID_READ_OPCODE = 0x03
    ERROR_READ_FAILED = 0x04
    ERROR_INVALID_WRITE_OPCODE = 0x05
    ERROR_WRITE_FAILED = 0x06

    KFDSelfTestCodes = [
    "PASS",
    "DATA_SHORT_TO_GND",
    "SENSE_SHORT_TO_GND",
    "DATA_SHORT_TO_VCC",
    "SENSE_SHORT_TO_VCC",
    "DATA_SENSE_SHORT",
    "SENSE_DATA_SHORT",
    ]

    def __init__(self, port):
        self.AdapterProtocolVersion = None
        self.FirmwareVersion = None
        self.UID = None
        self.ModelNumber = None
        self.HardwareRevision = None
        self.SerialNumber = None

    def _getInfo(self):
        '''Method to collect all applicable metadata (adapter protocol, firmware version, etc) from the keyloader and update the object'''
        self._openSerial()
        self.AdapterProtocolVersion = self._readInfo(OPKFD.READ_ADAPTER_VER)
        self.FirmwareVersion = self._readInfo(OPKFD.READ_FW_VER)
        self.UID = self._readInfo(OPKFD.READ_UID)
        self.ModelNumber = self._readInfo(OPKFD.READ_MODEL)
        self.HardwareRevision = self._readInfo(OPKFD.READ_HW_REV)
        self.SerialNumber = self._readInfo(OPKFD.READ_SN)
        self._closeSerial()

    def _readInfo(self, infoToRead):
        '''Method to request data from keyloader'''
        command = [OPKFD.CMD_READ_REQ, infoToRead]
        self.writeToSerial(command)
        resp = self.readFromSerial()
        
        opcode = resp[0]
        subop = resp[1]
        if (opcode == OPKFD.REPLY_READ):
            if (subop == OPKFD.READ_ADAPTER_VER):
                adpver = "{}.{}.{}".format(resp[2], resp[3], resp[4])
                return adpver
            elif (subop == OPKFD.READ_FW_VER):
                fwver = "{}.{}.{}".format(resp[2], resp[3], resp[4])
                return fwver
            elif (subop == OPKFD.READ_UID):
                uid = ""
                for i in range(2, len(resp)):
                    uid += "{}".format(resp[i])
                return uid
            elif (subop == OPKFD.READ_MODEL):
                modelno = resp[2]
                return modelno
            elif (subop == OPKFD.READ_HW_REV):
                hwrev = "{}.{}".format(resp[2], resp[3])
                return hwrev
            elif (subop == OPKFD.READ_SN):
                serialLength = resp[2]
                serialNo = ""
                if (serialLength > 0):
                    for i in range(3, serialLength+3):
                        print("Serial number byte: {}".format(resp[i]))
                        serialNo += "{}".format(str(resp[i]))
                else:
                    serialNo = "NOT SET"
                return serialNo
            else:
                raise Exception("Unknown data type received: {}".format(subop))
        else:
            raise Exception("Expected READ_REPLY opcode (0x21) but got {}".format(opcode))

    def writeModelInfo(self, hwid, hwrevMaj, hwrevMin):
        c = self._genInfoBytes(KFDTool.CMD_WRITE_REQ, KFDTool.WRITE_MODEL, hwid, hwrevMaj, hwrevMin)
        #print("Writing bytes: {}".format(c))
        self._serial.write(c)
        resp = self._serial.read(3)
        #print("Reply: {}".format(resp))
        result = resp[1:2]
        opcode = resp[2:3]

        if (result == KFDTool.WRITE_REPLY):
            return 1
        else:
            raise KFDWriteFailed()

    def writeSerialNumber(self, serialNum):
        c = self._genInfoBytes(KFDTool.WRITE_REQ, KFDTool.WRITE_SN, serialNum)
        #print("Writing bytes: {}".format(c))
        self._serial.write(c)
        resp = self._serial.read(3)
        #print("Reply: {}".format(resp))
        result = resp[1:2]
        opcode = resp[2:3]

        if (result == KFDTool.WRITE_REPLY):
            return 1
        else:
            raise KFDWriteFailed()

    def enterBootloader(self):
        command = KFDTool.SERIAL_HEADER + KFDTool.ENTER_BOOTLOADER + KFDTool.SERIAL_FOOTER
        self._serial.write(command)

    def reset(self):
        command = KFDTool.SERIAL_HEADER + KFDTool.RESET + KFDTool.SERIAL_FOOTER
        self._serial.write(command)

    def selfTest(self):
        command = [OPKFD.CMD_SELF_TEST]
        self.writeToSerial(command)
        resp = self.readFromSerial()
        assert resp[0] == OPKFD.REPLY_SELF_TEST
        return resp[1]
        
    def sendTwiByte(self, byte):
        command = [OPKFD.CMD_SEND_BYTE + 0x00 + byte]
        self.writeToSerial(command)

    def writeToSerial(self, command):
        """Frames and sends data to the keyloader"""
        raise NotImplementedError("Must be implemented in child class to frame and send data")

    def readFromSerial(self):
        """Blocking method to read and un-frame data from the keyloader"""
        raise NotImplementedError("Must be implemented in child class to frame and send data")

    def _openSerial(self):
        raise NotImplementedError

    def _closeSerial(self):
        raise NotImplementedError

class KFDTool(OPKFD):
    '''Class to handle communication with the KFDTool'''
    SERIAL_HEADERFOOTER = 0x61
    SERIAL_HEADERFOOTER_PLACEHOLDER = 0x62
    SERIAL_ESC = 0x63
    SERIAL_ESC_PLACEHOLDER = 0x64

    def __init__(self, port):
        super()
        self._serialPort = serial.Serial(port, 115200, timeout=2)
        self._getInfo()

    def _getInfo(self):
        raise NotImplementedError

    def openSerial(self):
        raise NotImplementedError

    def closeSerial(self):
        raise NotImplementedError

class KFDAVR(OPKFD):
    '''Class to handle communication with the KFD-AVR family'''
    SERIAL_HEADER = 0x61
    SERIAL_HEADER_PLACEHOLDER = 0x62
    SERIAL_FOOTER = 0x63
    SERIAL_FOOTER_PLACEHOLDER = 0x64
    SERIAL_ESC = 0x70
    SERIAL_ESC_PLACEHOLDER = 0x71

    READ_KEY_INFO = 0x07

    WRITE_KEY = 0x03

    MAX_INSTALLED_KEYS = 15

    def __init__(self, port):
        super()
        # set DSR/DTR to prevent a reset upon connection
        self._serialPort = serial.Serial(port, 
                                         baudrate=115200,
                                         timeout=2,
                                         xonxoff=0,
                                         rtscts=0,
                                         dsrdtr=True
                                         )
        self._getInfo()

    def _openSerial(self):
        if (self._serialPort.is_open):
            #don't open an already open port
            pass
        else:
            self._serialPort.open()

    def _closeSerial(self):
        if (self._serialPort.is_open):
            self._serialPort.close()
        else:
            #don't close an already closed port
            pass

    def writeToSerial(self, command):
        """Frames and sends data to the keyloader"""
        self._openSerial()
        toSend = bytearray()
        toSend.append(KFDAVR.SERIAL_HEADER)

        # iterate through bytes and escape if needed
        for b in command:
            if (b == KFDAVR.SERIAL_ESC):
                toSend.append(KFDAVR.SERIAL_ESC)
                toSend.append(KFDAVR.SERIAL_ESC_PLACEHOLDER)

            elif (b == KFDAVR.SERIAL_HEADER):
                toSend.append(KFDAVR.SERIAL_ESC)
                toSend.append(KFDAVR.SERIAL_HEADER_PLACEHOLDER)
            
            elif (b == KFDAVR.SERIAL_FOOTER):
                toSend.append(KFDAVR.SERIAL_ESC)
                toSend.append(KFDAVR.SERIAL_FOOTER_PLACEHOLDER)

            else:
                toSend.append(b)

        toSend.append(KFDAVR.SERIAL_FOOTER)

        self._serialPort.write(toSend)

    def readFromSerial(self):
        unpackedData = []
        fullFrameReceived = False
        #set a timeout so we don't loop forever, 2 sec is probably fine
        t_end = time.time() + 2
        while time.time() < t_end:
            b = self._serialPort.read(1)
            b = int.from_bytes(b, "big")
            if (b == KFDAVR.SERIAL_HEADER):
                # if we get a header, clear the buffer
                unpackedData = []
            elif (b == KFDAVR.SERIAL_FOOTER):
                #clean up and un-escape bytes
                for i in range(0, len(unpackedData)):
                    if (unpackedData[i] == KFDAVR.SERIAL_ESC):
                        del unpackedData[i]
                        if (unpackedData[i] == KFDAVR.SERIAL_ESC_PLACEHOLDER):
                            unpackedData[i] = KFDAVR.SERIAL_ESC
                        elif (unpackedData[i] == KFDAVR.SERIAL_HEADER_PLACEHOLDER):
                            unpackedData[i] = KFDAVR.SERIAL_HEADER
                        elif (unpackedData[i] == KFDAVR.SERIAL_FOOTER_PLACEHOLDER):
                            unpackedData[i] = KFDAVR.SERIAL_FOOTER
                        else:
                            raise Exception("Invalid character after escape")
                fullFrameReceived = True
                break
            else:
                unpackedData.append(b)

        if (fullFrameReceived):
            return unpackedData
        else:
            raise TimeoutError("KFD failed to reply in a timely manner.")
            return
    
    def getInstalledKeyInfo(self):
        '''Return a list of all keys installed on the KFD-AVR'''
        installedKeys = []
        for i in range(0, KFDAVR.MAX_INSTALLED_KEYS):
            command = [OPKFD.CMD_READ_REQ, KFDAVR.READ_KEY_INFO, i]
            self.writeToSerial(command)
            resp = self.readFromSerial()
            
            opcode = resp[0]
            subop = resp[1]
            print(opcode)
            print(subop)
            if (opcode == OPKFD.ERROR_READ_FAILED):
                #there probably isn't a key here
                pass
            elif (opcode == OPKFD.REPLY_READ):
                if (opcode == KFDAVR.READ_KEY_INFO):
                    ckr |= resp[4] << 8
                    ckr |= resp[5]
                    kid |= resp[6] << 8
                    kid |= resp[7]
                else:
                    raise Exception("KFD replied with unknown read data")
            else:
                raise Exception("KFD replied with unknown opcode")

    def writeInstalledKey(self, slot, keyToInstall):
        if (not isinstance(slot, int)):
            raise TypeError("Slot must be an int, not {}".format(type(slot)))
        if (slot > KFDAVR.MAX_INSTALLED_KEYS):
            raise ValueError("You tried to install a key into slot {}; while the device supports a maximum of {} slots.".format(slot, KFDAVR.MAX_INSTALLED_KEYS))

        if (isinstance(keyToInstall, KeyItem)):
            command = [OPKFD.CMD_WRITE_REQ, KFDAVR.WRITE_KEY]
            command[2] = (slot >> 8) & 0xFF
            command[3] = 0  # flags are reserved for now
            command[4] = (keyToInstall.sln >> 8) & 0xFF
            command[5] = (keyToInstall.sln & 0xFF)
            command[6] = (keyToInstall.kid >> 8) & 0xFF
            command[7] = (keyToInstall.kid & 0xFF)

            for b in keyToInstall.key:
                command.append(b)
        else:
            raise TypeError("You must pass a KeyItem type to me; see pykmm.kmm.items.KeyItem")

    def zeroizeInstalledKeys(self):
        command = [OPKFD.CMD_WRITE_REQ, KFDAVR.WRITE_KEY, 0xFE]
        self.writeToSerial(command)
        
    def enterBootloader(self):
        raise NotImplementedError("Bootloader mode does not exist on KFD-AVR")

def main():
    '''Execute basic test gathering info from connected keyloader'''
    import sys
    serialPort = 'COM3'
    kfd = KFDAVR(serialPort)

    #serialPort = 'COM8'
    #kfd = KFDTool(serialPort)
    print("Connected to {}".format(serialPort))
    print("Serial\t: {}".format(kfd.AdapterProtocolVersion))
    print("FwVer\t: {}".format(kfd.FirmwareVersion))
    print("UID\t: {}".format(kfd.UID))
    print("MdlNo\t: {}".format(kfd.ModelNumber))
    print("HwRev\t: {}".format(kfd.HardwareRevision))
    print("SerNo\t: {}".format(kfd.SerialNumber))
    selfTestResult = kfd.selfTest()
    selfTestText = KFDAVR.KFDSelfTestCodes[selfTestResult]
    print("SelfTest: {} ({})".format(selfTestResult, selfTestText))
    print("Installed Keys: {}".format(kfd.getInstalledKeyInfo()))

    sys.exit()

if __name__ == "__main__":
    main()
