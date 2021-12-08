# pso-utils
A collection of Python utilities made for parsing Sega/Phantasy Star Online (PSO) file formats. Enables users to unpack game asset archives, optionally modify the extracted assets, and repack them in a format that is faithful to the original. The purpose is to facilitate creating fresh custom content for a beloved cult classic!

These tools mainly pertain to the Gamecube version of PSO. Due to differences in file format, they will likely not work with other versions (and I made them because Gamecube support is lacking.)

## bml_util
WIP! Parsing and extracting gamecube BML is basically done; however recreating an "official" Sega BML is more complex. There are some caveats in the file format that seem unintuitive, for instance: blocks of empty space between archive contents which are usually 2048 bytes, but sometimes arbitrarily larger. It's hard to programmatically recreate these as it's unknown to me why these sections are larger. 

## gsl_util
I couldn't find a proper Gamecube format .gsl packer/unpacker so I made this one. The base code is adapted from the Dreamcast example on the [PSO Developers Wiki](http://sharnoth.com/psodevwiki/start) with byte order adjustments for Gamecube format (Big Endian), and added functionality to repack an archive.
- python command line script for now
- will not work with dreamcast/pc formats, use alternate tools for those

Notes:
- Unpacking a file produces a folder and text file with the ordered contents.
- The folder and text file of the same name must be present to repack.
- This is to preserve the file order which may matter for in-game loading behavior (ex: stage textures in specific order).
- When replacing individual files, it's probably best to keep the original name (but you could modify both the filename and its counterpart in the text file.)
- Max size for a filename in the header is 32 characters/bytes.

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

There's some edge case behavior I haven't fully figured out yet, so if you encounter a file that doesn't work please create an issue so I can figure it out. (For instance - does .gsl file section always start at 12288 bytes)

http://sharnoth.com/psodevwiki/dreamcast/gsl

http://sharnoth.com/psodevwiki/format/gsl

[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/T6T41O9SO)
