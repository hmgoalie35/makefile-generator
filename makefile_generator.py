import os.path
import argparse
import platform

class MakefileGenerator(object):
    def __init__(self):
        self.__directory = ""
        self.__compiler = "g++"
        self.__flags = "-g -Wall -std=c++11"
        self.__executable = ""
        self.__args = ""
        self.__lib = ""
        self.__lang = ""
        self.__mode = False
        self.get_command_line_input()

    def get_command_line_input(self):
        parser = argparse.ArgumentParser(description="Autogenerate makefile for files in the specified directory")
        parser.add_argument('dir', help="The directory with the .cpp, .hpp, .c, .h files")
        parser.add_argument('-flags', required=False, help="Flags to use when compiling, enclosed in \"\". (Default: -g -Wall -std=c++11)")
        parser.add_argument('-cc', required=False, help="Compiler (Default: g++)")
        parser.add_argument('-exec', required=False, help="Name of executable")
        parser.add_argument('-lang', required=False, choices=['c++', 'c'], help="Use Default Configs for Selected Language")
        parser.add_argument('-lib', required=False, help="Libraries to Include When Compiling, Separated by Spaces")
        parser.add_argument('-mode', required=False, help="If Specified, User Will Enter in Data Via Command Line Prompts", default=False, action='store_true')
        args = vars(parser.parse_args())
        self.__args = args

        if not os.path.isdir(self.__args["dir"]) and not os.path.exists(self.__args["dir"]):
            print("Invalid directory supplied on the command line, exiting...")
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
        directory = os.path.dirname(file_name)
        if not directory:
            directory = os.path.join(os.path.dirname(file_name), '.')
        VALID_EXTENSIONS = [".cpp", ".c", ".java"]
        file_list = list(filter(lambda x: os.path.splitext(x)[1] in VALID_EXTENSIONS, os.listdir(directory)))
        if len(file_list) == 0:
            print("No valid files were found, exiting...")
            exit(1)
        for x in file_list:
            print("Processing File: %s" % x)
        the_file = open(file_name, 'w')
        file_name_list = []
        write_str = ""
        for a_file in file_list:
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
        print("%s successfully saved." % os.path.abspath(file_name))

    def prompt_user_for_input(self):
        print "Please Fill Out The Following, Or Press <return> To Ignore And Use The Default."
        lang = raw_input("Language: If Specified, Defaults For the Selected Language Will Be Used And You Will Not Be Able to Further Customize Anything. Select From {c++, c}: ").strip()
        if lang:
            self.__lang = lang.lower()
            if self.__lang == 'c++':
                self.__compiler = 'g++'
                self.__flags = '-g -Wall -std=c++11'
            else:
                # mode is c
                self.__compiler = 'gcc'
                self.__flags = '-g -Wall -std=c11'
            self.makefile_exists()
        else:
            compiler = raw_input("Compiler: ").strip().lower()
            if compiler:
                self.__compiler = compiler
            flags = raw_input("Flags: ").strip().lower()
            if flags:
                self.__flags = flags
            lib = raw_input("Extra Libraries, Separated By A Space: ").lower()
            if lib:
                self.__lib = lib
            executable = raw_input("Executable Name: ").strip()
            if executable:
                self.__executable = executable

            print self.__directory
            self.makefile_exists()

    def makefile_exists(self):
        makefile_name = "makefile"
        the_file = os.path.join(self.__directory, makefile_name)
        print self.__directory, the_file
        # note the exists funciton is case insensitive
        if os.path.exists(the_file):
            if os.path.isfile(the_file):      
                answer = raw_input("%s already exists, overwrite? (y/n): " % os.path.basename(the_file))
                if answer.strip().lower() == 'y':
                    self.write_to_file(the_file)
                else:
                    print("File not overwritten, exiting...")
                    exit(0)
            else:
                print "%s is not a valid file and/or path to a file." % the_file
        else:
            self.write_to_file(the_file)
def main():
    MakefileGenerator()
main()
