# kanji_dataset

Creates a simple HuggingFace Dataset compatible data set of kanji images and their meanings.

```
# Clone KanjiVG repository to get the SVG files
git clone https://github.com/KanjiVG/kanjivg.git

# Get the `kanjivg.xml` file from the Releases section
wget https://github.com/KanjiVG/kanjivg/releases/download/r20240807/kanjivg-20240807.xml.gz
gunzip kanjivg-20240807.xml.gz

# Create a virtual environmnet
python -m venv myenv
source myenv/bin/activate
pip install -U pip
pip install cairosvg
```

```
# Run the script
python create_images.py

Japanese unicode range min=4E00 max=9FBF
is_japanese_kanji count: 6409
kanji kvg:kanji_04e00 [一] has 1 groups
kanji kvg:kanji_04e01 [丁] has 1 groups
kanji kvg:kanji_04e03 [七] has 1 groups
kanji kvg:kanji_04e07 [万] has 1 groups
kanji kvg:kanji_04e08 [丈] has 1 groups
kanji kvg:kanji_04e09 [三] has 1 groups
kanji kvg:kanji_04e0a [上] has 1 groups
kanji kvg:kanji_04e0b [下] has 1 groups
kanji kvg:kanji_04e0d [不] has 1 groups
kanji kvg:kanji_04e0e [与] has 1 groups
svg_files count: 6410
Saving svg_nonumbers/04e00.svg
Saving svg_nonumbers/04e01.svg
Saving svg_nonumbers/04e03.svg
Saving svg_nonumbers/04e07.svg
Saving svg_nonumbers/04e08.svg
Saving svg_nonumbers/04e09.svg
Saving svg_nonumbers/04e0a.svg
Saving svg_nonumbers/04e0b.svg
(...)
Saving svg_nonumbers/09f9d.svg
Saving svg_nonumbers/09fa0.svg
Converting svg_nonumbers/04e00.svg to png_nonumbers/04e00.png
Converting svg_nonumbers/04e01.svg to png_nonumbers/04e01.png
Converting svg_nonumbers/04e03.svg to png_nonumbers/04e03.png
Converting svg_nonumbers/04e07.svg to png_nonumbers/04e07.png
Converting svg_nonumbers/04e08.svg to png_nonumbers/04e08.png
(...)
Converting svg_nonumbers/09f95.svg to png_nonumbers/09f95.png
Converting svg_nonumbers/09f9c.svg to png_nonumbers/09f9c.png
Converting svg_nonumbers/09f9d.svg to png_nonumbers/09f9d.png
Converting svg_nonumbers/09fa0.svg to png_nonumbers/09fa0.png
```

```
# Get the meanings from kanjidic
# Go to https://www.edrdg.org/wiki/index.php/KANJIDIC_Project to get the file and description
wget http://www.edrdg.org/kanjidic/kanjidic2.xml.gz
gunzip kanjidic2.xml.gz
```

```
# Run the script
python prepare_dataset.py

Warning! code point 9F5D has no SVG
Warning! code point 9F5E has no SVG
Warning! code point 9F68 has no SVG
Warning! code point 9F69 has no SVG
(...)
Warning! invalid code point=2000B character=𠀋
Warning! invalid code point=20089 character=𠂉
Warning! invalid code point=200A2 character=𠂢
Warning! invalid code point=200A4 character=𠂤
Warning! invalid code point=201A2 character=𠆢
Warning! invalid code point=20213 character=𠈓
(...)
Warning! code point 4E0F has no SVG
Warning! code point 4E29 has no SVG
Warning! code point 4E2C has no SVG
Warning! code point 4E48 has no SVG
(...)
Will rename 04ebb.png
Will rename 04edd.png
Will rename 04ff1.png
Will rename 0525d.png
Will rename 0541e.png
Will rename 055bb.png
Will rename 0590d.png
Will rename 05c03.png
Will rename 0687c.png
Will rename 07c1e.png
Will rename 087ec.png
Will rename 098e0.png
Will rename 09ec3.png
Will rename 09ed1.png
```

To use it:
```
pip install datasets
python
>>> import datasets
>>> from datasets import load_dataset, Image
>>> dataset = load_dataset("png_nonumbers")
Resolving data files: 100%|██████████████████████████| 6410/6410 [00:00<00:00, 66288.17it/s]
Downloading data: 100%|███████████████████████████| 6396/6396 [00:00<00:00, 69914.72files/s]
Generating train split: 6395 examples [00:00, 54542.48 examples/s]
```

Note there are no training splits, and the metadata is stored in `png_nonumbers/metadata.jsonl`.
