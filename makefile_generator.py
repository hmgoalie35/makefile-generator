import os
import argparse
import platform

SUPPORTED_LANGUAGES = ['c++', 'c']

class MakefileGenerator(object):
    def __init__(self):
        self.__directory = ""
        self.__compiler = "g++"
        self.__flags = "-g -Wall -std=c++11"
        self.__executable = ""
        self.__args = ""
        self.__lib = ""
        self.__lang = ""
        self.parse_command_line_input()

    def create_parser(self):
        parser = argparse.ArgumentParser(description="Generate makefile for files in the specified directory")
        parser.add_argument('dir', help="Directory with the file(s)")
        parser.add_argument('-flags', required=False, help="Flag(s) to use when compiling, enclosed in \"\" (Default: %s)" % self.__flags)
        parser.add_argument('-cc', required=False, help="Compiler (Default: %s)" % self.__compiler)
        parser.add_argument('-exec', required=False, help="Executable name")
        parser.add_argument('-lang', required=False, choices=SUPPORTED_LANGUAGES, help="Use the default configs for the selected language")
        parser.add_argument('-lib', required=False, help="Libraries (if there are multiple, must be separated by a space)")
        parser.add_argument('-mode', required=False, help="If specified, user will enter in data via command line prompts", default=False, action='store_true')
        return parser

    def parse_command_line_input(self):
        parser = self.create_parser()
        self.__args = vars(parser.parse_args())

        if not os.path.isdir(self.__args["dir"]) and not os.path.exists(self.__args["dir"]):
            print "Invalid directory %s, exiting..." % self.__args["dir"]
            exit(1)

        self.__directory = self.__args['dir']

        if self.__args['mode']:
            self.prompt_user_for_input()
            return 0
        if self.__args["cc"]:
            self.__compiler = self.__args["cc"]
        if self.__args["flags"]:
            self.__flags = self.__args["flags"]
        if self.__args["exec"]:
            self.__executable = self.__args["exec"]
        if self.__args['lang']:
            self.__lang = self.__args['lang']
            if self.__args['lang'].lower() == "c++":
                self.__compiler = 'g++'
                self.__flags = '-g -Wall -std=c++11'
            else:
                # mode is c
                self.__compiler = 'gcc'
                self.__flags = '-g -Wall -std=c11'
        if self.__args['lib']:
            self.__lib = self.__args['lib']

        self.makefile_exists()
        

    def write_to_file(self, file_name):
        VALID_EXTENSIONS = [".cpp", ".c"]
        file_list = list(filter(lambda x: os.path.splitext(x)[1] in VALID_EXTENSIONS, os.listdir(os.path.dirname(file_name))))
        if len(file_list) == 0:
            print "No valid files were found in %s, exiting..." % os.path.dirname(file_name)
            exit(1)
        the_file = open(file_name, 'w')
        file_name_list = []
        write_str = ""
        for a_file in file_list:
            print "Processing File: %s" % a_file
            name = os.path.splitext(a_file)[0]
            file_name_list.append(name)
            write_str += "%s.o:\t%s" % (name, a_file)
            write_str += "\n\t%s $(%s) -c %s -o %s\n\n" % (self.__compiler, "FLAGS", a_file, name + ".o")

        the_file.write("FLAGS = %s\n\n" % self.__flags)
        the_file.write("all:\tMain\n\n")
        file_names = ""
        i = 0
        for name in file_name_list:
            if i+1 < len(file_name_list):
                file_names += name + ".o "
            else:
                file_names += name + ".o"
            i+=1
        the_file.write("Main:\tclean %s\n" % file_names)
        if self.__executable:
            if self.__lib:
                the_file.write("\t%s %s -o %s -l %s\n\n" % (self.__compiler, file_names, self.__executable, self.__lib))
            else:
                the_file.write("\t%s %s -o %s\n\n" % (self.__compiler, file_names, self.__executable))
        else:
            if self.__lib:
                the_file.write("\t%s %s -l %s\n\n" % (self.__compiler, file_names, self.__lib))
            else:
                the_file.write("\t%s %s\n\n" % (self.__compiler, file_names))

        the_file.write(write_str)
        if self.__executable:
            the_file.write("clean:\n\trm -f *.o %s\n" % self.__executable)
        else:
            the_file.write("clean:\n\trm -f *.o %s\n" % ("a.exe" if platform.system().lower() == "windows" else "a.out"))

        the_file.close()
        print "%s successfully saved." % file_name

    def prompt_user_for_input(self):
        print "Please fill out the following, or press <return> to ignore and use the default."
        lang = raw_input("Language: if specified, defaults for the selected language will be used and you will not be able to further customize anything. Select from [c++, c]: ")
        if lang:
            self.__lang = lang.strip().lower()
            if self.__lang == 'c++':
                self.__compiler = 'g++'
                self.__flags = '-g -Wall -std=c++11'
            elif self.__lang == 'c':
                # mode is c
                self.__compiler = 'gcc'
                self.__flags = '-g -Wall -std=c11'
            else:
                print "%s is not a valid selection, select from [c++, c]" % self.__lang
                exit(1)
        else:
            compiler = raw_input("Compiler: ").strip()
            if compiler:
                self.__compiler = compiler
            flags = raw_input("Flags: ").strip()
            if flags:
                self.__flags = flags
            lib = raw_input("Extra libraries, separated by a space: ").strip()
            if lib:
                self.__lib = lib
            executable = raw_input("Executable Name: ").strip()
            if executable:
                self.__executable = executable

        self.makefile_exists()

    def makefile_exists(self):
        makefile_name = "makefile"
        the_file = os.path.join(self.__directory, makefile_name)
        # note the exists funciton is case insensitive
        if os.path.exists(the_file):
            if os.path.isfile(the_file):      
                answer = raw_input("%s already exists, overwrite? (y/n): " % os.path.basename(the_file))
                if answer.strip().lower() == 'y':
                    self.write_to_file(the_file)
                else:
                    print "File not overwritten, exiting..."
                    exit(0)
            else:
                print "%s is not a valid file and/or path to a file. Is %s a directory?" % (the_file, the_file)
        else:
            self.write_to_file(the_file)

if __name__ == '__main__':
    MakefileGenerator()