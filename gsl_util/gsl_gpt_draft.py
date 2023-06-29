import os
import struct
import sys

HEADER_ENTRY_SIZE = 0x30  # Size of each header entry in bytes
BLOCK_SIZE = 2048  # Size of a block in bytes

def parse_contents(fp):
    fp.seek(0, os.SEEK_END)
    size = fp.tell()
    fp.seek(0)

    headers = []
    max_offset = 0

    while fp.tell() < size:
        data = fp.read(HEADER_ENTRY_SIZE)
        if not data:
            break

        name, offset, length, unused = struct.unpack('>32sII8s', data)
        name = name.decode('ascii').rstrip(' \t\r\n\0')

        if not name:
            break

        offset *= BLOCK_SIZE
        max_offset = max(max_offset, offset)

        header = {
            'filename': name,
            'offset': offset,
            'length': length,
            'unused': unused
        }
        headers.append(header)

    if size > max_offset:
        size = max_offset

    contents = []
    for header in headers:
        fp.seek(header['offset'])
        chunk = fp.read(header['length'])
        contents.append({'filename': header['filename'], 'bytes': chunk})

    return contents

def gsl_parse(filename):
    if not os.path.exists(filename):
        return None

    with open(filename, 'rb') as fp:
        return parse_contents(fp)

def export_file(file_dict, directory):
    full_path = os.path.join(directory, file_dict['filename'])

    with open(full_path, 'wb') as f:
        f.write(file_dict['bytes'])

def unpack_gsl(filename, unpack_dir):
    print(f"Unpacking: {filename} to: {unpack_dir}")
    text_file = f"{unpack_dir}.txt"

    if not os.path.exists(unpack_dir):
        os.mkdir(unpack_dir)

    with open(text_file, 'w') as tx:
        contents = gsl_parse(filename)
        for file in contents:
            name = file['filename']
            tx.write(f"{name}\n")
            export_file(file, unpack_dir)

def pack_gsl(unpack_dir, filename):
    print(f"Packing: {unpack_dir} to file: {filename}")
    text_file = f"{unpack_dir}.txt"

    if not os.path.exists(unpack_dir) or not os.path.exists(text_file):
        print("Need both unpacked directory and .txt file of the same name to pack.")
        return

    with open(text_file, 'r') as tx:
        file_names = [line.strip('\n') for line in tx]

    contents = []
    offset = 12288  # Starting offset for files
    header_section = bytearray()

    for item in file_names:
        path = os.path.join(".", unpack_dir, item)
        with open(path, 'rb') as f:
            raw_bytes = f.read()
            contents.append({'filename': item, 'bytes': raw_bytes})

            header = {
                'filename': bytes(item, 'ascii'),
                'offset': offset // BLOCK_SIZE,
                'length': len(raw_bytes),
                'unused': bytes([0] * 8)
            }

            packed_entry = struct.pack('>32sII8s', header['filename'], header['offset'], header['length'], header['unused'])
            header_section += packed_entry

            offset += header['length']
            if header['length'] % BLOCK_SIZE != 0:
                offset += BLOCK_SIZE - (header['length'] % BLOCK_SIZE)

    h_len = len(header_section)

    rem = 12288 - (h_len % 12288) if h_len % 12288 != 0 else 0
    header_format = f"{h_len+rem}s"
    padded_header = struct.pack(header_format, header_section)

    file_section = bytearray()
    for item in contents:
        size = len(item['bytes'])
        arr = bytearray(item['bytes'])

        diff = (2048 - (size % 2048)) % 2048
        format_str = f">{size+diff}s"
        padded = struct.pack(format_str, arr)
        file_section += bytes(padded)

    combined = padded_header + file_section

    with open(filename, 'wb') as out:
        out.write(combined)

def find_and_print(folder, target):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.gsl'):
                gsl_path = os.path.join(root, file)
                gsl_contents = gsl_parse(gsl_path)
                for item in gsl_contents:
                    if target in item['filename']:
                        print(f"{file}/{item['filename']}")

def list_contents(filename):
    contents = gsl_parse(filename)
    for item in contents:
        print(item['filename'])

def print_usage():
    print("Usage:\n")
    print("# Unpack .gsl archive to folder/textfile pair")
    print("python gsl.py unpack <input_file> <unpack_dir>\n")
    print("# Pack folder/textfile pair to .gsl archive")
    print("python gsl.py pack <unpacked_dir> <out_file>\n")
    print("# Search all gsl archives in directory for contents with a keyword in the filename")
    print("python gsl.py find <directory> <keyword>\n")
    print("# List contents of an archive")
    print("python gsl.py list <input_file>\n")

def main():
    if len(sys.argv) <= 2:
        print_usage()
        return

    if sys.argv[1] == 'pack':
        if len(sys.argv) != 4:
            print("Invalid number of arguments for pack.")
            return

        unpacked_dir = sys.argv[2]
        out_file = sys.argv[3]

        if not os.path.exists(unpacked_dir):
            print("<unpack_dir> does not exist.")
        else:
            pack_gsl(unpacked_dir, out_file)
        return

    elif sys.argv[1] == 'unpack':
        if len(sys.argv) != 4:
            print("Invalid number of arguments for unpack.")
            return

        input_file = sys.argv[2]
        unpack_dir = sys.argv[3]

        if not os.path.exists(input_file):
            print("<input_file> does not exist.")
        else:
            unpack_gsl(input_file, unpack_dir)
        return

    elif sys.argv[1] == 'find':
        if len(sys.argv) != 4:
            print("Invalid number of arguments for find.")
            return

        directory = sys.argv[2]
        keyword = sys.argv[3]

        if not os.path.exists(directory):
            print("<directory> does not exist.")
        else:
            find_and_print(directory, keyword)
        return

    elif sys.argv[1] == 'list':
        if len(sys.argv) != 3:
            print("Invalid number of arguments for list.")
            return

        input_file = sys.argv[2]

        if not os.path.exists(input_file):           
            print("<input_file> does not exist.")
        else:
            list_contents(input_file)
        return

    print_usage()

if __name__ == "__main__":
    main()