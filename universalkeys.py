from csv import reader
from sys import argv

from base import Binding
from binding_writers.emacs import EmacsBindingWriter
from binding_writers.intellij import IntelliJBindingWriter

OUTPUT_PATH = 'out'

WRITERS_FILENAMES = {EmacsBindingWriter: 'bindings.el',
                     IntelliJBindingWriter: 'ErgoBindings.xml'}


def create_binding_writers(editor_names):
    return [bw(i, WRITERS_FILENAMES[bw], OUTPUT_PATH)
            for bw in WRITERS_FILENAMES.keys()
            for i, name in enumerate(editor_names)
            if name == bw.editor_name]


try:
    csv_filename = argv[1]
except:
    raise Exception('Need to specify a TSV file')

with open(csv_filename, 'r') as csv_file:
    rows = reader(csv_file, delimiter='\t')
    header = next(rows)
    binding_writers = create_binding_writers(header[1:])
    bindings = [Binding(row[0], row[1:]) for row in rows if any(row)]

for bw in binding_writers:
    bw.write_bindings(bindings)
