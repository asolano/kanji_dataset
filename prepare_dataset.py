import os
import xml.etree.ElementTree as ET
import glob
import collections
import json
from create_images import unicode_id_to_code_point, is_japanese_code_point
from string import Template


def create_metadata_content(characters, has_png):
    metadata_content = collections.defaultdict(list)

    invalid_count = 0
    valid_count = 0

    for character in characters:
        literal = character.find('literal')
        for cp in character.findall('codepoint'):
            cp_value = cp.find('cp_value')
            code_point = unicode_id_to_code_point(cp_value.text)
            if cp_value.get('cp_type') == 'ucs':
                # Check for code points outside of kanji range
                if not is_japanese_code_point(code_point):
                    print(f"Warning! invalid code point={code_point:X} character={literal.text}")
                    invalid_count += 1
                else:
                    if code_point not in has_png:
                        print(f'Warning! code point {code_point:X} has no SVG')
                    else:
                        meanings = character.iter('meaning')
                        valid_count += 1
                        for meaning in meanings:
                            # Ignore non-english meanings
                            if 'm_lang' not in meaning.attrib:
                                metadata_content[f'0{cp_value.text}.png'].append(meaning.text)

    print(f'Image to text entries: {len(metadata_content)}')
    print(f'code points: valid={valid_count} invalid={invalid_count}')
    
    return metadata_content


# JSONL file format
# {"file_name": "something_1.png", "text": ["caption_1", "caption_2", ..., "caption_n"]}
def create_entry(template, image_file, text_captions):
    full_captions = [template.substitute({"MEANING": m}) for m in text_captions]
    return {'file_name': image_file, 'text': full_captions }

def write_metadata_file(base_path, png_files, metadata_content, template):
    # The metadata.json needs to be inside the image folder
    metadata_file = os.path.join(base_path, 'png_nonumbers', 'metadata.jsonl')

    with open(metadata_file, 'w') as out_file:
        for (image, captions) in metadata_content.items():
            # Some PNG are not full kanji
            if image not in png_files:
                print(f'Warning! image {image} does not exist')
                continue
            entry = create_entry(template, image, captions)
            json.dump(entry, out_file)
            out_file.write('\n')


def main():
    base_path = os.getcwd()

    filepath = os.path.join(base_path, 'kanjidic2.xml')
    print(f'Dictionary file: {filepath}')
    try:
        tree = ET.parse(filepath)
    except ET.ParseError as e:
        print(f"ElementTree parse error: {e}")
    root = tree.getroot()

    # Get all the character elements
    characters = [e for e in root.findall('.//character')]
    print(f'Characters in dictionary: {len(characters)}')

    # NOTE Not all kanji have an SVG
    has_png = []
    full_paths = sorted(glob.glob(os.path.join(base_path, 'png_nonumbers', '*.png')))
    png_files = [x.split('/')[-1] for x in full_paths]
    print(f'PNG files: {len(png_files)}')
    for path in full_paths:
        file_name = path.split('/')[-1]
        unicode_code = file_name.split('.')[0]
        has_png.append(unicode_id_to_code_point(unicode_code))
    print(f'Characters with PNG: {len(has_png)}')

    metadata_content = create_metadata_content(characters, has_png)
    template = Template('a kanji drawing meaning "$MEANING"')
    write_metadata_file(base_path, png_files, metadata_content, template)

    # FIXME data is loaded first, then looks for metadata
    # SEE https://discuss.huggingface.co/t/valueerror-audio-at-filename-doesnt-have-metadata-in-path-metadata-csv/58303/2
    # Rename files in png_nonumbers/ that are not present in metadata.json
    to_rename = []
    for file_name in png_files:
        if file_name not in metadata_content:
            print(f'Will rename {file_name}')
            to_rename.append(file_name)

    for path in to_rename:
        old_path = os.path.join(base_path, 'png_nonumbers', path)
        new_path = os.path.join(base_path, 'png_nonumbers', f'{old_path}.old')
        print(f'Renaming {old_path} to {new_path}')
        os.rename(old_path, new_path)

if __name__ == '__main__':
    main()
