#!/usr/bin/env python

'''
Created on Apr 29, 2012
'''

from __future__ import division

__author__ = "Shyue Ping Ong"
__version__ = "0.1"
__maintainer__ = "Shyue Ping Ong"
__email__ = "shyue@mit.edu"
__date__ = "Apr 29, 2012"

import os
import subprocess
import glob
import shlex
import shutil

sphinxcmd = "sphinx-apidoc -o . -f ../pyhull"
args = shlex.split(sphinxcmd)
p = subprocess.Popen(args)
output = p.communicate()[0]

for f in glob.glob("*.rst"):
    if f.endswith('tests.rst'):
        os.remove(f)
    elif f.startswith('pyhull') and f.endswith('rst'):
        newoutput = []
        suboutput = []
        subpackage = False
        with open(f, 'r') as fid:
            for line in fid:
                if line.strip() == "Subpackages":
                    subpackage = True
                if not subpackage and not line.strip().endswith("tests"):
                    newoutput.append(line)
                else:
                    if not line.strip().endswith("tests"):
                        suboutput.append(line)
                    if line.strip().startswith("pyhull") and not line.strip().endswith("tests"):
                        newoutput.extend(suboutput)
                        subpackage = False
                        suboutput = []


        with open(f, 'w') as fid:
            fid.write("".join(newoutput))

p = subprocess.Popen(["make", "html"])
output = p.communicate()[0]
