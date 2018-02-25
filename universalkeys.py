from sys import argv

from base import extract_bindings
from binding_writers.emacs import EmacsBindingWriter
from binding_writers.intellij import IntelliJBindingWriter

binding_writers = [EmacsBindingWriter('bindings'),
                   IntelliJBindingWriter('ErgoBindings')]

try:
    csv_filename = argv[1]
except:
    raise Exception('Need to specify a TSV file')

bindings = extract_bindings(csv_filename)

for bw in binding_writers:
    bw.write(bindings)
