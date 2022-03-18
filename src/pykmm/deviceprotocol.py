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

import serial
from enum import Enum

class KFDReplyFailed(Exception):
    pass

class KFDInvalidOpcode(Exception):
    pass

class KFDWriteFailed(Exception):
    pass

class KFDRadioTimeout(Exception):
    pass


class KFDSelfTestCodes(Enum):
    SELFTEST_PASS = 0
    SELFTEST_FAIL_DATA_SHORT_TO_GND = 1
    SELFTEST_FAIL_SENSE_SHORT_TO_GND = 2
    SELFTEST_FAIL_DATA_SHORT_TO_VCC = 3
    SELFTEST_FAIL_SENSE_SHORT_TO_VCC = 4
    SELFTEST_DATA_SENSE_SHORT = 5
    SELFTEST_SENSE_DATA_SHORT = 6


class OPKFD():
    '''A generic class for communication with open source hardware keyloaders'''
    READ_REQ = b'\x11'
    WRITE_REQ = b'\x12'
    ENTER_BOOTLOADER = b'\x13'
    RESET = b'\x14'
    SELF_TEST = b'\x15'
    SEND_KEY_SIG = b'\x16'
    SEND_BYTE = b'\x17'

    ERROR_REPLY = b'\x20'
    READ_REPLY = b'\x21'
    WRITE_REPLY = b'\x22'

    READ_ADAPTER_VER = b'\x01'
    READ_FW_VER = b'\x02'
    READ_UID = b'\x03'
    READ_MODEL = b'\x04'
    READ_HW_REV = b'\x05'
    READ_SN = b'\x06'

    WRITE_MODEL = b'\x01'
    WRITE_SN = b'\x02'

    ERROR_INVALID_CMD_LENGTH = b'\x01'
    ERROR_WRITE_FAILED = b'\x06'

    def __init__(self, port):
        self.AdapterProtocolVersion = None
        self.FirmwareVersion = None
        self.UID = None
        self.ModelNumber = None
        self.HardwareRevision = None
        self.SerialNumber = None

    def _getInfo(self):
        '''Method to collect all applicable metadata (adapter protocol, firmware version, etc) from the keyloader'''
        self.AdapterProtocolVersion = self._getAdapterVer()
        self.FirmwareVersion = self._getFwVer()
        self.UID = self._getUID()
        self.ModelNumber = self._getModel()
        self.HardwareRevision = self._getHwRev()
        self.SerialNumber = self._getSerialNumber()

    def _getAdapterVer(self):
        command = [OPKFD.READ_REQ, OPKFD.READ_ADAPTER_VER]
        self.writeToSerial(command)
        resp = self.readFromSerial()
        return command

    def _getFwVer(self):
        command = [OPKFD.READ_REQ, OPKFD.READ_FW_VER]
        return command

    def _getUID(self):
        command = [OPKFD.READ_REQ, OPKFD.READ_UID]
        return command

    def _getModel(self):
        c = self._genInfoBytes(KFDTool.READ_REQ, KFDTool.READ_MODEL)
        self._serial.write(c)
        resp = self._serial.read(5)
        # check that the reply is what we're expecting
        result = resp[1:2]
        opcode = resp[2:3]

        modelId = 0

        if (result == KFDTool.READ_REPLY and opcode == KFDTool.READ_MODEL):
            modelId = int.from_bytes(resp[3:4], "big")
        else:
            raise KFDReplyFailed("KFDTool replied with a bad code")

        return modelId

    def _getHwRev(self):
        c = self._genInfoBytes(KFDTool.READ_REQ, KFDTool.READ_HW_REV)
        self._serial.write(c)
        resp = self._serial.read(6)
        # check that the reply is what we're expecting
        result = resp[1:2]
        opcode = resp[2:3]

        version = ""

        if (result == KFDTool.READ_REPLY and opcode == KFDTool.READ_HW_REV):
            major = int.from_bytes(resp[3:4], "big")
            minor = int.from_bytes(resp[4:5], "big")

            version = "{}.{}".format(major, minor)
        else:
            raise KFDReplyFailed("KFDTool replied with a bad code")

        return version

    def _getSerialNumber(self):
        c = self._genInfoBytes(KFDTool.READ_REQ, KFDTool.READ_SN)
        self._serial.write(c)
        resp = self._serial.read(11)
        # check that the reply is what we're expecting
        result = resp[1:2]
        opcode = resp[2:3]
        length = resp[3:4]

        serial = ""

        if (result == KFDTool.READ_REPLY and opcode == KFDTool.READ_SN):
            if (length == b'\x00'):
                #no serial number
                return None
            offset = 4
            for i in range(0,5):
                uidByte = resp[offset+i:offset+i+1].hex()
                serial += "{}".format(uidByte)
        else:
            raise KFDReplyFailed("KFDTool replied with a bad code")

        return serial

    def writeModelInfo(self, hwid, hwrevMaj, hwrevMin):
        c = self._genInfoBytes(KFDTool.WRITE_REQ, KFDTool.WRITE_MODEL, hwid, hwrevMaj, hwrevMin)
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
        command = OPKFD.SELF_TEST
        self.writeToSerial(command)
        resp = self._serial.read(4)
        testResult = KFDSelfTestCodes(int.from_bytes(resp[2:3], "big"))
        return testResult
        
    def sendTwiByte(self, byte):
        command = [OPKFD.SEND_BYTE + b'\x00' + byte]
        self.writeToSerial(command)

    def _genInfoBytes(self, reqType, info, *args):
        command = b''
        if (reqType == KFDTool.READ_REQ):
            command = KFDTool.SERIAL_HEADER + reqType + info + KFDTool.SERIAL_FOOTER
        if (reqType == KFDTool.WRITE_REQ):
            if (info == KFDTool.WRITE_MODEL):
                hwid = int(args[0]).to_bytes(1, "big")
                hwverMin = int(args[1]).to_bytes(1, "big")
                hwverMaj = int(args[2]).to_bytes(1, "big")

                command = KFDTool.SERIAL_HEADER + reqType + info + hwid + hwverMin + hwverMaj + KFDTool.SERIAL_FOOTER
            if (info == KFDTool.WRITE_SN):
                serialString = args[0]
                #convert sn to uppercase, idk why but it gets borked sometimes if it's lower
                serialString = serialString.upper()
                #check if the wanted serial is too long
                if (len(serialString) > 6):
                    raise ValueError("Your serial number is too long. Try a shorter one.")
                serialBytes = serialString.encode()

                #pad the bytes out

                while (len(serialBytes) < 6):
                    serialBytes += b'\x00'

                command = KFDTool.SERIAL_HEADER + reqType + info + serialBytes + KFDTool.SERIAL_FOOTER

        return command

    def writeToSerial(self, command):
        """Frames and sends data to the keyloader"""
        raise NotImplementedError("Must be implemented in child class to frame and send data")

    def readFromSerial(self, command):
        """Reads and un-frames data from the keyloader"""
        raise NotImplementedError("Must be implemented in child class to frame and send data")

