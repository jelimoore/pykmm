import unittest

from pykmm.kmm import KeyItem

class TestKeyItem(unittest.TestCase):
    def setUp(self):
        """Test setup."""
        self._keyitem = KeyItem()

    def tearDown(self):
        """Tear down."""
        del self._keyitem

    def sln_tests(self):
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