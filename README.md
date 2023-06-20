# pso-utils
A collection of Python utilities made for parsing file formats used in Sega's Phantasy Star Online (PSO) for Nintendo Gamecube. Enables users to unpack archives, optionally modify the extracted assets, and repack them in a format that is accepted by the game's engine. The motivation is to facilitate creating custom content for a beloved cult classic MMO!

These tools were made for the Gamecube version of PSO. Due to small differences in file format, they will likely not work with other versions (and I made them because I found Gamecube utilities to be lacking.)

- GSL - Archive format usually containing 2D textures to be applied to 3D models
- BML - Archive format containing assets for in-game enemies and items, including textures, 3D models, and animations 

Please delve into each tool's folder for specific usage.

There's some edge case behavior I haven't fully figured out yet, so if you encounter a bug please create an issue so I can track it :). (For instance - does .gsl file section always start at 12288 bytes?)

Pull requests on all my PSO work are welcome! :) I would like to complete these tools but don't have time at the moment.

http://sharnoth.com/psodevwiki/dreamcast/gsl

http://sharnoth.com/psodevwiki/format/gsl

[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/T6T41O9SO)
