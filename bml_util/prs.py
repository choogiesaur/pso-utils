def prs_compress(data):
    compressed_data = bytearray()
    length = len(data)
    pos = 0

    while pos < length:
        rep_offset = 1
        rep_length = 2
        max_offset = min(pos, 0x1000)

        for offset in range(1, max_offset + 1):
            if data[pos:pos + rep_length] == data[pos - offset:pos - offset + rep_length]:
                while pos + rep_length < length and rep_length < 0x12 and data[pos + rep_length] == data[pos - offset + rep_length]:
                    rep_length += 1

                if rep_length > 2:
                    break

                rep_length = 1

        if rep_length > 2:
            rep_offset = offset

        if rep_length == 1:
            compressed_data.append(0)
            compressed_data.append(data[pos])
            pos += 1
        else:
            rep_offset -= 1
            compressed_data.append(((rep_length - 3) << 4) | (rep_offset >> 8))
            compressed_data.append(rep_offset & 0xFF)
            compressed_data.append(rep_length - 3)
            pos += rep_length

    return compressed_data


def prs_decompress(compressed_data):
    decompressed_data = bytearray()
    length = len(compressed_data)
    pos = 0

    while pos < length:
        command_byte = compressed_data[pos]
        pos += 1

        if command_byte == 0:
            decompressed_data.append(compressed_data[pos])
            pos += 1
        else:
            rep_offset = ((command_byte & 0xF) << 8) | compressed_data[pos]
            rep_length = (command_byte >> 4) + 3
            pos += 1

            for i in range(rep_length):
                decompressed_data.append(decompressed_data[-rep_offset])

    return decompressed_data
