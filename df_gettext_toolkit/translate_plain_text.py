import os
import sys
import shutil

from .parse_raws import parse_plain_text_file
from .po import load_po


def translate_plain_text(po_filename, path, encoding, join_paragraphs=True):
    with open(po_filename, 'r', encoding='utf-8') as pofile:
        dictionary = {item['msgid']: item['msgstr'] for item in load_po(pofile)}
        
    for cur_dir, _, files in os.walk(path):
        for file_name in files:
            basename, ext = os.path.splitext(file_name)
            if ext == '.txt':
                bak_name = os.path.join(cur_dir, basename+'.bak')
                dest_name = os.path.join(cur_dir, file_name)
                
                if not os.path.exists(bak_name):
                    shutil.copy(dest_name, bak_name)
                
                with open(bak_name) as src:
                    with open(dest_name, 'w', encoding=encoding) as dest:
                        yield file_name
                        for text_block, is_translatable, _ in parse_plain_text_file(src, join_paragraphs):
                            text_block = text_block.rstrip('\n')
                            if text_block in dictionary:
                                translation = dictionary[text_block]
                                if not translation:
                                    translation = text_block
                            else:
                                translation = text_block
                            print(translation, file=dest)


def main():
    po_filename = sys.argv[1]

    if len(sys.argv) > 2:
        path = sys.argv[2]
    else:
        path = '.'

    join_paragraphs = '--split' not in sys.argv[1:]

    for filename in translate_plain_text(po_filename, path, 'cp1251', join_paragraphs):
        print(filename, file=sys.stderr)


if __name__ == "__main__":
    main()
