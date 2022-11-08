# pso-utils
A collection of Python utilities made for parsing file formats used in Sega's Phantasy Star Online (PSO) for Nintendo Gamecube. Enables users to unpack archives, optionally modify the extracted assets, and repack them in a format that is accepted by the game's engine. The motivation is to facilitate creating custom content for a beloved cult classic MMO!

These tools were made for the Gamecube version of PSO. Due to small differences in file format, they will likely not work with other versions (and I made them because I found Gamecube utilities to be lacking.)

- GSL - Archive format usually containing 2D textures to be applied to 3D models
- BML - Archive format containing assets for in-game enemies and items, including textures, 3D models, and animations 

## gsl_util
I couldn't find a proper Gamecube format .gsl packer/unpacker so I made this one. The base code is adapted from the C++ Dreamcast example on the [PSO Developers Wiki](http://sharnoth.com/psodevwiki/start) with byte order adjustments for Gamecube format (Big Endian), and added functionality to repack an archive. It seems to be 100% faithful, as unpacking and repacking an original archive produces an identical file with the same hash. 
#### unpack / pack ####
- Unpacking a .gsl file produces a folder with the contents and text file with the original order:
```
pso-utils/
├── my_archive/
│   ├── unpacked contents 1
│   ├── unpacked contents 2
│   └── ...
├── my_archive.txt # output file with original order
└── my_archive.gsl
```
- This is to preserve the order of files in the archive which may matter for in-game loading behavior (ex: stage textures expected to be found immediately after models).
- The folder and text file of the same name must be present to repack.
- When replacing individual files, it's probably best to keep the original name (but you could modify both the filename and its counterpart in the text file.)
- Max size for a filename in the header is 32 characters/bytes.

#### find ####
- Parses a .gsl archive and returns all contents containing input string in filename. Useful for figuring out what asset to modify for a particular item or enemy. (Ex. Poison Lily and Nar Lily textures have 'flower' in their filename.)

## bml_util
Parsing and extracting gamecube BML is finished; however repacking into an "official" Sega-style BML is more complex. There are some oddities in the file format, for instance: blocks of empty space between archive contents which are usually 2048 bytes, but sometimes arbitrarily larger. It's hard to programmatically recreate these as it's unknown to me why these sections are larger.

*usage:*
```
# Unpack .gsl archive to folder/textfile pair
python gsl.py unpack <input_file> <unpack_dir>

# Pack folder/textfile pair to .gsl archive
python gsl.py pack <unpacked_dir> <out_file>

# Search all gsl archives in directory for contents with keyword in filename
python gsl.py find <directory> <keyword>

ex: 
python gsl.py unpack gsl_acave01.gsl caves1
python gsl.py pack caves1 out.gsl
python gsl.py find . flower
python gsl.py find ~/Desktop/root nanodrago
```

There's some edge case behavior I haven't fully figured out yet, so if you encounter a bug please create an issue so I can track it :). (For instance - does .gsl file section always start at 12288 bytes?)

Pull requests on all my PSO work are welcome! :) I would like to complete these tools but don't have time at the moment.

http://sharnoth.com/psodevwiki/dreamcast/gsl

http://sharnoth.com/psodevwiki/format/gsl

[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/T6T41O9SO)
