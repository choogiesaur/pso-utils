# pso-utils
a collection of helpful utilities for modding PSO! these are Python utilities aimed at parsing various PSO game file formats to enable users to extract, modify, and repack game assets before reinserting them into the game

## gsl_util
I couldn't find a proper Gamecube format .gsl packer/unpacker so I made this one. The base code is adapted from the Dreamcast example on the [PSO Developers Wiki](http://sharnoth.com/psodevwiki/start) with byte order adjustments for gamecube format (Big Endian), and added functionality to repack an archive.
- python command line script for now
- will not work with dreamcast/pc formats, use alternate tools for those

Notes:
- Unpacking a file produces a folder and text file with the ordered contents
- The folder and text file of the same name must be present to repack
- This is to preserve the file order which may matter for in-game loading behavior (ex: stage textures in specific order)
- When replacing individual files probably best to keep the original name, but you could modify the name in the text file
- Max size for a filename in the header is 32 characters/bytes

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
