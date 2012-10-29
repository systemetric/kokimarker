"""Routines for encoding/decoding a marker number into the grid of
bits to be placed on a marker."""

import CrcMoose
import hamming
import mapper


def add_crc(marker_num):
    "Add the CRC to the given marker number"

    CRC12 = CrcMoose.CrcAlgorithm(
        name         = "CRC-12",
        width        = 12,
        polynomial   = (12, 11, 3, 2, 1, 0),
        seed         = 0,
        lsbFirst     = True,
        xorMask      = 0)

    marker_chr = chr(int((marker_num+1) % 256))
    crc = CRC12.calcString(marker_chr)

    code = (crc << 8) | marker_num
    return code

def code_to_lists(code):
    "Split the given code up into sections for hamming"
    output = []

    for i in range(5):
        l = []

        for j in range(4):
            mask = 0x1 << (i*4+j)
            tmp = code & mask
            bit = 1
            if (tmp == 0):
                bit = 0

            l.append(bit)

        output.append(l)

    return output

def encoded_lists(l):
    "Add hamming codes to all the items of the given list"
    return map(hamming.encode, l)

def code_grid(code):
    "Return the grid for the given (mapped) code"

    blocks = encoded_lists(code_to_lists(code))
    cell = 0

    grid = [[-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1]]

    for i in range(7):
        for j in range(5):
            grid[cell / 6][cell % 6] = blocks[j][i]
            cell = cell + 1

    return grid

def user_code_grid( usercode ):
    "Return the grid for the given user-friendly code"

    marker_code = mapper.user_friendly_to_marker_code( usercode )
    c = add_crc( marker_code )
    grid = code_grid(c)

    return grid
