"""
websocket - WebSocket client library for Python

Copyright (C) 2010 Hiroki Ohtani(liris)

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor,
    Boston, MA  02110-1335  USA

"""
import array
import struct
import os
from ._exceptions import *
from ._utils import validate_utf8

try:
    # If wsaccel is available we use compiled routines to mask data.
    from wsaccel.xormask import XorMaskerSimple

    def _mask(_m, _d):
        return XorMaskerSimple(_m).process(_d)

except ImportError:
    # wsaccel is not available, we rely on python implementations.
    def _mask(_m, _d):
        for i in range(len(_d)):
            _d[i] ^= _m[i % 4]

        return _d.tostring()

# closing frame status codes.
STATUS_NORMAL = 1000
STATUS_GOING_AWAY = 1001
STATUS_PROTOCOL_ERROR = 1002
STATUS_UNSUPPORTED_DATA_TYPE = 1003
STATUS_STATUS_NOT_AVAILABLE = 1005
STATUS_ABNORMAL_CLOSED = 1006
STATUS_INVALID_PAYLOAD = 1007
STATUS_POLICY_VIOLATION = 1008
STATUS_MESSAGE_TOO_BIG = 1009
STATUS_INVALID_EXTENSION = 1010
STATUS_UNEXPECTED_CONDITION = 1011
STATUS_TLS_HANDSHAKE_ERROR = 1015

VALID_CLOSE_STATUS = (
    STATUS_NORMAL,
    STATUS_GOING_AWAY,
    STATUS_PROTOCOL_ERROR,
    STATUS_UNSUPPORTED_DATA_TYPE,
    STATUS_INVALID_PAYLOAD,
    STATUS_POLICY_VIOLATION,
    STATUS_MESSAGE_TOO_BIG,
    STATUS_INVALID_EXTENSION,
    STATUS_UNEXPECTED_CONDITION,
    )


