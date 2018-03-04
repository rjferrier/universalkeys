from base import BindingWriter, SPECIAL_KEYS, F_KEYS


class EmacsBindingWriter(BindingWriter):
    SHIFT_MAP = {key: shifted for key, shifted in zip(
        "1234567890-=[];'#,./",
        '!"£$%^&*()_+{}:@~<>?')}
    SPECIAL_MAP = {key: emacs_key for key, emacs_key in zip(
        SPECIAL_KEYS,
        ['SPC', 'return', 'delete', 'insert', 'deletechar', *(c for c in '-=[];\',./'), *F_KEYS])}
    BRACKETED = ['return', 'delete', 'insert', 'deletechar', *F_KEYS]

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
        try:
            result = EmacsBindingWriter.SPECIAL_MAP[segment.key]
        except KeyError:
            result = segment.key

        envelope = '<{}>' if result in EmacsBindingWriter.BRACKETED else '{}'

        if segment.shift:
            result = EmacsBindingWriter.shift(result, segment.key in SPECIAL_KEYS)

        return envelope.format(('A-' if segment.alt else '') + ('C-' if segment.ctrl else '') + result)

    @staticmethod
    def shift(key, is_special):
        try:
            return EmacsBindingWriter.SHIFT_MAP[key]
        except KeyError:
            pass
        if not is_special and key.isalpha():
            return key.upper()
        return 'S-' + key
