def stringToByteList(stringIn):
    result = []
    if (len(stringIn) % 2 == 0):
        for i in range(0, len(stringIn), 2):
            result.append(int(stringIn[i:i+2], 16))
    else:
        raise ValueError("Input string is not even length")
    return result

def dataFormat(dataIn):
    if (isinstance(dataIn, int)):
        if (dataIn > 0xFF):
            raise ValueError("Input must be >0 <255")
        else:
            padding = 2
        return f"{dataIn:#0{padding}x}"
    elif (isinstance(dataIn, list)):
        dataString = ""
        for b in dataIn:
            dataString += dataFormat(b)
            dataString += ", "
        #cut the last ", " from the list
        dataString = dataString[-2]
        return dataString
