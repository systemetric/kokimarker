import cairo
import code_table
import CrcMoose
import hamming
import mapper
import math

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
    return map(hamming.encode, l)

def code_grid(code):
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

class Marker(object):
    "A libkoki marker"
    VERSION = "v0.5"

    def __init__(self, code):
        self.code = code
        self.desc = ""

    # def __repr__(self):
    #     sys.stdout.write("# # # # # # # # # #\n")
    #     sys.stdout.write("# # # # # # # # # #\n")
    #     for i in range(6):
    #         sys.stdout.write("# # ")
    #         for j in range(6):
    #             if grid[i][j] == 1:
    #                 sys.stdout.write("# ")
    #             else:
    #                 sys.stdout.write("  ")
    #         sys.stdout.write("# #\n")
    #     sys.stdout.write("# # # # # # # # # #\n")
    #     sys.stdout.write("# # # # # # # # # #\n")


    def render( self, surface,
                overall_width, offset_x, offset_y,
                desc="", show_text=1 ):

        fwd = mapper.gen_forwards_table()
        rev = mapper.gen_reverse_table(fwd)

        grid = code_grid(add_crc(rev[ self.code ]))

        marker_width = overall_width * (10.0/12.0)
        cell_width = marker_width / 10
        cell_grid_offset_x = cell_width * 2
        cell_grid_offset_y = cell_width * 2

        cr = cairo.Context(surface)

        # draw outline
        cr.set_line_width(1)
        grey = 0.7
        cr.set_source_rgb(grey, grey, grey)
        cr.rectangle(offset_x, offset_y, overall_width, overall_width)
        cr.stroke()

        # draw black border
        cr.set_source_rgb(0, 0, 0)
        cr.rectangle(offset_x + cell_width,
                     offset_y + cell_width,
                     marker_width, marker_width)
        cr.fill()

        # draw white grid background (i.e. zero grid)
        cr.set_source_rgb(1, 1, 1)
        cr.rectangle(offset_x + cell_width + cell_width * 2,
                     offset_y + cell_width + cell_width * 2,
                     marker_width * 0.6, marker_width * 0.6)
        cr.fill()

        #draw cells
        cr.set_source_rgb(0, 0, 0)
        for row in range(6):
            for col in range(6):

                if grid[row][col] == 1:
                    #draw the 1 bit
                    cr.rectangle(offset_x + cell_width + cell_width * 2 + col * cell_width,
                                 offset_y + cell_width + cell_width * 2 + row * cell_width,
                                 marker_width * 0.1, marker_width * 0.1)

                cr.fill()

        # write on marker
        if show_text:

            font_size = 6
            grey = 0.5

            cr.select_font_face('Sans')
            cr.set_font_size(font_size)
            cr.set_source_rgb(grey, grey, grey)

            cr.move_to(offset_x + cell_width + font_size, offset_y + cell_width + marker_width - font_size)
            cr.show_text('libkoki marker #%d (%s)   %s' % (self.code, self.VERSION, self.desc))

        # put dot in top left
        cr.new_sub_path()
        grey = 0.2
        cr.set_source_rgb(grey, grey, grey)
        cr.arc(offset_x + cell_width + cell_width,
               offset_y + cell_width + cell_width,
               cell_width/8, 0, 2 * math.pi)
        cr.fill()
