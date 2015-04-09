# makefile-generator
For all of those people who copy their old makefiles...

A useful little tool that will easily create makefiles for you.

No more copying and pasting of old makefiles and trying to figure out why the hell it isn't working, even though all you did was copy and paste a previous makefile


Python 2 Currently Supported

Python 3 Support Coming Soon

##Notes: 
The directory arg must be included at all times

Directory arg can be passed as ".", "../", etc. (w/o quotes)

For multiple flags, the flags must be enclosed in "". ex: "-g -Wall" NOT -g -Wall

Specifying -lang [arg] will use the following defaults:

c++: 

Flags = -g -Wall -std=c++11

CC = g++

c:

Flags = -g -Wall -std=c11

CC = gcc

(more to come if desired)

##Usage:
```
$ python makefile_generator.py -h

usage: makefile_generator.py [-h] [-flags FLAGS] [-cc CC] [-exec EXEC]
                             [-lang {c++,c}] [-lib LIB] [-mode]
                             dir

Generate makefile for files in the specified directory

positional arguments:
  dir            Directory with the file(s)

optional arguments:
  -h, --help     show this help message and exit
  -flags FLAGS   Flag(s) to use when compiling, enclosed in "" (Default: -g
                 -Wall -std=c++11)
  -cc CC         Compiler (Default: g++)
  -exec EXEC     Executable name
  -lang {c++,c}  Use the default configs for the selected language
  -lib LIB       Libraries (if there are multiple, must be separated by a
                 space)
  -mode          If specified, user will enter in data via command line prompts
```

Any questions feel free to email me at hpittin1@binghamton.edu
