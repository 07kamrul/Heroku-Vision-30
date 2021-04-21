#!/media/cts/499ce1c2-ad39-47ba-a77f-e16984e6953d/home/cts/Kamrul Hasan/Practies/Heroku-Vision-30/vision/bin/python

# $Id: rst2xetex.py 7847 2015-03-17 17:30:47Z milde $
# Author: Guenter Milde
# Copyright: This module has been placed in the public domain.

"""
A minimal front end to the Docutils Publisher, producing Lua/XeLaTeX code.
"""

try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except:
    pass

from docutils.core import publish_cmdline

description = ('Generates LaTeX documents from standalone reStructuredText '
               'sources for compilation with the Unicode-aware TeX variants '
               'XeLaTeX or LuaLaTeX. '
               'Reads from <source> (default is stdin) and writes to '
               '<destination> (default is stdout).  See '
               '<http://docutils.sourceforge.net/docs/user/latex.html> for '
               'the full reference.')

publish_cmdline(writer_name='xetex', description=description)
