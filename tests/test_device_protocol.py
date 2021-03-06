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

import unittest

from pykmm.kmm.items import *

class TestKeyItem(unittest.TestCase):
    def setUp(self):
        """Test setup."""
        self._keyitem = KeyItem()

    def tearDown(self):
        """Tear down."""
        del self._keyitem

    def test_sln(self):
        """Test all SLN get, set, and invalid paths"""

        # set the SLN then get it
        self._keyitem.sln = 0x1234
        self.assertEqual(self._keyitem.sln, 0x1234)

        self._keyitem.sln = 156
        self.assertEqual(self._keyitem.sln, 156)

        #test with invalid types
        with self.assertRaises(TypeError):
            self._keyitem.sln = "beans"

        with self.assertRaises(TypeError):
            self._keyitem.sln = [0x0, 0x1, 0x2, 0x3]

        #test with invalid bounds
        with self.assertRaises(ValueError):
            self._keyitem.sln = -256

        with self.assertRaises(ValueError):
            self._keyitem.sln = 0xFFFFFF

if __name__ == '__main__':
    unittest.main()