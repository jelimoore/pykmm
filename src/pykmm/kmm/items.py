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

from bitarray import bitarray

class KeyItem():
    def __init__(self):
        self._sln = 0
        self._kid = 0
        self._key = 0
        self.kek = False
        self.erase = False

    def get_sln(self):
        return self._sln
    
    def set_sln(self, slnIn):
        if (isinstance(slnIn, int)):
            if (slnIn > 0 and slnIn < 0xFFFF):
                self._sln = slnIn
            else:
                raise ValueError("SLN must be between 0x0 and 0xFFFF")
        else:
            raise TypeError("SLN must be an int type")
    
    def del_sln(self):
        del self._sln

    def get_kid(self):
        return self._kid
    
    def set_kid(self, kidIn):
        if (isinstance(kidIn, int)):
            if (kidIn > 0 and kidIn < 0xFFFF):
                self._kid = kidIn
            else:
                raise ValueError("SLN must be between 0x0 and 0xFFFF")
        else:
            raise TypeError("SLN must be an int type")
    
    def del_kid(self):
        del self._kid

    def get_key(self):
        return self._key
    
    def set_key(self, keyIn):
        if (isinstance(keyIn, int)):
            self._key = keyIn
        else:
            raise TypeError("SLN must be an int type")
    
    def del_key(self):
        del self._key

    def to_bytes(self):
        keyItemFormat = bitarray(8)
        keyItemFormat[7] = self.kek
        keyItemFormat[5] = self.erase

        keyItemBytes = bytearray(5 + len(self._key))
        keyItemBytes[0] = keyItemFormat
        #keyItemBytes += self._sln   # 2 bytes
        #keyItemBytes += self._kid   # 2 bytes
        #keyItemBytes += self._key   # however long the key is

        #TODO: finish this

        return keyItemBytes

    def parse(self, bytesIn):
        if (len(bytesIn) < 5):
            raise ValueError("Expected more then 5 bytes incoming but got {}".format(len(bytesIn)))

        #TODO: finish

    sln = property(get_sln, set_sln, del_sln)
    kid = property(get_kid, set_kid, del_kid)
    key = property(get_key, set_key, del_key)


class KeyInfo():
    def __init__(self):
        self._sln = 0
        self._kid = 0
        self._key = 0
        self.kek = False
        self.erase = False

    def get_sln(self):
        return self._sln
    
    def set_sln(self, slnIn):
        if (isinstance(slnIn, int)):
            if (slnIn > 0 and slnIn < 0xFFFF):
                self._sln = slnIn
            else:
                raise ValueError("SLN must be between 0x0 and 0xFFFF")
        else:
            raise TypeError("SLN must be an int type")
    
    def del_sln(self):
        del self._sln

    def get_kid(self):
        return self._kid
    
    def set_kid(self, kidIn):
        if (isinstance(kidIn, int)):
            if (kidIn > 0 and kidIn < 0xFFFF):
                self._kid = kidIn
            else:
                raise ValueError("SLN must be between 0x0 and 0xFFFF")
        else:
            raise TypeError("SLN must be an int type")
    
    def del_kid(self):
        del self._kid

    def get_key(self):
        return self._key
    
    def set_key(self, keyIn):
        if (isinstance(keyIn, int)):
            self._key = keyIn
        else:
            raise TypeError("SLN must be an int type")
    
    def del_key(self):
        del self._key

    def to_bytes(self):
        keyItemFormat = bitarray(8)
        keyItemFormat[7] = self.kek
        keyItemFormat[5] = self.erase

        keyItemBytes = bytearray(5 + len(self._key))
        keyItemBytes[0] = keyItemFormat
        #keyItemBytes += self._sln   # 2 bytes
        #keyItemBytes += self._kid   # 2 bytes
        #keyItemBytes += self._key   # however long the key is

        #TODO: finish this

        return keyItemBytes

    def parse(self, bytesIn):
        if (len(bytesIn) < 5):
            raise ValueError("Expected more then 5 bytes incoming but got {}".format(len(bytesIn)))

        #TODO: finish

    sln = property(get_sln, set_sln, del_sln)
    kid = property(get_kid, set_kid, del_kid)
    key = property(get_key, set_key, del_key)