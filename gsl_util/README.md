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
