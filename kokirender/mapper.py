"""Routines for encoding/decoding marker numbers about code holes

When rendered onto a marker, some numbers look too much like other
numbers.  Therefore, libkoki does not use some marker numbers.  To
maintain library usability, marker numbers are shifted around these
gaps.

Definitions:
 * User-friendly code: The marker number that the user specifies.
 * Mapped code: A code that has been shifted around the gaps.
"""

# The codes that are not used
bad_codes = [ 2, 3, 8, 9, 11, 13, 17, 19, 34, 42, 45, 46, 48, 51, 79,
              95, 96, 114, 126, 127, 159, 160, 178, 198, 200, 208,
              255 ]

def gen_forwards_table():
    """Return a dict that translates a user-friendly marker into a
    mapped code."""
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
    """Return a dict that translate a mapped code into a
    user-friendly code."""
    rev = {}
    items = fwd_table.items()

    for i in items:
        if i[1] != -1:
            rev[i[1]] = i[0]

    return rev

