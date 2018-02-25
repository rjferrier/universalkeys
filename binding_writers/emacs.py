from base import BindingWriter, SPECIAL_KEYS


class EmacsBindingWriter(BindingWriter):
    special_key_map = {key: emacs_key for key, emacs_key in zip(
        SPECIAL_KEYS, ['SPC', 'RET', 'DEL', '<insert>', '<deletechar>', *(c for c in '-=[];\',./')])}
    alt_map = {'SPC': 'SPC', 'RET': 'return', 'DEL': 'backspace', '<insert>': 'insert', '<deletechar>': 'delete'}
    shift_map = {key: shifted for key, shifted in zip(
        "1234567890-=[];'#,./",
        '!"£$%^&*()_+{}:@~<>?')}

    def __init__(self, output_name):
        super().__init__('Emacs', output_name + '.el')

    def create_entries(self, command, key_combos):
        return ''.join((EmacsBindingWriter.create_entry(command, key_combo) for key_combo in key_combos))

    @staticmethod
    def create_entry(command, key_combo):
        return '(define-key global-map (kbd "{}") \'{})\n'.format(
            EmacsBindingWriter.translate_key_combo(key_combo), command)

    @staticmethod
    def translate_key_combo(key_combo):
        return ' '.join(
            EmacsBindingWriter.translate_segment(segment) for segment in key_combo)

    @staticmethod
    def translate_segment(segment):
        if type(segment) == bool:
            pass
        result = segment.key

        if segment.special:
            result = EmacsBindingWriter.special_key_map[result]

        if segment.shift:
            result = EmacsBindingWriter.shift(result, segment.special)

        if segment.alt:
            result = EmacsBindingWriter.alter(result)

        return result

    @staticmethod
    def shift(key, is_special):
        try:
            return EmacsBindingWriter.shift_map[key]
        except KeyError:
            pass
        if not is_special and key.isalpha():
            return key.upper()
        return 'S-' + key

    @staticmethod
    def alter(key):
        try:
            return '<A-{}>'.format(EmacsBindingWriter.alt_map[key])
        except KeyError:
            pass
        return 'A-' + key
