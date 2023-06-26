import os
import struct
import sys
import prs

def unpack_bml(filename, unpack_dir):
    if not os.path.exists(filename):
        return None

    with open(filename, "rb") as file:
        file_size = os.path.getsize(filename)

        file.seek(4)
        file_count = struct.unpack('i', file.read(4))[0]
        file.seek(0x40)

        bml_entries = []
        for _ in range(file_count):
            entry_data = file.read(0x34)
            entry = struct.unpack('>32sIIIII', entry_data)
            file.read(0x0c)

            name = entry[0].decode('ascii').rstrip(' \t\r\n\0')
            compressed_size = entry[1]
            decompressed_size = entry[3]
            pvm_compressed_size = entry[4]
            pvm_decompressed_size = entry[5]

            entry_info = {
                "filename": name,
                "compressed_size": compressed_size,
                "decompressed_size": decompressed_size
            }

            if pvm_compressed_size:
                basename = os.path.splitext(name)[0]
                pvm_entry = {
                    "filename": f"{basename}.pvm",
                    "compressed_size": pvm_compressed_size,
                    "decompressed_size": pvm_decompressed_size
                }
                bml_entries.append(pvm_entry)

            bml_entries.append(entry_info)

        bml_data = []
        offset = file.tell()
        offset = (0xFFFFF800 & offset) + 0x800
        file.seek(offset)

        while file.tell() < file_size:
            byte = struct.unpack('B', file.read(1))[0]
            if byte != 0:
                file.seek(-1, os.SEEK_CUR)
                bytes_data = file.read(bml_entries[len(bml_data)]["compressed_size"])
                if bml_entries[len(bml_data)]["filename"].endswith(".pvm"):
                    decompressed_data = prs.prs_decompress(bytes_data)
                else:
                    decompressed_data = bytes_data
                bml_data.append({
                    "filename": bml_entries[len(bml_data)]["filename"],
                    "bytes": decompressed_data
                })

        for file_info in bml_data:
            file_path = os.path.join(unpack_dir, file_info["filename"])
            with open(file_path, "wb") as output_file:
                output_file.write(file_info["bytes"])

        order_file = os.path.join(unpack_dir, "order.txt")
        with open(order_file, "w") as order_fp:
            for file_info in bml_data:
                order_fp.write(file_info["filename"] + "\n")

        return bml_data


def pack_bml(unpack_dir, filename, order_file):
    print("Packing:", unpack_dir, "to file:", filename)
    with open(order_file, "r") as order_fp:
        file_names = [line.strip() for line in order_fp.readlines()]

    contents = []
    offset = 64 + (len(file_names) * 64)

    for item in file_names:
        path = os.path.join(unpack_dir, item)
        with open(path, "rb") as f:
            raw_bytes = f.read()
            if item.endswith(".pvm"):
                compressed_data = prs.prs_compress(raw_bytes)
                contents.append({"filename": item, "bytes": compressed_data})
            else:
                contents.append({"filename": item, "bytes": raw_bytes})

            file_entry = struct.pack(
                ">32sIIIII12s",
                item.encode("ascii"),
                len(raw_bytes),
                0,
                len(raw_bytes),
                0,
                0,
                b"\x00" * 12,
            )

            offset += len(raw_bytes)
            offset += 2048 - (len(raw_bytes) % 2048)

    with open(filename, "wb") as out:
        out.write(struct.pack(">4sII52s", b"\x00" * 4, len(file_names), 0x150, b"\x00" * 52))

        for file_entry in contents:
            out.write(file_entry["filename"].encode("ascii")[:32])
            out.write(struct.pack(">I", len(file_entry["bytes"])))
            out.write(struct.pack(">I", 0))
            out.write(struct.pack(">I", len(file_entry["bytes"])))
            out.write(struct.pack(">I", 0))
            out.write(struct.pack(">I", 0))
            out.write(b"\x00" * 12)

            out.write(file_entry["bytes"])

        padding_size = (2048 - (offset % 2048)) % 2048
        out.write(b"\x00" * padding_size)

    print("BML archive repacked:", filename)


def main():
    if len(sys.argv) < 2:
        print("Usage: python bml.py <bml_file>")
        return

    filename = sys.argv[1]

    if not os.path.exists(filename):
        print(f"Error: File '{filename}' does not exist.")
        return

    print(f"Processing BML archive: {filename}\n")

    # Extracting BML archive
    unpack_dir = os.path.splitext(filename)[0]
    os.makedirs(unpack_dir, exist_ok=True)
    extracted_files = unpack_bml(filename, unpack_dir)

    if extracted_files is None:
        print("Error: Failed to extract BML archive.")
    else:
        print("Extracted files:")
        for file_info in extracted_files:
            print(file_info["filename"])

        if len(sys.argv) >= 5 and sys.argv[2] == "-p":
            new_bml_filename = sys.argv[3]
            order_file = sys.argv[4]

            # Repack the extracted files into a new BML archive
            pack_bml(unpack_dir, new_bml_filename, order_file)
            print(f"\nBML archive repacked: {new_bml_filename}")


if __name__ == "__main__":
    main()
