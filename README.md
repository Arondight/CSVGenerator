# CSVGenerator

## ABOUT

Generate random CSV files, this may help for some test.

## USAGE

```
$ ./CSVGenerator.py
usage: ./CSVGenerator.py [-h] [--directory [DIRECTORY] | --file [FILE]]
                         [--number NUMBER] [--rows ROWS]
                         [--delimiter DELIMITER]
                         [--types {int,float,str} [{int,float,str} ...]]
                         [--maxint MAXINT] [--strlen STRLEN] [--quiet]
                         [--process PROCESS]

Generate random CSV files.

optional arguments:
  -h, --help            show this help message and exit
  --directory [DIRECTORY], -d [DIRECTORY]
                        output directory, default is "outdir"
  --file [FILE], -f [FILE]
                        output file, default is "out.csv"
  --number NUMBER, -n NUMBER
                        number of files to generate, default is 4096, only work with --directory
  --rows ROWS, -r ROWS  number of rows for each file,default is 8192
  --delimiter DELIMITER
                        the delimiter, default is ","
  --types {int,float,str} [{int,float,str} ...], -t {int,float,str} [{int,float,str} ...]
                        list of column types to generate
  --maxint MAXINT       maxinum of int for --type, default is 1e9
  --strlen STRLEN       length of str for --type, default is 30
  --quiet, -q           do not print log
  --process PROCESS, -p PROCESS
                        number of process, default is 4, only work with --directory

--directory and --file are mutually exclusive.

Examples:
	./CSVGenerator.py -d outdir -n 4096 -r 8192 -t int float str
	./CSVGenerator.py -d -t int int
	./CSVGenerator.py -f out.csv -r 65536 -t str int str float
	./CSVGenerator.py -f -t str str
```

## COPYRIGHT

Copyright (c) 2018 秦凡东 (Qin Fandong)

## LICENSE

Read [LICENSE](./LICENSE)

