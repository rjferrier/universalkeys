from base import BindingWriter


class IntelliJBindingWriter(BindingWriter):
    editor_name = 'IntelliJ'

    def create_header(self):
        return '<keymap version="1" name="{}" parent="$default">'.format(self.output_filename)

    def create_entry(self, key_combo, command):
        foo = '''
  <action id="{}">
    <keyboard-shortcut {}/>
  </action>'''.format(command, ' '.join((self.create_keystroke(n + 1, segment) for n, segment in enumerate(key_combo))))
        return foo

    @staticmethod
    def create_keystroke(number, segment):
        keystroke__format = '{}-keystroke="{}"'.format('first' if number == 1 else 'second',
                                                       IntelliJBindingWriter.translate_segment(segment))
        return keystroke__format

    @staticmethod
    def translate_segment(segment):
        return ('shift ' if segment.shift else '') + ('alt ' if segment.alt else '') + segment.key

    def create_footer(self):
        return '\n</keymap>'
