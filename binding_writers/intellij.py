from base import BindingWriter


class IntelliJBindingWriter(BindingWriter):
    def __init__(self, output_name, parent_keymap='$default'):
        super().__init__('IntelliJ', output_name + '.xml')
        self.output_name = output_name
        self.parent_keymap = parent_keymap

    def create_header(self):
        return '<keymap version="1" name="{}" parent="{}">'.format(self.output_name, self.parent_keymap)

    def create_entries(self, command, key_combos):
        return '''
  <action id="{}">{}
  </action>'''.format(command, ''.join((IntelliJBindingWriter.create_sub_entry(key_combo) for key_combo in key_combos)))

    def create_footer(self):
        return '\n</keymap>'

    @staticmethod
    def create_sub_entry(key_combo):
        return '\n    <keyboard-shortcut {}/>'.format(
            ' '.join((IntelliJBindingWriter.create_keystroke(n + 1, segment) for n, segment in enumerate(key_combo))))

    @staticmethod
    def create_keystroke(number, segment):
        keystroke__format = '{}-keystroke="{}"'.format('first' if number == 1 else 'second',
                                                       IntelliJBindingWriter.translate_segment(segment))
        return keystroke__format

    @staticmethod
    def translate_segment(segment):
        return ('shift ' if segment.shift else '') + \
               ('ctrl ' if segment.alt else '') + \
               ('alt ' if segment.alt else '') + \
               segment.key
