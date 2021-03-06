# -*- coding: utf-8 -*-
"""
View for the Commandline UI

This module handles the main "sage-package" commandline utility, which
is also exposed as "sage --package".
"""


#*****************************************************************************
#       Copyright (C) 2016 Volker Braun <vbraun.name@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

import os
import sys
import logging
log = logging.getLogger()

# Note that argparse is not part of Python 2.6, so we bundle it
from sage_bootstrap.compat import argparse

from sage_bootstrap.app import Application


description = \
"""
Sage Bootstrap Library
"""


epilog = \
"""
The individual subcommands have their own detailed help, for example
run "sage --package config -h" to see the help on the config option.
"""


epilog_config = \
"""
Print the configuration

EXAMPLE:

    $ sage --package config
    Configuration:
    * log = info
    * interactive = True
"""


epilog_list = \
"""
Print a list of all available packages

EXAMPLE:

    $ sage --package list | sort
    4ti2
    arb
    atlas
    autotools
    [...]
    zn_poly

    $ sage --package list :standard: | sort
    arb
    atlas
    backports_ssl_match_hostname
    [...]
    zn_poly
"""


epilog_name = \
"""
Find the package name given a tarball filename
    
EXAMPLE:

    $ sage --package name pari-2.8-1564-gdeac36e.tar.gz
    pari
"""


epilog_tarball = \
"""
Find the tarball filename given a package name
    
EXAMPLE:

    $ sage --package tarball pari
    pari-2.8-1564-gdeac36e.tar.gz
"""


epilog_apropos = \
"""
Find up to 5 package names that are close to the given name

EXAMPLE:

    $ sage --package apropos python
    Did you mean: cython, ipython, python2, python3, patch?
"""
        

epilog_update = \
"""
Update a package. This modifies the Sage sources. 
    
EXAMPLE:

    $ sage --package update pari 2015 --url=http://localhost/pari/tarball.tgz
"""


epilog_update_latest = \
"""
Update a package to the latest version. This modifies the Sage sources. 
    
EXAMPLE:

    $ sage --package update-latest ipython
"""


epilog_download = \
"""
Download the tarball for a package and print the filename to stdout
    
EXAMPLE:

    $ sage --package download pari
    Using cached file /home/vbraun/Code/sage.git/upstream/pari-2.8-2044-g89b0f1e.tar.gz
    /home/vbraun/Code/sage.git/upstream/pari-2.8-2044-g89b0f1e.tar.gz
"""


epilog_upload = \
"""
Upload the tarball to the Sage mirror network (requires ssh key authentication)
    
EXAMPLE:

    $ sage --package upload pari
    Uploading /home/vbraun/Code/sage.git/upstream/pari-2.8-2044-g89b0f1e.tar.gz
"""


epilog_fix_checksum = \
"""
Fix the checksum of a package
    
EXAMPLE:

    $ sage --package fix-checksum pari
    Updating checksum of pari-2.8-2044-g89b0f1e.tar.gz
"""


def make_parser():
    """
    The main commandline argument parser
    """
    parser = argparse.ArgumentParser(
        description=description, epilog=epilog,
        prog='sage --package',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('--log', dest='log', default=None,
                        help='one of [DEBUG, INFO, ERROR, WARNING, CRITICAL]')
    subparsers = parser.add_subparsers(dest='subcommand')

    parser_config = subparsers.add_parser(
        'config', epilog=epilog_config,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='Print the configuration')

    parser_list = subparsers.add_parser(
        'list', epilog=epilog_list,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='Print a list of all available packages')
    parser_list.add_argument(
        'package_or_class_list',
        type=str, default=':all:', nargs='+',
        help='Package class like :all: (default) or :standard:')

    parser_name = subparsers.add_parser(
        'name', epilog=epilog_name,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='Find the package name given a tarball filename')
    parser_name.add_argument('tarball_filename', type=str, help='Tarball filename')

    parser_tarball = subparsers.add_parser(
        'tarball', epilog=epilog_tarball,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='Find the tarball filename given a package name')
    parser_tarball.add_argument('package_name', type=str, help='Package name')
    
    parser_apropos = subparsers.add_parser(
        'apropos', epilog=epilog_apropos,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='Find up to 5 package names that are close to the given name')
    parser_apropos.add_argument(
        'incorrect_name', type=str, 
        help='Fuzzy name to search for')

    parser_update = subparsers.add_parser(
        'update', epilog=epilog_update,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='Update a package. This modifies the Sage sources.')
    parser_update.add_argument(
        'package_name', type=str, help='Package name')
    parser_update.add_argument(
        'new_version', type=str, help='New version')
    parser_update.add_argument(
        '--url', type=str, default=None, help='Download URL')

    parser_update_latest = subparsers.add_parser(
        'update-latest', epilog=epilog_update_latest,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='Update a package to the latest version. This modifies the Sage sources.')
    parser_update_latest.add_argument(
        'package_name', type=str, help='Package name (:all: for all packages)')

    parser_download = subparsers.add_parser(
        'download', epilog=epilog_download,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='Download tarball')
    parser_download.add_argument(
        'package_or_class_list', type=str, nargs='+', help='Package name(s) or :type:')
    
    parser_upload = subparsers.add_parser(
        'upload', epilog=epilog_upload,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='Upload tarball to Sage mirrors')
    parser_upload.add_argument(
        'package_or_class_list', type=str, nargs='+', help='Package name(s) or :type:')
    
    parser_fix_checksum = subparsers.add_parser(
        'fix-checksum', epilog=epilog_fix_checksum,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='Fix the checksum of package.')
    parser_fix_checksum.add_argument(
        'package_or_class_list', nargs='+', type=str,
        help='Package name. Default: fix all packages.')
    
    return parser



def run():
    parser = make_parser()
    if len(sys.argv) == 1:
        parser.print_help()
        return
    args = parser.parse_args(sys.argv[1:])
    if args.log is not None:
        level = getattr(logging, args.log.upper())
        log.setLevel(level=level)
    log.debug('Commandline arguments: %s', args)
    app = Application()
    if args.subcommand == 'config':
        app.config()
    elif args.subcommand == 'list':
        app.list_multi(args.package_or_class_list)
    elif args.subcommand == 'name':
        app.name(args.tarball_filename)
    elif args.subcommand == 'tarball':
        app.tarball(args.package_name)
    elif args.subcommand == 'apropos':
        app.apropos(args.incorrect_name)
    elif args.subcommand == 'update':
        app.update(args.package_name, args.new_version, url=args.url)
    elif args.subcommand == 'update-latest':
        if args.package_name == ':all:':
            app.update_latest_all()
        else:
            app.update_latest(args.package_name)
    elif args.subcommand == 'download':
        app.download_multi(args.package_or_class_list)
    elif args.subcommand == 'upload':
        app.upload_multi(args.package_or_class_list)
    elif args.subcommand == 'fix-checksum':
        app.fix_checksum_multi(args.package_or_class_list)
    else:
        raise RuntimeError('unknown subcommand: {0}'.format(args))

        
if __name__ == '__main__':
    run()
