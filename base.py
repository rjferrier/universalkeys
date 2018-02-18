import os
import re
from collections import namedtuple

KeyComboSegment = namedtuple('KeyComboSegment', ['shift', 'alt', 'key', 'special'])

SPECIAL_KEYS = ['space', 'enter', 'back_space', 'insert', 'delete',
                'minus', 'equals', 'open_bracket', 'close_bracket',
                'semicolon', 'quote', 'comma', 'period', 'slash']

def tolerant_mkdir(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass


class Binding:
    regex = re.compile('(?:.*?)(shift |alt )?(shift |alt )?([^ ,]+)(.*)')

    def __init__(self, key_expression, commands):
        self.key_combo = self.parse(key_expression)
        self.commands = commands

    def __repr__(self):
        return "{}: {}".format(self.key_combo, self.commands)

    def parse(self, key_combo, running_result=None):
        if running_result is None:
            running_result = []

        match = self.regex.match(key_combo)
        if not match:
            return running_result

        running_result.append(
            KeyComboSegment('shift ' in (match.group(1), match.group(2)),
                            'alt ' in (match.group(1), match.group(2)),
                            match.group(3),
                            match.group(3) in SPECIAL_KEYS))

        return self.parse(match.group(4), running_result)


class BindingWriter:
    def __init__(self, command_index, output_filename, output_path='.'):
        self.command_index = command_index
        self.output_filename = output_filename
        tolerant_mkdir(output_path)
        self.output_path = output_path

    def write_bindings(self, bindings):
        with open('{}/{}'.format(self.output_path, self.output_filename), 'w') as output_file:
            output_file.write(self.create_header())
            for binding in bindings:
                command = self.get_command(binding.commands)
                if command:
                    output_file.write(self.create_entry(binding.key_combo, self.get_command(binding.commands)))
            output_file.write(self.create_footer())

    def get_command(self, commands):
        try:
            return commands[self.command_index]
        except IndexError:
            return None

    def create_header(self):
        return ''

    def create_entry(self, key_combo, command):
        pass

    def create_footer(self):
        return ''