class KFDTool(OPKFD):
    '''Class to handle communication with the KFDTool'''
    SERIAL_HEADERFOOTER = b'\x61'
    SERIAL_HEADERFOOTER_PLACEHOLDER = b'\x62'
    SERIAL_ESC = b'\x63'
    SERIAL_ESC_PLACEHOLDER = b'\x64'

    def __init__(self, port):
        super()
        self._serialPort = serial.Serial(port, 115200, timeout=2)
        self._getInfo()

    def _getInfo(self):
        raise NotImplementedError

class KFDAVR(OPKFD):
    '''Class to handle communication with the KFD-AVR family'''
    SERIAL_HEADER = b'\x61'
    SERIAL_HEADER_PLACEHOLDER = b'\x62'
    SERIAL_FOOTER = b'\x63'
    SERIAL_FOOTER_PLACEHOLDER = b'\x64'
    SERIAL_ESC = b'\x70'
    SERIAL_ESC_PLACEHOLDER = b'\x71'

    def __init__(self, port):
        super()
        # set DSR/DTR to false to prevent a reset upon connection
        self._serialPort = serial.Serial(port, 115200, timeout=2, dsrdtr=False)
        self._getInfo()

    def writeToSerial(self, command):
        """Frames and sends data to the keyloader"""
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
        
        

    def enterBootloader(self):
        raise NotImplementedError("Bootloader mode does not exist on KFD-AVR")

if __name__ == "__main__":
    '''Execute basic test gathering info from connected keyloader'''
    import sys
    serialPort = 'COM3'
    kfd = KFDAVR(serialPort)

    #serialPort = 'COM8'
    #kfd = KFDTool(serialPort)
    print("Connected to {}".format(serialPort))
    print("Serial Number: {}".format(kfd.SerialNumber))

    sys.exit()
