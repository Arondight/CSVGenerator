#!/usr/bin/env python3
# encoding:utf8
# ==============================================================================
# Copyright (c) 2018 秦凡东 (Qin Fandong)
# ==============================================================================
# Usage: ./CSVGenerator.py -h
# ==============================================================================

import os
import sys
import string
import signal
import argparse
import random
import csv
import logging
from concurrent.futures import ProcessPoolExecutor

class CSVGenerator (object):
    def __init__ (self):
        self._parseargs ()
        self._sigbind ()

    def _parseargs (self):
        me = sys.argv[0]
        example = "Examples:\n\t%s %s\n\t%s %s\n\t%s %s\n\t%s %s" %(
                    me, "-d outdir -n 4096 -r 8192 -t int float str",
                    me, "-d -t int int",
                    me, "-f out.csv -r 65536 -t str int str float",
                    me, "-f -t str str")
        epilogstr = '--directory and --file are mutually exclusive.\n\n' + example
        parser = argparse.ArgumentParser (
                    formatter_class = argparse.RawTextHelpFormatter,
                    description = 'Generate random CSV files.',
                    prog = me,
                    epilog = epilogstr)
        group = parser.add_mutually_exclusive_group ()

        group.add_argument ('--directory', '-d', type = str, required=False,
                                nargs = '?', const = 'outdir',
                                help = 'output directory, default is "outdir"')
        group.add_argument ('--file', '-f', type = str, required=False,
                                nargs = '?', const = 'out.csv',
                                help = 'output file, default is "out.csv"')
        parser.add_argument ('--number', '-n', type = int, required=False,
                                default = 4096,
                                help = 'number of files to generate,'
                                        + ' default is 4096,'
                                        + ' only work with --directory')
        parser.add_argument ('--rows', '-r', type = int, required=False,
                                default  = 8192,
                                help = 'number of rows for each file,'
                                        + 'default is 8192')
        parser.add_argument ('--delimiter', type = str, required = False,
                                default = ',',
                                help = 'the delimiter, default is ","')
        parser.add_argument ('--types', '-t', type = str, nargs = '+',
                                choices = ['int', 'float', 'str'],
                                help = 'list of column types to generate')
        parser.add_argument ('--maxint', type = int, required = False,
                                default = 1e9,
                                help = 'maxinum of int for --type, default is 1e9')
        parser.add_argument ('--strlen', type = int, required = False,
                                default = 30,
                                help = 'length of str for --type, default is 30')
        parser.add_argument ('--quiet', '-q', action = 'store_true',
                                help = 'do not print log')
        parser.add_argument ('--process', '-p', type = int, required = False,
                                default = 4,
                                help = 'number of process, default is 4,'
                                        + ' only work with --directory')
        self._args = parser.parse_args ()

    def _sigbind (self):
        self._quit = False
        signal.signal (signal.SIGTERM, self._siginthandler)
        signal.signal (signal.SIGINT, self._siginthandler)

    def _siginthandler(self, signum, frame):
        self._quit = True

    def _generate (self, filename, args):
        rows = args.rows
        delimiter = args.delimiter
        types = args.types
        maxint = args.maxint
        strlen = args.strlen
        quiet = args.quiet

        random.seed (233)
        generators = []
        char_set = string.ascii_letters + string.digits + '_'

        if self._quit:
            return True

        logging.basicConfig (
            format = "%(asctime)-19.19s %(message)s",
            level = logging.CRITICAL if args.quiet else logging.INFO)

        try:
            generator = None
            fh = open (filename, 'w', encoding = 'utf8', newline = '')
            logging.info ('Begin write %s ...' %(filename))
            writer = csv.writer (fh, delimiter=delimiter)

            for column in types:
                if 'int' == column:
                    generator = lambda: random.randint (0, maxint)
                elif 'float' == column:
                    generator = lambda: random.random ()
                elif 'str' == column:
                    generator = lambda: ''.join (random.choice (char_set)
                                            for _ in range (strlen))
                else:
                    logging.critical ('ERROR: BAD column type %s' %(column))

                if generator:
                    generators.append (generator)

            for row in range (rows):
                writer.writerow ([generator () for generator in generators])

            logging.info ('End write %s' %(filename))
            fh.close ()
        except Exception as e:
            print (e)

        return True

    def run (self):
        args = self._args
        futures = []

        if args.file:
            return self._generate (args.file, args)

        if not args.directory:
            print ("Wrong option, run with '-h' to show help.", file=sys.stderr)
            return False

        if not os.path.exists (args.directory):
            try:
                os.makedirs (args.directory)
            except Exception as e:
                print (e)

        with ProcessPoolExecutor (max_workers = args.process) as executor:
            for count in range (1, args.number + 1):
                file = os.path.join (args.directory, str (count) + '.csv')
                futures.append (executor.submit (self._generate, file, args))

        return True

if '__main__' == __name__:
    ret = True
    generator = CSVGenerator ()

    ret = generator.run ()
    exit (not ret)

