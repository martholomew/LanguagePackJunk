#!/bin/python

import os
import sys
import json
from os import listdir
from os.path import isfile, join
from pprint import pprint
import xml.etree.ElementTree as et


#popupKeyboard="@xml/popup_16keys_abc"


with open("lang_acc.json", "r") as f:
    langs = json.load(f)

assert sys.argv[1] in langs.keys()
print("noice")

accents = langs[sys.argv[1]]

latin_dir = "latin_keyboards"
keyboards = [join(latin_dir, f) for f in listdir(latin_dir) if isfile(join(latin_dir, f))]

schema = '{http://schemas.android.com/apk/res/android}'
codes = schema + "codes"
popup = schema + "popupKeyboard"

for keyboard in keyboards:
    with open(keyboard, 'r') as f:
        xml = et.parse(f).getroot()
        for alpha in accents:
            for key in xml.iter('Key'):
                if key.attrib[codes] == alpha:
                    key.attrib[popup] = f"@xml/popup_{alpha}"
        try:
            os.mkdir(sys.argv[1])
        except OSError:
            pass
        new_keyboard = sys.argv[1] + "/" + keyboard.split('/')[1]
        tree = et.ElementTree(xml)
        tree.write(new_keyboard, xml_declaration=True, encoding='utf-8')
        with open(new_keyboard, "r+") as s:
            data = s.read().replace("ns0", "android")
            s.seek(0)
            s.write(data)
            s.truncate()

for alpha in accents:
    xml = et.Element('Keyboard')
    xml.set("xmlns:android", "http://schemas.android.com/apk/res/android")
    row = et.SubElement(xml, 'Row')
    for accent in accents[alpha]:
        et.SubElement(row, 'Key').set("android:codes", accent)
    new_popup = sys.argv[1] + "/" + "popup_" + alpha + ".xml"
    tree = et.ElementTree(xml)
    tree.write(new_popup, xml_declaration=True, encoding='utf-8')
