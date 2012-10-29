#!/usr/bin/env python
from distutils.core import setup

setup( name = "kokimarker",
       version = "0.0.1",
       py_modules = [ "kokimarker" ],
       packages = ["kokimarker"],
       scripts = [ "koki-marker-gen" ],

       maintainer = "Rob Spanton",
       maintainer_email = "rspanton@zepler.net",
       url = "https://www.studentrobotics.org/trac/wiki/libkoki",
       )
