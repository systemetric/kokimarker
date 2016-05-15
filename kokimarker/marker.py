import cairo
import coder
import mapper
import math

class Marker(object):
    "A libkoki marker"
    VERSION = "v0.5"

    def __init__(self, code):
        self.code = code
        self.grid = coder.user_code_grid( self.code )

    def text_grid(self):
        "Return a text representation of the marker's grid"

        s = "# # # # # # # # # #\n" * 2

        for i in range(6):
            s += "# # "
            for j in range(6):
                if self.grid[i][j] == 1:
                    s += "# "
                else:
                    s += "  "
            s += "# #\n"

        s += "# # # # # # # # # #\n" * 2
        return s

    def render( self, cr,
                overall_width, offset_x, offset_y,
                desc="", show_text=True, font_size=3,
                corner_dot = True,
                outline = True ):
        """
        Render the marker onto the given cairo context.

        :param cr: A cairo context.
        :param overall_width: The overall width to render the marker at.
        :param offset_x: The x-offset within the context to render the
                         marker at.
        :param offset_y: The y-offset within the context to render the
                         marker at.
        :param desc: A human-readable description of the marker to show.
        :param show_text: Whether or not to show information about the
                          the marker, including the description.
        :param font_size: The size of font to use for the information and
                          description.
        :param corner_dot: Whether or not to render a dot in the top left
                           corner of the marker.
        :param outline: Whether or not to draw an outline around the marker.
        """

        marker_width = overall_width * (10.0/12.0)
        cell_width = marker_width / 10
        cell_grid_offset_x = cell_width * 2
        cell_grid_offset_y = cell_width * 2

        # draw outline
        if outline:
            cr.set_line_width( overall_width * 0.005 )
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

        #draw cells
        cr.set_source_rgb(1, 1, 1)
        for row in range(6):
            for col in range(6):
                if self.grid[row][col] == 0:
                    # Set this cell to be white
                    cr.rectangle(offset_x + cell_width + cell_width * 2 + col * cell_width,
                                 offset_y + cell_width + cell_width * 2 + row * cell_width,
                                 marker_width * 0.1, marker_width * 0.1)

        cr.fill()

        # write on marker
        if show_text:

            grey = 0.5

            cr.select_font_face('Sans')
            cr.set_font_size(font_size)
            cr.set_source_rgb(grey, grey, grey)

            cr.move_to(offset_x + cell_width + font_size, offset_y + cell_width + marker_width - font_size)
            cr.show_text('libkoki marker #%d (%s)   %s' % (self.code, self.VERSION, desc))

        # put dot in top left
        if corner_dot:
            cr.new_sub_path()
            grey = 0.2
            cr.set_source_rgb(grey, grey, grey)
            cr.arc(offset_x + cell_width + cell_width,
                   offset_y + cell_width + cell_width,
                   cell_width/8, 0, 2 * math.pi)
            cr.fill()
