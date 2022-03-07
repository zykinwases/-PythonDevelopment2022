from ast import arg
import cmd, sys
from tracemalloc import start
import pynames
import inspect

class GeneratingShell(cmd.Cmd):
    intro = 'Welcome to the name generation shell.   Type help or ? to list commands.\n'
    prompt = '(generator) '
    language = 'NATIVE'
    genders = ['MALE', 'FEMALE']
    languages = ['RU', 'EN', 'NATIVE']
    generators = []
    for generator in pynames.get_all_generators():
        name = generator.__name__
        subclass_position = name.find('NamesGenerator') + name.find('FullnameGenerator') + 1
        subclass_name = ''
        if subclass_position > -1:
            subclass_name = name[0:subclass_position]
        class_name = generator.__module__.split('.')[-1]
        if (subclass_name.lower() == class_name):
            generators.append({'class': class_name, 'subclass': '', 'generator': generator.__module__ + '.' + generator.__name__})
        else:
            generators.append({'class': class_name, 'subclass': subclass_name, 'generator': generator.__module__ + '.' + generator.__name__})

    def do_language(self, arg):
        'Set generating language: language <language>'
        args = arg.split()
        if (args[0] in self.languages):
            self.language = args[0]
    def complete_language(self, text, line, begidx, endidx):
        return [l for l in self.languages if l.startswith(text)]

    def do_generate(self, arg):
        'Generate name: generate <class> <subclass> <gender> or generate <class> <subclass>'
        args = arg.split()
        gender = 'ALL'
        if (args[-1].upper() in self.genders):
            gender = args[-1].upper()
        if (len(args) == 1) or (len(args) == 2 and gender != 'ALL'):
            if gender == 'ALL':
                gender = 'MALE'
            for gen in self.generators:
                if (gen['class'] == args[0]):
                    print(eval(gen['generator'] + '().get_name_simple(pynames.GENDER.' + gender + ', pynames.LANGUAGE.' + self.language + ')'))
                    return
        if (len(args) == 2) or (len(args) == 3 and gender != 'ALL'):
            if gender == 'ALL':
                gender = 'MALE'
            for gen in self.generators:
                if (gen['class'] == args[0]) and (gen['subclass'] == args[1]):
                    print(eval(gen['generator'] + '().get_name_simple(pynames.GENDER.' + gender + ', pynames.LANGUAGE.' + self.language + ')'))
                    return
    def complete_generate(self, text, line, begin, end):
        command = line.split(' ')
        if (len(command) == 2):
            return [l['class'] for l in self.generators if l['class'].startswith(text)]
        if (len(command) == 3):
            main_generator = [l for l in self.generators if l['class'] == command[1]][0]
            if main_generator['subclass'] == '':
                return [g for g in self.genders if g.startswith(command[2])]
            else:
                return [l['subclass'] for l in self.generators if (l['class'] == command[1]) and (l['subclass'].startswith(command[2]))]
        if (len(command) == 4):
            return [g for g in self.genders if g.startswith(command[3])]

    def do_info(self, arg):
        'Print info about class/subclass: info <class> <subclass> or info <class> <subclass> <gender> or info <class> <subclass> language'
        args = arg.split()
        gender = 'ALL'
        if (args[-1].upper() in self.genders):
            gender = args[-1].upper()
        if (len(args) == 1) or (len(args) == 2 and gender != 'ALL'):
            for gen in self.generators:
                if (gen['class'] == args[0]):
                    print(eval(gen['generator'] + '().get_names_number(pynames.GENDER.' + gender + ')'))
                    return
        if (len(args) == 2) or (len(args) == 3 and gender != 'ALL'):
            for gen in self.generators:
                if (gen['class'] == args[0]) and (gen['subclass'] == args[1]):
                    print(eval(gen['generator'] + '().get_names_number(pynames.GENDER.' + gender + ')'))
                    return
        if (args[-1] == 'language'):
            if (len(args) == 2):
                for gen in self.generators:
                    if (gen['class'] == args[0]):
                        print(' '.join(eval(gen['generator'] + '().languages')))
            else:
                for gen in self.generators:
                    if (gen['class'] == args[0]) and (gen['subclass'] == args[1]):
                        print(' '.join(eval(gen['generator'] + '().languages')))
    def complete_info(self, text, line, begin, end):
        command = line.split(' ')
        if (len(command) == 2):
            return [l['class'] for l in self.generators if l['class'].startswith(text)]
        if (len(command) == 3):
            main_generator = [l for l in self.generators if l['class'] == command[1]][0]
            if main_generator['subclass'] == '':
                completion_list = [g for g in self.genders if g.startswith(command[2])]
                if ("language".startswith(command[2])):
                    completion_list.append("language")
                return completion_list
            else:
                return [l['subclass'] for l in self.generators if (l['class'] == command[1]) and (l['subclass'].startswith(command[2]))]
        if (len(command) == 4):
            completion_list = [g for g in self.genders if g.startswith(command[3])]
            if ("language".startswith(command[3])):
                completion_list.append("language")
            return completion_list

    def do_exit(self, arg):
        'Exit name generation:  exit'
        return True

if __name__ == '__main__':
    GeneratingShell().cmdloop()