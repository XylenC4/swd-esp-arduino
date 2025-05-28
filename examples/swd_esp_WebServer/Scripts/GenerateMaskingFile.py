import os
import time
import requests

# Configuration
SRAM_URL = "http://192.168.178.46/SRAM.bin"  # URL to download SRAM data
ACQUISITION_INTERVAL = 1                     # Time in seconds between acquisitions
TOTAL_DURATION = 10                          # Total duration for acquisition in seconds

def download_sram_data(url, index):
    try:
        # Send a GET request to the specified URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        # Determine the filename
        base_filename = f"SRAM_{index}.bin"

        # Save the data to a binary file
        with open(base_filename, "wb") as f:
            f.write(response.content)
        print(f"Data saved to {base_filename}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading data: {e}")

def generate_mask_file(base_filename, num_files):
    # Read the first file to use as the reference
    with open(base_filename, "rb") as f:
        reference_data = f.read()

    # Initialize the mask with zeros
    mask = bytearray(len(reference_data))

    # Compare each subsequent file with the reference
    for i in range(2, num_files + 1):
        current_filename = f"SRAM_{i}.bin"
        
        if not os.path.exists(current_filename):
            print(f"File {current_filename} does not exist. Skipping.")
            continue

        with open(current_filename, "rb") as f:
            current_data = f.read()

        # Generate the mask
        for j in range(len(reference_data)):
            if j < len(current_data) and reference_data[j] != current_data[j]:
                mask[j] = 0xFF  # Mark as changed
            else:
                mask[j] = mask[j]  # Keep the previous value (0x00)

    # Save the mask to a file
    mask_filename = "mask.bin"
    with open(mask_filename, "wb") as f:
        f.write(mask)

    print(f"Mask file generated: {mask_filename}")

def main():
    # Calculate the number of acquisitions
    num_acquisitions = TOTAL_DURATION // ACQUISITION_INTERVAL

    for i in range(num_acquisitions):
        # Download SRAM data from the specified URL
        download_sram_data(SRAM_URL, i + 1)

        # Wait for the specified interval
        time.sleep(ACQUISITION_INTERVAL)

    # Generate the mask file after all data has been downloaded
    base_filename = "SRAM_1.bin"  # The first file to use as reference
    num_files = num_acquisitions    # Total number of files downloaded
    generate_mask_file(base_filename, num_files)

if __name__ == '__main__':
    main()