
class KeyItem():
    def __init__(self):
        self._sln = 0

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

    sln = property(get_sln, set_sln, del_sln)