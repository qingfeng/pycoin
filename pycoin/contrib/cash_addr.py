# Copyright (c) 2017 Pieter Wuille
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Reference implementation for Cash addresses."""
from ..intbytes import int2byte

CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"

SIZE_MAP = {
    160: 0,
    192: 1,
    224: 2,
    256: 3,
    320: 4,
    384: 5,
    448: 6,
    512: 7
    }


def cash_polymod(values):
    """Internal function that computes the Cash checksum."""
    generator = [
        0x98f2bc8e61,
        0x79b76d99e2,
        0xf33e5fb3c4,
        0xae2eabe2a8,
        0x1e4f43e470
        ]
    chk = 1
    for value in values:
        top = chk >> 35
        #chk = (chk & 0x1ffffff) << 5 ^ value
        chk = ((chk & 0x07ffffffff) << 5) ^ value
        for i in range(5):
            chk ^= generator[i] if ((top >> i) & 1) else 0
    return chk ^ 1


def cash_hrp_expand(hrp):
    """Expand the HRP into values for checksum computation."""
    #return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]
    return [ord(x) & 0x1f for x in hrp] + [0]


def cash_verify_checksum(hrp, data):
    """Verify a checksum given HRP and converted data characters."""
    checksum = cash_create_checksum(hrp, data[:-8])
    return cash_polymod(cash_hrp_expand(hrp) + data) == 0


def cash_create_checksum(hrp, data):
    """Compute the checksum values given HRP and data."""
    values = cash_hrp_expand(hrp) + data
    polymod = cash_polymod(values + [0, 0, 0, 0, 0, 0, 0, 0])
    return [(polymod >> 5 * (7 - i)) & 31 for i in range(8)]


def cash_encode(hrp, data, infix=':'):
    """Compute a Cash string given HRP and data values."""
    combined = data + cash_create_checksum(hrp, data)
    return hrp + infix + ''.join([CHARSET[d] for d in combined])


def cash_decode(bech, infix=':'):
    """Validate a Cash string, and determine HRP and data."""
    if ((any(ord(x) < 33 or ord(x) > 126 for x in bech)) or
            (bech.lower() != bech and bech.upper() != bech)):
        return (None, None)
    bech = bech.lower()
    pos = bech.rfind(infix)
    if pos < 1 or pos + 7 > len(bech) or len(bech) > 90:
        return (None, None)
    if not all(x in CHARSET for x in bech[pos+len(infix):]):
        return (None, None)
    hrp = bech[:pos]
    data = [CHARSET.find(x) for x in bech[pos+len(infix):]]
    if not cash_verify_checksum(hrp, data):
        return (None, None)
    return (hrp, data[:-8])


def convertbits(data, frombits, tobits, pad=True):
    """General power-of-2 base conversion."""
    acc = 0
    bits = 0
    ret = []
    maxv = (1 << tobits) - 1
    max_acc = (1 << (frombits + tobits - 1)) - 1
    for value in data:
        if value < 0 or (value >> frombits):
            return None
        acc = ((acc << frombits) | value) & max_acc
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)
    if pad:
        if bits:
            ret.append((acc << (tobits - bits)) & maxv)
    elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
        return None
    return ret

def pack_data(type, data):
    version_byte = type << 3
    encode_size = SIZE_MAP[len(data) * 8]
    version_byte |= encode_size
    return int2byte(version_byte) + data

def unpack_data(data):
    version_byte = data[0]
    type = (version_byte >> 3) & 0x1f
    hash_size = 20 + 4 * (version_byte & 0x03)

    if version_byte & 0x04:
        hash_size *= 2

    if len(data) != hash_size + 1:
        raise ValueError
    return type, data[1:]

def decode(hrp, addr):
    """Decode a cash address."""
    hrpgot, data = cash_decode(addr)
    if hrp is not None and hrpgot != hrp:
        raise TypeError
    decoded = convertbits(data, 5, 8, False)
    type, unpacked = unpack_data(decoded)
    return (hrpgot, type, unpacked)

def encode(hrp, type, hashdata):
    """Encode a code address."""
    data = pack_data(type, hashdata)
    ret = cash_encode(hrp, convertbits(data, 8, 5))
    assert decode(hrp, ret) is not (None, None)
    return ret
