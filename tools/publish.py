#!/bin/python3

import os
import shutil
import stat

if not os.path.exists('src/'):
    print('could not find ./src/')
    exit(1)

if not os.path.exists('dist'):
    os.mkdir('dist')

shutil.copyfile('./src/main.py', './dist/pinit')
os.chmod('./dist/pinit', stat.S_IRWXU | stat.S_IXOTH)
shutil.copytree('./src/templates', './dist/templates')
