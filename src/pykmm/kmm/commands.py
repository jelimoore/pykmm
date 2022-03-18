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

class InventoryCommand():
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