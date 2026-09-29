import struct
import sys

def parse_exif(filename):
    with open(filename, 'rb') as f:
        data = f.read()

    # Find Exif header (APP1)
    idx = data.find(b'\xff\xe1')
    if idx == -1:
        print("No APP1")
        return

    length = struct.unpack(">H", data[idx+2:idx+4])[0]
    exif_data = data[idx+4:idx+2+length]
    
    if exif_data[:4] != b'Exif':
        print("Not Exif", exif_data[:6])
        return
        
    tiff_data = exif_data[6:]
    endian = tiff_data[:2]
    if endian == b'II':
        fmt = '<'
    elif endian == b'MM':
        fmt = '>'
    else:
        print("Unknown endian", endian)
        return

    def get_tag_type_len(type_id):
        return {1:1, 2:1, 3:2, 4:4, 5:8, 7:1, 9:4, 10:8}.get(type_id, 1)

    def parse_ifd(offset, name="IFD"):
        if offset > len(tiff_data) - 2: return
        num_tags = struct.unpack(fmt + "H", tiff_data[offset:offset+2])[0]
        print(f"\n{name} at {offset} with {num_tags} tags")
        
        for i in range(num_tags):
            entry_offset = offset + 2 + i * 12
            if entry_offset > len(tiff_data) - 12: break
            tag_id, type_id, count, val_offset = struct.unpack(fmt + "HHII", tiff_data[entry_offset:entry_offset+12])
            
            size = count * get_tag_type_len(type_id)
            if size <= 4:
                raw_val = tiff_data[entry_offset+8:entry_offset+8+size]
            else:
                raw_val = tiff_data[val_offset:val_offset+size]
                
            print(f"Tag: {hex(tag_id)}, Type: {type_id}, Count: {count}, Raw: {raw_val.hex()}")
            
            if tag_id == 0x8769: # ExifOffset
                parse_ifd(val_offset, "Exif SubIFD")
            if tag_id == 0x8825: # GPSInfo
                parse_ifd(val_offset, "GPS IFD")

    parse_ifd(struct.unpack(fmt + "I", tiff_data[4:8])[0], "IFD0")

parse_exif(sys.argv[1])