class ABNF(object):
    """
    ABNF frame class.
    see http://tools.ietf.org/html/rfc5234
    and http://tools.ietf.org/html/rfc6455#section-5.2
    """

    # operation code values.
    OPCODE_CONT = 0x0
    OPCODE_TEXT = 0x1
    OPCODE_BINARY = 0x2
    OPCODE_CLOSE = 0x8
    OPCODE_PING = 0x9
    OPCODE_PONG = 0xa

    # available operation code value tuple
    OPCODES = (OPCODE_CONT, OPCODE_TEXT, OPCODE_BINARY, OPCODE_CLOSE,
                OPCODE_PING, OPCODE_PONG)

    # opcode human readable string
    OPCODE_MAP = {
        OPCODE_CONT: "cont",
        OPCODE_TEXT: "text",
        OPCODE_BINARY: "binary",
        OPCODE_CLOSE: "close",
        OPCODE_PING: "ping",
        OPCODE_PONG: "pong"
        }

    # data length threshold.
    LENGTH_7 = 0x7e
    LENGTH_16 = 1 << 16
    LENGTH_63 = 1 << 63

    def __init__(self, fin=0, rsv1=0, rsv2=0, rsv3=0,
                 opcode=OPCODE_TEXT, mask=1, data=""):
        """
        Constructor for ABNF.
        please check RFC for arguments.
        """
        self.fin = fin
        self.rsv1 = rsv1
        self.rsv2 = rsv2
        self.rsv3 = rsv3
        self.opcode = opcode
        self.mask = mask
        if data is None:
            data = ""
        self.data = data
        self.get_mask_key = os.urandom

    def validate(self, skip_utf8_validation=False):
        """
        validate the ABNF frame.
        skip_utf8_validation: skip utf8 validation.
        """
        if self.rsv1 or self.rsv2 or self.rsv3:
            raise WebSocketProtocolException("rsv is not implemented, yet")

        if self.opcode not in ABNF.OPCODES:
            raise WebSocketProtocolException("Invalid opcode %r", self.opcode)

        if self.opcode == ABNF.OPCODE_PING and not self.fin:
            raise WebSocketProtocolException("Invalid ping frame.")

        if self.opcode == ABNF.OPCODE_CLOSE:
            l = len(self.data)
            if not l:
                return
            if l == 1 or l >= 126:
                raise WebSocketProtocolException("Invalid close frame.")
            if l > 2 and not skip_utf8_validation and not validate_utf8(self.data[2:]):
                raise WebSocketProtocolException("Invalid close frame.")

            code = 256 * ord(self.data[0:1][0]) + ord(self.data[1:2][0])  # ord(bs[0])
            if not self._is_valid_close_status(code):
                raise WebSocketProtocolException("Invalid close opcode.")

    def _is_valid_close_status(self, code):
        return code in VALID_CLOSE_STATUS or (3000 <= code < 5000)

    def __str__(self):
        return "fin=" + str(self.fin) \
                + " opcode=" + str(self.opcode) \
                + " data=" + str(self.data)

    @staticmethod
    def create_frame(data, opcode, fin=1):
        """
        create frame to send text, binary and other data.

        data: data to send. This is string value(byte array).
            if opcode is OPCODE_TEXT and this value is unicode,
            data value is converted into unicode string, automatically.

        opcode: operation code. please see OPCODE_XXX.

        fin: fin flag. if set to 0, create continue fragmentation.
        """
        if opcode == ABNF.OPCODE_TEXT and isinstance(data, str):
            data = data.encode("utf-8")
        # mask must be set if send data from client
        return ABNF(fin, 0, 0, 0, opcode, 1, data)

    def format(self):
        """
        format this object to string(byte array) to send data to server.
        """
        if any(x not in (0, 1) for x in [self.fin, self.rsv1, self.rsv2, self.rsv3]):
            raise ValueError("not 0 or 1")
        if self.opcode not in ABNF.OPCODES:
            raise ValueError("Invalid OPCODE")
        length = len(self.data)
        if length >= ABNF.LENGTH_63:
            raise ValueError("data is too long")

        frame_header = chr(self.fin << 7
                           | self.rsv1 << 6 | self.rsv2 << 5 | self.rsv3 << 4
                           | self.opcode)
        if length < ABNF.LENGTH_7:
            frame_header += chr(self.mask << 7 | length)
            frame_header = b"%s" % frame_header
        elif length < ABNF.LENGTH_16:
            frame_header += chr(self.mask << 7 | 0x7e)
            frame_header = b"%s" % frame_header
            frame_header += struct.pack("!H", length)
        else:
            frame_header += chr(self.mask << 7 | 0x7f)
            frame_header = b"%s" % frame_header
            frame_header += struct.pack("!Q", length)

        if not self.mask:
            return frame_header + self.data
        else:
            mask_key = self.get_mask_key(4)
            return frame_header + self._get_masked(mask_key)

    def _get_masked(self, mask_key):
        s = ABNF.mask(mask_key, self.data)

        if isinstance(mask_key, str):
            mask_key = mask_key.encode('utf-8')

        return mask_key + s

    @staticmethod
    def mask(mask_key, data):
        """
        mask or unmask data. Just do xor for each byte

        mask_key: 4 byte string(byte).

        data: data to mask/unmask.
        """
        if data is None:
            data = ""

        if isinstance(mask_key, str):
            mask_key = b"%s" % mask_key

        if isinstance(data, str):
            data = b"%s" % data

        _m = array.array("B", mask_key)
        _d = array.array("B", data)
        return _mask(_m, _d)


