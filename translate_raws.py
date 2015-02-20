import sys
import os
import shutil

from dfgettext import *

if len(sys.argv)<3:
    sys.exit()

mofilename = sys.argv[1]
dictionary = {(item['msgid'],item['msgctxt']):item['msgstr'] for item in LoadMO(mofilename)}

path = sys.argv[2]
raws = os.listdir(path)
for file_name in raws:
    basename, ext = os.path.splitext(file_name)
    if ext == '.txt':
        bak_name = os.path.join(path, basename+'.bak')
        raw_file = os.path.join(path, file_name)
        
        if not os.path.exists(bak_name):
            shutil.copy(raw_file, bak_name)
        
        with open(bak_name) as src:
            with open(raw_file, 'w', encoding='cp1251') as dest:
                for line in translate_raw_file(src, dictionary):
                    print(line, file=dest)