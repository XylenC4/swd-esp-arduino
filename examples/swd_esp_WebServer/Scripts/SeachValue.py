import struct
import os
from collections import defaultdict

def extract_values(data, formats, value_range):
    found = {}
    for fmt, size in formats:
        for i in range(0, len(data) - size + 1):
            chunk = data[i:i+size]
            try:
                value = struct.unpack(fmt, chunk)[0]
                if value in value_range:
                    found[i] = value  # Store the value with its offset
            except struct.error:
                continue
    return found

def main():
    # Directory containing the files
    directory = 'FileSearch'
    
    # Define the formats for extraction
    formats = [
        ('>b', 1),   # int8 (big-endian)
        ('>B', 1),   # uint8 (big-endian)
        ('>h', 2),   # int16 (big-endian)
        ('>H', 2),   # uint16 (big-endian)
        ('>i', 4),   # int32 (big-endian)
        ('>I', 4),   # uint32 (big-endian)
        ('>f', 4),   # float32 (big-endian)
        ('>d', 8),   # float64 (big-endian)
        ('>c', 1),   # char (big-endian)
    ]

    # Dictionary to hold values from each file
    file_values = {}

    # Read all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.bin'):
            number_str = filename[:-4]  # Remove the .bin extension
            if not number_str.isdigit():
                raise ValueError(f"Invalid filename '{filename}': must be a number.")
            
            number = int(number_str)
            value_range = set(range(max(0, number - 1), number + 2))  # n-1, n, n+1

            with open(os.path.join(directory, filename), 'rb') as f:
                data = f.read()
                values = extract_values(data, formats, value_range)
                file_values[filename] = values

    # Collect common values across all files
    common_values = defaultdict(list)
    all_offsets = set()

    # Gather all offsets from all files
    for filename, values in file_values.items():
        for offset in values.keys():
            all_offsets.add(offset)

    # Check for common values at the same offsets across all files
    for offset in all_offsets:
        values_at_offset = [file_values[filename].get(offset) for filename in file_values if offset in file_values[filename]]
        if len(values_at_offset) == len(file_values):  # Check if all files have a value at this offset
            common_values[offset] = values_at_offset

    # Print common values found
    if common_values:
        print("✅ Common values found at the same offsets across all files:")
        for offset, values in sorted(common_values.items()):
            # Print values at both the original offset and the offset + 0x20000000 inline
            adjusted_offset = offset + 0x20000000
            print(f"  At Offset {hex(offset)} (Adjusted: {hex(adjusted_offset)}): Values = {values}")
    else:
        print("❌ No common values found at the same offsets across the files.")

if __name__ == '__main__':
    main()
