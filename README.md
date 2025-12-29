
# Method Module

This folder contains the core implementation of the project, including functions and classes for chaotic systems, coordinate scrambling, encryption, and dynamic sequence selection.

## Folder Structure

- **`FourD_chaos.py`**  
  Contains functions for calculating initial values and generating sequences for a 4D chaotic system.  
  - `calculate_chaos_initial_values`: Computes initial values for the chaotic system based on file size, vertex count, and other parameters.  
  - `calculate_chaos_sequence`: Solves the 4D chaotic system equations and generates chaotic sequences.

- **`dynamic_selection_sequence.py`**  
  Implements dynamic selection of chaotic sequences for scrambling.  
  - `dynamic_selection`: Dynamically selects two sequences for scrambling and two for encryption.

- **`coordinate_scrambling.py`**  
  Handles coordinate scrambling and unscrambling.  
  - `scramble_coordinates`: Scrambles the coordinates using chaotic sequences.  
  - `unscramble_coordinates`: Restores the original coordinates from scrambled ones.  
  - `extract_coordinates_from_shapefile`: Extracts coordinates and metadata from a shapefile.

- **`gmalg`**  
  Contains the implementation of the SM4 encryption algorithm.  
  - `CryptSM4`: Class for SM4 encryption and decryption.  
  - `SM4_ENCRYPT` and `SM4_DECRYPT`: Constants for encryption and decryption modes.

- **`calculate_sm4key_and_iv.py`**  
  Generates SM4 encryption keys and initialization vectors (IVs).  
  - `generate_key_and_iv_combined`: Generates a key and IV based on chaotic sequences.

- **`main.py`**  
  The main script that integrates all components.  
  - Reads shapefile data and extracts coordinates.  
  - Computes chaotic sequences and dynamically selects them.  
  - Scrambles coordinates, encrypts them using SM4, and performs decryption and unscrambling.  

## Key Features

1. **4D Chaotic System**  
   - Generates chaotic sequences for scrambling and encryption.  

2. **Dynamic Sequence Selection**  
   - Dynamically selects sequences for scrambling and encryption based on input data.

3. **Coordinate Scrambling**  
   - Scrambles and unscrambles coordinates using chaotic sequences.

4. **SM4 Encryption**  
   - Encrypts and decrypts data using the SM4 algorithm with dynamically generated keys and IVs.


## How to Use

1. Place the shapefile in the `data` directory.
2. Run the `main.py` script to process the shapefile.
3. The script will:
   - Extract coordinates.
   - Scramble, encrypt, decrypt, and unscramble the data.

## Dependencies

- Python 3.x
- NumPy
- Matplotlib

## Notes

- Ensure the `data` directory contains the required shapefiles.
- Modify the `shapefile_path` in `main.py` to point to the desired shapefile.
-  Due to the large size of the dataset, we provide a link for access: (https://download.geofabrik.de/)
