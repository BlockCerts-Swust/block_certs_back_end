import time

class FlakeIdProvider():
    def __init__(self, machineId):
        self.shiftedMachineId = (0x0000FFFFFFFFFFFF & machineId) << 16

    def max_sequence(self):
        return 65536

    def encode_as_string(self, time, sequence):
        s  = ""
        mm = self.encode_as_byte(time, sequence)
        for m in mm:
            s = s+self.left_pad(hex(int(m, 2)))
        return s

    def left_pad(self, bb):
        countIDdata = str(bb).replace("0x","")
        if len(countIDdata) < 16:  # 序列号不够5位的在前面补0
            length = len(countIDdata)
            s = "0" * (16 - length)
            countIDdata = s + countIDdata
        return countIDdata

    def encode_as_byte(self, time, sequence):
        buffer = []
        buffer.append(bin(time))
        rest = self.shiftedMachineId | (0x0000FFFF & sequence)
        buffer.append(bin(rest))
        return buffer


    def encode_as_long(self, time, sequence):
        print("Long value not supported")


class WsidGenerator:
    def __init__(self, logo=None):
        self.WSID_LOGO = logo
        self.DEFAULT_WSID_SEPARATOR = "_"
        self.DEFAULT_WSID_START = "wsid"
        self.SEQUENCE = 1
        self.LAST_TIMESTAMP = int(time.time() * 1000)
        self.FlakeIdProvider = FlakeIdProvider(self.get_mac_int())
        self.maxSequence = self.FlakeIdProvider.max_sequence()

    def get_string_wsid(self):
        current_time_stamp = int(round(time.time() * 1000))
        bb = self.FlakeIdProvider.encode_as_string(current_time_stamp, self.SEQUENCE+1)
        if self.WSID_LOGO is None:
            wsid = self.DEFAULT_WSID_START + self.DEFAULT_WSID_SEPARATOR + bb
        else:
            wsid = self.WSID_LOGO + self.DEFAULT_WSID_SEPARATOR + self.DEFAULT_WSID_START + self.DEFAULT_WSID_SEPARATOR + bb
        return wsid

    def get_mac_int(self):
        import uuid
        node = uuid.getnode()
        return node