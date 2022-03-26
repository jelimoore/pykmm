# pykmm
A library to facilitate rekeying and key maintenance of P25 (TIA102) radios using Python, supporting KFDTool, KFD-AVR and DLI (OTAR).

Planned features:
- Communication with [KFDTool](https://github.com/kfdtool/kfdtool), [KFD-AVR](https://github.com/omahacommsys/kfdtool), and DLI/OTAR
- Support for encrypted frames, RSI, and MN
- 1:1 compatibility with KFDTool ekc files
- Implementation of all required and optional features from the TIA102.AACA and AACD specifications

## License
This project is licensed under the GNU GPLv2 license.

## Using
You can run the example app using the kfdpy.py file in the root of this repository. Make sure to set the options in the file header (serial port, etc).