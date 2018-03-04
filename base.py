import os
import re
from csv import reader
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

    def __init__(self, editor, command, key_expression):
        self.editor = editor
        self.command = command
        self.key_combo = self.parse(key_expression)

    def __repr__(self):
        return "Binding[{}, {}, {}]".format(self.editor, self.command, self.key_combo)

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


def count_key_columns(header):
    for i, txt in enumerate(header):
        if txt.lower() != 'key' and txt:
            return i


def extract_bindings(csv_filename):
    with open(csv_filename, 'r') as csv_file:
        rows = reader(csv_file, delimiter='\t')
        header = next(rows)
        n = count_key_columns(header)
        return [Binding(editor, command, key_expression)
                for row in rows
                for editor, commands in zip(header[n:], row[n:])
                for key_expression in (row[j] for j in range(n))
                for command in commands.split(',')
                if any(row) and key_expression and commands]


class BindingWriter:
    output_path = 'out'

    def __init__(self, editor, output_filename):
        self.editor = editor
        self.output_filename = output_filename
        tolerant_mkdir(self.output_path)

    def write(self, bindings):
        with open('{}/{}'.format(self.output_path, self.output_filename), 'w') as output_file:
            output_file.write(self.create_header())
            bindings_map = self.create_map(bindings)
            for command in bindings_map:
                print(command, bindings_map[command])
                output_file.write(self.create_entries(command, bindings_map[command]))
            output_file.write(self.create_footer())

    def create_map(self, bindings):
        result = dict()
        for binding in (b for b in bindings if b.editor == self.editor):
            try:
                result[binding.command].append(binding.key_combo)
            except KeyError:
                result[binding.command] = [binding.key_combo]
        return result

    def create_header(self):
        return ''

    def create_entries(self, command, key_combos):
        pass

    def create_footer(self):
        return ''
