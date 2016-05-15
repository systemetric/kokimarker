#!/usr/bin/env python

"""
libkoki marker validation script
"""

from __future__ import print_function

import cairo
import cv
import os.path

from pykoki import CameraParams, Point2Df, Point2Di, PyKoki
import kokimarker

NUM_MARKERS = 200

SURFACE_WIDTH = 1024
MARKER_WIDTH = 1000
MARKER_OFFSET = (SURFACE_WIDTH - MARKER_WIDTH) / 2

OUT_DIR = 'test_markers'

def cairo_surface(width, height):
    """Create a configured Cairo surface"""
    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width, height)
    return surface


def cairo_context(surface):
    """Configure a Cairo surface and produce a context"""
    context = cairo.Context(surface)

    # Set white background
    white = 1
    context.set_source_rgb(white, white, white)
    context.rectangle(0, 0, surface.get_width(), surface.get_height())
    context.fill()

    return context


def generate_marker(num):
    surface = cairo_surface(SURFACE_WIDTH, SURFACE_WIDTH)
    context = cairo_context(surface)

    marker = kokimarker.Marker(num)

    marker.render(context, MARKER_WIDTH, MARKER_OFFSET, MARKER_OFFSET,
                  font_size = 15)

    filename = os.path.join(OUT_DIR, "{0}.png".format(num))
    surface.write_to_png(filename)

    return filename

def read_number(filename, koki):
    img = cv.LoadImage(filename, cv.CV_LOAD_IMAGE_GRAYSCALE)
    assert img, "Failed to load image at {0}".format(filename)

    params = CameraParams(Point2Df( img.width/2, img.height/2 ),
                          Point2Df(571, 571),
                          Point2Di( img.width, img.height ))

    markers = koki.find_markers(img, 0.1, params)

    assert len(markers) < 2, "Found too many ({0}) markers in {1}".format(len(markers), filename)

    if len(markers):
        marker = markers[0]
        return marker.code
    else:
        return -1

def check_marker(num, koki):
    filename = generate_marker(num)
    found_num = read_number(filename, koki)

    return found_num == num

def main():
    if not os.path.exists(OUT_DIR):
        os.mkdir(OUT_DIR)


    koki = PyKoki()

    bad_markers = []

    for num in range(NUM_MARKERS):
        if not check_marker(num, koki):
            bad_markers.append(num)

    if bad_markers:
        bad_markers_str = ', '.join(map(str, bad_markers))
        print("Identified the following bad markers: {0}".format(bad_markers_str))
        exit(1)

if __name__ == '__main__':
    main()
