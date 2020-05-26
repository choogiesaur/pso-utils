import os
import struct
import sys

def bml_archive(filename):
 
    if not os.path.exists(filename):
        return None
 
    with open(filename, "rb") as fp:
 
        fp.seek(0, os.SEEK_END)
        size = fp.tell()
 
        fp.seek(4)
        count = struct.unpack('i', fp.read(4))[0]
        fp.seek(0x40)
 
        files = []
        for i in range(count):
            data = fp.read(0x34)
            s = struct.unpack('>32sIIIII', data)
            fp.read(0x0c)
 
            name = s[0].decode('ascii').rstrip(' \t\r\n\0')
            compressed_size = s[1]
            file_type = s[2]
            decompressed_size = s[3]
            pvm_compressed_size = s[4]
            pvm_decompressed_size = s[5]
 
            files.append({
                "filename" : name,
                "compressed_size" : compressed_size,
                "decompressed_size" : decompressed_size
            })
 
            if pvm_compressed_size == 0:
                continue
 
            basename = os.path.splitext(name)[0]
 
            files.append({
                "filename" : "%s.pvm" % (basename),
                "compressed_size" : pvm_compressed_size,
                "decompressed_size" : pvm_decompressed_size
            })
 
        ofs = fp.tell()
        ofs = (0xFFFFF800 & ofs) + 0x800;
        fp.seek(ofs)
 
        bml = []
        for file in files:
 
            #Seek to next non-zero byte
            while fp.tell() < size:
                byte = struct.unpack('B', fp.read(1))[0]
                if byte == 0:
                    continue
                fp.seek(-1, os.SEEK_CUR)
                break
 
            #Read and decompress the file
            bytes = fp.read(file["compressed_size"])
            bml.append({
                "filename" : file["filename"],
                "bytes" : prs_decompress(bytes)
            })
 
        return bml

# struct bml_header_s {
#   uint8_t unused[4];
#   uint32_t num_files;
#   uint32_t unk; // 0x00000150, magic number?
#   uint8_t unused2[52];
# };
def extract_header(filename):

    if not os.path.exists(filename):
        return None

    with open(filename, "rb") as fp:
 
        fp.seek(0, os.SEEK_END)
        size = fp.tell()
        print("Size:", size)
 
        fp.seek(0)
        header_bytes = fp.read(64)
        s = struct.unpack('>4sII52s', header_bytes)

        print("unused 4 bytes:",    s[0])
        print("num_files 4 bytes:", s[1])
        print("unkown 4 bytes:",    s[2])
        print("unkown 52 bytes:",   s[3])

# bml_archive('bm_ene_re2_flower_a.bml')
# extract_header('bm_ene_re2_flower_a.bml')

def main():

    extract_header(sys.argv[1])

if __name__ == "__main__":
    main()
