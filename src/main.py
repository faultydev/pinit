#!/bin/python3

import argparse
import os
from posixpath import basename

pyspath = os.path.dirname(os.path.realpath(__file__))
templates_path = os.environ.get('TEMPLATE_DIR') or pyspath + '/templates/'


def __touch(fname, times=None):
    fhandle = open(fname, 'a')
    try:
        os.utime(fname, times)
    finally:
        fhandle.close()


def _get_templates():
    arr = []
    for root, path, files in os.walk(pyspath + '/templates'):
        for f in files:
            if f.endswith('.tmpl.txt'):
                arr.append(f.split('.tmpl')[0])
    return arr


def _fetch_template(template_name):
    def tmplpath(tmpl_name): return templates_path + tmpl_name + '.tmpl.txt'
    if not os.path.exists(tmplpath(template_name)):
        raise Exception('Template not found.')
    fstr = ""
    with open(tmplpath(template_name), 'r') as tm:
        fstr += tm.read()
    return fstr


def compose_template(templates=None):
    if templates is None:
        templates = ['_']
    tmpl_str = ""
    for tmpl in templates:
        tmpl_str += _fetch_template(tmpl)
        tmpl_str += '\n'
    return tmpl_str


def carve_template(tmpl_str: str):
    """
        MAKE SURE THIS IS RAN INSIDE THE PROJECT DIR
    """
    lines = tmpl_str.splitlines()
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
    argp = argparse.ArgumentParser(
        description="Initialize and manage projects",
        prog="pinit",
        # epilog="pinit is MIT licensed."
    )

    argp.add_argument(
        '-v', '--version',
        action='store_true',
        default=False,
        help="Displays the version"
    )

    argp.add_argument(
        '-n', '--name',
        type=str,
        dest='pname',
        default=str(basename(os.getcwd())),
        help="the project name (default's to basename of cwd)"
    )

    argp.add_argument(
        '-t', '--type',
        type=str,
        dest='type',
        default='_',
        help="choose a type of project ({})".format(
            ", ".join(_get_templates())
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
    origin_dir = os.getcwd()

    if args.version:
        print('You\'re using pinit @ commit: ' + "<VERSION>")
        return

    if args.pname != basename(origin_dir):
        os.mkdir(args.pname)
        os.chdir(args.pname)

    if args.type:
        if args.type == '_':
            composed = compose_template()
        else:
            composed = compose_template(['_', args.type])

    if args.gitignore:
        for gif in args.gitignore:
            composed += 'ignore: ' + gif + '\n'

    os.system('git init --quiet')

    if args.gitRemote != '':
        os.system('git remote add origin {}'.format(args.gitRemote))

    carve_template(composed)


if __name__ == "__main__":
    try:
        main()
    finally:
        pass
