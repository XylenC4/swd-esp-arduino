import os
import requests

# Configuration
SRAM_URL = "http://192.168.178.46/SRAM.bin"  # URL to download SRAM data
PREVIOUS_FILE = "SRAM_1.bin"
NEW_FILE = "SRAM_MaskCompare.bin"
CHANGED_FILE = "SRAM_MaskCompare2.bin"
MASK_FILE = "mask.bin"

def download_sram_data(url):
    try:
        # Send a GET request to the specified URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error downloading data: {e}")
        return None

def save_to_binary_file(data, filename):
    # Save the data to a binary file
    with open(filename, "wb") as f:
        f.write(data)
    print(f"Data saved to {filename}")

def load_binary_file(filename):
    # Load data from a binary file
    with open(filename, "rb") as f:
        return f.read()

def load_mask_file(filename):
    # Load the mask data from a binary file
    with open(filename, "rb") as f:
        return f.read()

def find_changed_data(old_data, new_data, mask_data):
    # Create a bytearray for the changed data
    changed_data = bytearray()
    
    # Compare old and new data with the mask
    for i in range(len(new_data)):
        if i < len(mask_data) and mask_data[i] == 0xFF:
            changed_data.append(0x00)  # Exclude this byte, write 0x00
        else:
            if i < len(old_data) and old_data[i] == new_data[i]:
                changed_data.append(0x00)  # Write 0x00 if the data is unchanged
            else:
                changed_data.append(new_data[i])  # Write the new data if changed

    # If the new data is longer than the old data, fill the rest with 0x00
    if len(new_data) > len(old_data):
        changed_data.extend([0x00] * (len(new_data) - len(old_data)))

    return changed_data

def main():
    # Download the new SRAM data from the web server
    memory_data = download_sram_data(SRAM_URL)

    if memory_data is None:
        print("Failed to download SRAM data. Exiting.")
        return

    # Save the new memory data to a binary file
    save_to_binary_file(memory_data, NEW_FILE)

    # Load the previous data
    previous_data = load_binary_file(PREVIOUS_FILE)

    # Load the mask data
    mask_data = load_mask_file(MASK_FILE)

    # Find changed data using the mask
    changed_data = find_changed_data(previous_data, memory_data, mask_data)

    # Save the changed data to a new binary file
    save_to_binary_file(changed_data, CHANGED_FILE)

if __name__ == '__main__':
    main()