class frame_buffer(object):
    _HEADER_MASK_INDEX = 5
    _HEADER_LENGHT_INDEX = 6

    def __init__(self, recv_fn, skip_utf8_validation):
        self.recv = recv_fn
        self.skip_utf8_validation = skip_utf8_validation
        # Buffers over the packets from the layer beneath until desired amount
        # bytes of bytes are received.
        self.recv_buffer = []
        self.clear()

    def clear(self):
        self.header = None
        self.length = None
        self.mask = None

    def has_received_header(self):
        return self.header is None

    def recv_header(self):
        header = self.recv_strict(2)
        b1 = header[0]

        b1 = ord(b1)

        fin = b1 >> 7 & 1
        rsv1 = b1 >> 6 & 1
        rsv2 = b1 >> 5 & 1
        rsv3 = b1 >> 4 & 1
        opcode = b1 & 0xf
        b2 = header[1]

        b2 = ord(b2)

        has_mask = b2 >> 7 & 1
        length_bits = b2 & 0x7f

        self.header = (fin, rsv1, rsv2, rsv3, opcode, has_mask, length_bits)

    def has_mask(self):
        if not self.header:
            return False
        return self.header[frame_buffer._HEADER_MASK_INDEX]

    def has_received_length(self):
        return self.length is None

    def recv_length(self):
        bits = self.header[frame_buffer._HEADER_LENGHT_INDEX]
        length_bits = bits & 0x7f
        if length_bits == 0x7e:
            v = self.recv_strict(2)
            self.length = struct.unpack("!H", v)[0]
        elif length_bits == 0x7f:
            v = self.recv_strict(8)
            self.length = struct.unpack("!Q", v)[0]
        else:
            self.length = length_bits

    def has_received_mask(self):
        return self.mask is None

    def recv_mask(self):
        self.mask = self.recv_strict(4) if self.has_mask() else ""

    def recv_frame(self):
        # Header
        if self.has_received_header():
            self.recv_header()
        (fin, rsv1, rsv2, rsv3, opcode, has_mask, _) = self.header

        # Frame length
        if self.has_received_length():
            self.recv_length()
        length = self.length

        # Mask
        if self.has_received_mask():
            self.recv_mask()
        mask = self.mask

        # Payload
        payload = self.recv_strict(length)
        if has_mask:
            payload = ABNF.mask(mask, payload)

        # Reset for next frame
        self.clear()

        frame = ABNF(fin, rsv1, rsv2, rsv3, opcode, has_mask, payload)
        frame.validate(self.skip_utf8_validation)

        return frame

    def recv_strict(self, bufsize):
        shortage = bufsize - sum(len(x) for x in self.recv_buffer)
        while shortage > 0:
            # Limit buffer size that we pass to socket.recv() to avoid
            # fragmenting the heap -- the number of bytes recv() actually
            # reads is limited by socket buffer and is relatively small,
            # yet passing large numbers repeatedly causes lots of large
            # buffers allocated and then shrunk, which results in fragmentation.
            bytes = self.recv(min(16384, shortage))
            self.recv_buffer.append(bytes)
            shortage -= len(bytes)

        unified = b"".join(self.recv_buffer)

        if shortage == 0:
            self.recv_buffer = []
            return unified
        else:
            self.recv_buffer = [unified[bufsize:]]
            return unified[:bufsize]


class continuous_frame(object):
    def __init__(self, fire_cont_frame, skip_utf8_validation):
        self.fire_cont_frame = fire_cont_frame
        self.skip_utf8_validation = skip_utf8_validation
        self.cont_data = None
        self.recving_frames = None

    def validate(self, frame):
        if not self.recving_frames and frame.opcode == ABNF.OPCODE_CONT:
            raise WebSocketProtocolException("Illegal frame")
        if self.recving_frames and frame.opcode in (ABNF.OPCODE_TEXT, ABNF.OPCODE_BINARY):
            raise WebSocketProtocolException("Illegal frame")

    def add(self, frame):
        if self.cont_data:
            self.cont_data[1] += frame.data
        else:
            if frame.opcode in (ABNF.OPCODE_TEXT, ABNF.OPCODE_BINARY):
                self.recving_frames = frame.opcode
            self.cont_data = [frame.opcode, frame.data]

        if frame.fin:
            self.recving_frames = None

    def is_fire(self, frame):
        return frame.fin or self.fire_cont_frame

    def extract(self, frame):
        data = self.cont_data
        self.cont_data = None
        frame.data = data[1]
        if not self.fire_cont_frame and data[0] == ABNF.OPCODE_TEXT and not self.skip_utf8_validation and not validate_utf8(frame.data):
            raise WebSocketPayloadException("cannot decode: " + repr(frame.data))

        return [data[0], frame]
