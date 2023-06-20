## bml-util ##
Preliminary support for BML repacking has been added.
Packing is still technically incomplete as PRS decompression may be needed. Not certain if files need to be decompressed at extraction time or could be decompressed later with an alternate utility. If anyone has copies or links to the old Sharnoth documentation for PRS decompress, bml, and gsl let me know!

Usage:
```
  Unpack BML Archive:
    python script.py <bml_file>

  Repack BML Archive:
    python script.py -p <unpack_dir> <new_bml_file.bml> <order_file.txt>

  - Unpack BML Archive:
    Extracts the contents of the specified BML archive file.

  - Repack BML Archive:
    Repacks the extracted files from the specified directory into a new BML archive according to the order specified in the order file.
```
