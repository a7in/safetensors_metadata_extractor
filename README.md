# Safetensors Metadata Extractor

A utility for extracting metadata from `.safetensors` LoRa files and saving the information into an Excel file.
The utility extracts the following parameters from the LoRa of those trained using kohya_ss:  
  ss_steps  
  ss_unet_lr  
  ss_network_alpha  
  ss_network_dim  
  ss_sd_model_name  
  ss_learning_rate  
  ss_epoch  
  ss_network_module  
  ss_lr_scheduler  
  ss_optimizer  
  img_count  

## Features

- Recursively searches a specified directory for `.safetensors` files.
- Extracts relevant metadata and aggregates it into a structured format.
- Saves the extracted data into an Excel file (`result.xlsx`).

## Requirements

This project requires Python 3.x and the following libraries:

- pandas
- openpyxl

You can install the required libraries using the following command:

pip install -r requirements.txt

## Usage:
1. Clone the repository or download the source code.
2. Navigate to the project directory.
3. Run the script:
  python safetensors_metadata_extractor.py
4. When prompted, enter the path to the directory containing the .safetensors files you want to process.
5. The extracted metadata will be saved in result.xlsx in the same directory as the script.

## License:
This project is licensed under the MIT License. See the LICENSE file for details.
