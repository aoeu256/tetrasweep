# Common colour constant things for writing coloured text
# Coded by Andy Friesen
# Copyright whenever.  All rights reserved.
#
# This source code may be used for any purpose, provided that
# the original author is never misrepresented in any way.
#
# There is no warranty, express or implied on the functionality, or
# suitability of this code for any purpose.

import ika
o = 0x00
x = 0xFF

colours = dict(
    [ (name, '#[%X]' % ika.RGB(*value))

        for name, value in
        (
            ('black',   (o, o, o)),
            ('blue',    (o, o, x)),
            ('green',   (o, x, o)),
            ('aqua',    (o, x, x)),
            ('red',     (x, o, o)),
            ('violet',  (x, o, x)),
            ('yellow',  (x, x, o)),
            ('white',   (x, x, x)),
        )
    ]
)

del o
del x
del ika