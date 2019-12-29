import zigpy.types
from zigpy_cc.types import ParameterType


class BuffaloOptions:

    def __init__(self) -> None:
        self.startIndex = None
        self.length = None


class Buffalo:
    def __init__(self, buffer, position=0) -> None:
        self.position = position
        self.buffer = buffer

    def __len__(self) -> int:
        return len(self.buffer)

    def write_parameter(self, type, value, options):
        if type == ParameterType.UINT8:
            self.write(value)
        elif type == ParameterType.UINT16:
            self.write(value, 2)
        elif type == ParameterType.UINT32:
            self.write(value, 4)
        elif type == ParameterType.IEEEADDR:
            # self.write(int(value[10:], 16), 4)
            # self.write(int(value[2:10], 16), 4)
            for i in reversed(value):
                self.write(i)
        elif type == ParameterType.BUFFER:
            self.buffer += value
        elif type == ParameterType.LIST_UINT8:
            for v in value:
                self.write(v)
        elif type == ParameterType.LIST_UINT16:
            for v in value:
                self.write(v, 2)
        else:
            raise Exception('write not implemented', ParameterType(type))

    def write(self, value, length=1):
        self.buffer += value.to_bytes(length, "little")

    def read_parameter(self, type, options):
        if type == ParameterType.UINT8:
            res = self.read_int()
        elif type == ParameterType.UINT16:
            res = self.read_int(2)
        elif type == ParameterType.UINT32:
            res = self.read_int(4)
        elif type == ParameterType.IEEEADDR:
            # res = "0x" + self.read(8).hex()
            res = zigpy.types.EUI64(self.read(8))
        elif type == ParameterType.BUFFER:
            length = options.length
            res = self.read(length)
        else:
            # list types
            res = []
            if type == ParameterType.LIST_UINT8:
                for i in range(0, options.length):
                    res.append(self.read_int())
            elif type == ParameterType.LIST_UINT16:
                for i in range(0, options.length):
                    res.append(self.read_int(2))
            else:
                raise Exception('read not implemented', ParameterType(type))

        return res

    def read_int(self, length=1):
        return int.from_bytes(self.read(length), "little")

    def read(self, length=1):
        res = self.buffer[self.position: self.position + length]
        self.position += length
        return res
