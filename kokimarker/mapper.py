"""Routines for encoding/decoding marker numbers about code holes

When rendered onto a marker, some numbers look too much like other
numbers.  Therefore, libkoki does not use some marker numbers.  To
maintain library usability, marker numbers are shifted around these
gaps.

Definitions:
 * User-friendly code: The marker number that the user specifies.
 * Marker code: The number that is actually found in the grid of a
                marker.
"""

# The codes that are not used
bad_codes = [ 2, 3, 8, 9, 11, 13, 17, 19, 34, 42, 45, 46, 48, 51, 79,
              95, 96, 114, 126, 127, 159, 160, 178, 198, 200, 208,
              255 ]

def gen_forwards_table():
    """Returns a dict mapping marker codes to user-friendly codes.

    Returns a dict with keys 0-255.

      keys: Marker code
    values: User-friendly code -- unless the key is an invalid marker
    code (a hole), in which case the value is -1.
    """

    table = {}
    count = 0
    for i in range(256):
        if not i in bad_codes:
            table[i] = count
            count += 1
        else:
            table[i] = -1
    return table


def gen_reverse_table(fwd_table):
    """Returns a dict mapping user friendly codes to marker codes.

      keys: User-friendly codes.
    values: Marker codes.
    """

    rev = {}

    for marker_code, user_friendly in fwd_table.iteritems():
        if user_friendly != -1:
            rev[user_friendly] = marker_code

    return rev


# FORWARD[marker code] = user-friendly code
FORWARD = gen_forwards_table()

# REVERSE[user-friendly code] = marker code
REVERSE = gen_reverse_table( FORWARD )

def marker_code_to_user_friendly(marker_code):
    return FORWARD[marker_code]

def user_friendly_to_marker_code(user_friendly):
    return REVERSE[user_friendly]
