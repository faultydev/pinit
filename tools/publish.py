#!/bin/python3

import os
import shutil
import stat
import subprocess


def run_command(args: str):
    p = subprocess.Popen(args=args,
                         stdout=subprocess.PIPE)
    text = p.stdout.read()
    retcode = p.wait()
    return (retcode, text)


if not os.path.exists('src/'):
    print('could not find ./src/')
    exit(1)

if not os.path.exists('dist'):
    os.mkdir('dist')

shutil.copyfile('./src/main.py', './dist/pinit')
githashtext = run_command(
    ['git', 'log', '-n 1', '--pretty=format:"%H"'])[1].decode('UTF-8')

pinit_content = ""
with open('./dist/pinit', 'r') as rf:
    pinit_content += rf.read()
    rf.close()

pinit_content = pinit_content.replace("\"<VERSION>\"", githashtext)

with open('./dist/pinit', 'w') as wf:
    wf.write(pinit_content)
    wf.close()

os.chmod('./dist/pinit', stat.S_IRWXU | stat.S_IXOTH)

shutil.rmtree('./dist/templates')
shutil.copytree('./src/templates', './dist/templates')
