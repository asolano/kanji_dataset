import xml.etree.ElementTree as ET
import os
import glob
from pathlib import Path
import cairosvg


# From wikipedia, we want the kanji code points only (not hiragana or katakana)
# https://en.wikipedia.org/wiki/Japanese_writing_system
min_unicode_point = 0x04E00
max_unicode_point = 0x09FBF
print(f'Japanese unicode range min={min_unicode_point:X} max={max_unicode_point:X}')


def is_japanese_code_point(c):
    return min_unicode_point <= c <= max_unicode_point

def unicode_id_to_code_point(unicode_id):
    code_point = int(f'0x{unicode_id}', 0)
    return code_point

def extract_code_point(child):
    unicode_id = child.get('id').split(':')[1].split('_')[1]
    code_point = unicode_id_to_code_point(unicode_id)
    return code_point

def create_output_folder(folder_path):
    path = Path(folder_path)
    path.mkdir(parents=True, exist_ok=True)

def modify_svg_file(input_folder, filename, output_folder):
    full_path = os.path.join(input_folder, filename)

    tree = ET.parse(full_path)
    root = tree.getroot()

    # Remove the stroke numbers section from the file
    for child in root:
        if 'id' in child.attrib:
            if 'StrokeNumbers' in child.get('id'):
                root.remove(child)

    save_filepath = os.path.join(output_folder, filename)
    with open(save_filepath, 'w') as f:
        print(f'Saving {save_filepath}')
        tree.write(f, encoding='unicode')

def convert_svg(in_folder, file_name, out_folder):
    in_path = os.path.join(in_folder, file_name)
    with open(in_path, 'r') as f_in:
        content = f_in.read()
        save_path = os.path.join(out_folder, file_name.replace('svg', 'png'))
        print(f'Converting {in_path} to {save_path}')
        cairosvg.svg2png(content, write_to=save_path, output_width=128, output_height=128, background_color="#fff")

def main():
    filepath = 'kanjivg.xml'
 
    try:
        tree = ET.parse(filepath)
    except ET.ParseError as e:
        print(f"ElementTree parse error: {e}")
    root = tree.getroot()

    # Get the unicode points for kanji
    is_japanese_kanji = [e for e in root.findall('.//kanji')
                         if 'id' in e.attrib
                         and is_japanese_code_point(extract_code_point(e))]
    print(f'is_japanese_kanji count: {len(is_japanese_kanji)}')

    for child in is_japanese_kanji[:10]:
        code_point = extract_code_point(child)
        print(f'kanji {child.get("id")} [{chr(code_point)}] has {len(child)} groups')

    # Get the SVG files (no variations)
    folder = os.path.join('kanjivg', 'kanji')
    # NOTE sorted() for debugging only, not needed
    # NOTE 5 chars to ignore variations
    svg_files = [f.split('/')[-1]
                 for f in sorted(glob.glob(os.path.join(folder, '*.svg')))
                 if len(filename := f.split('/')[-1].split('.')[0]) == 5
                 and is_japanese_code_point(unicode_id_to_code_point(filename.split('.')[0]))]
    print(f'svg_files count: {len(svg_files)}')

    # Create the image files without the stroke numbers
    svg_folder = 'svg_nonumbers'
    create_output_folder(svg_folder)
    for filename in svg_files:
        modify_svg_file(folder, filename, svg_folder)

    # Convert the SVG into PNG
    png_folder = 'png_nonumbers'
    create_output_folder(png_folder)
    for filename in svg_files:
        convert_svg(svg_folder, filename, png_folder)

    print(f'Done')

if __name__ == '__main__':
    main()
