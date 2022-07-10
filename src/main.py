#!/bin/python3

from argparse import ArgumentParser
import os
from posixpath import basename

pyspath = os.path.dirname(os.path.realpath(__file__))


def __touch(fname, times=None):
    fhandle = open(fname, 'a')
    try:
        os.utime(fname, times)
    finally:
        fhandle.close()


def _getTemplates():
    arr = []
    for root, path, files in os.walk(pyspath + '/templates'):
        for f in files:
            if f.endswith('.tmpl.txt'):
                arr.append(f.split('.tmpl')[0])
    return arr


def _fetchTemplate(template_name):
    def tmplpath(tmpl_name): return pyspath + \
        '/templates/' + tmpl_name + '.tmpl.txt'
    if not os.path.exists(tmplpath(template_name)):
        raise Exception('Template not found.')
    fstr = ""
    with open(tmplpath(template_name), 'r') as tm:
        fstr += tm.read()
    return fstr


def composeTemplate(templates=['_']):
    tmplstr = ""
    for tmpl in templates:
        tmplstr += _fetchTemplate(tmpl)
        tmplstr += '\n'
    return tmplstr


def carveTemplate(tmplStr: str):
    """
        MAKE SURE THIS IS RAN INSIDE THE PROJECT DIR
    """
    lines = tmplStr.splitlines()
    for l in lines:
        if l.startswith('dir: '):
            os.mkdir(l.split('dir: ')[1])
        if l.startswith('file: '):
            __touch(l.split('file: ')[1])
        if l.startswith('ignore: '):
            with open('.gitignore', 'a+') as gif:
                try:
                    gif.write(l.split('ignore: ')[1] + '\n')
                finally:
                    gif.close()


def main():
    argp = ArgumentParser(
        description="Initialize and manage projects",
        prog="pinit",
        # epilog="pinit is MIT licensed."
    )

    argp.add_argument(
        '-n', '--name',
        help="the project name (default's to basename of cwd)",
        dest='pname',
        type=str,
        default=str(basename(os.getcwd()))
    )

    argp.add_argument(
        '-t', '--type',
        type=str,
        dest='type',
        default='_',
        help="choose a type of project ({})".format(
            ", ".join(_getTemplates())
        )
    )

    argp.add_argument(
        '-gi', '--gitignore',
        action='append',
        dest="gitignore",
        default=None,
        help="add folders to the git ignore"
    )

    argp.add_argument(
        '-gr', '--git-remote',
        type=str,
        dest='gitRemote',
        default='',
        help="add a remote when initializing the repo."
    )

    args = argp.parse_args()
    origindir = os.getcwd()

    if args.pname != basename(origindir):
        os.mkdir(args.pname)
        os.chdir(args.pname)

    if args.type:
        if args.type == '_':
            composed = composeTemplate()
        else:
            composed = composeTemplate(['_', args.type])

    if args.gitignore:
        for gif in args.gitignore:
            composed += 'ignore: ' + gif + '\n'

    os.system('git init')

    if args.gitRemote != '':
        os.system('git remote add origin {}'.format(args.gitRemote))

    carveTemplate(composed)


if __name__ == "__main__":
    try:
        main()
    finally:
        pass
