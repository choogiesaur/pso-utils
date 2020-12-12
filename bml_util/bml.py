import os
import struct
import sys

# afs/gsl/bml should generally be the same, 
# except for the endianness of the file offsets 
# and sizes for each file entry
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

# Extract the first 64 bytes, BML header
def extract_header(fp):

    # struct bml_header_s {
    #   uint8_t unused[4];
    #   uint32_t num_files;
    #   uint32_t unk; // 0x00000150, magic number?
    #   uint8_t unused2[52];
    # };

    fp.seek(0, os.SEEK_END)
    size = fp.tell()
    print("Size:", size)

    fp.seek(0)
    header_bytes = fp.read(64)
    s = struct.unpack('>4sII52s', header_bytes)

    return s

# Extract a 64 byte file entry at given offset
def extract_file_entry(fp, offset):

    # struct bml_file_table_entry_s {
    #   uint8_t  filename[32];
    #   uint32_t compressed_size;
    #   uint32_t unused1;
    #   uint32_t decompressed_size;
    #   uint32_t gvm_compressed_size;   # if this 
    #   uint32_t gvm_decompressed_size; # and this are > 0, there is a .gvm following this file
    #   uint8_t  unused[12]
    # };

    fp.seek(offset)
    print("0x"+str(fp.tell()))

    entry_bytes = fp.read(64)
    s = struct.unpack('>32sIIIII12s', entry_bytes)

    return s

def print_file_entry(file_entry):
    print(file_entry[0].decode('ascii').rstrip(' \t\r\n\0'))
    print('compressed_size:',file_entry[1])
    print('unused1:',file_entry[2])
    print('decompressed_size:',file_entry[3])
    print('gvm_compressed_size:',file_entry[4])
    print('gvm_decompressed_size:',file_entry[5])
    print()

def main():

    filename = sys.argv[1]

    if not os.path.exists(filename):
        return None

    with open(filename, "rb") as fp:

        # Extract BML header
        header = extract_header(fp)
        file_count = header[1]
        print('File Count:', file_count, '\n')

        # Starting right after header, extract n=file_count file_entries
        offset = 64
        for i in range(file_count):
            file_entry = extract_file_entry(fp, offset)

            print_file_entry(file_entry)
            offset += 64

if __name__ == "__main__":
    main()
