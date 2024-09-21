import os
import json
import pandas as pd

def extract_lora_metadata(filename):
    """
    Extracts metadata from a LoRa file in .safetensors format.
    Args:
        filename: The name of the LoRa file.
    Returns:
        Dictionary with the extracted metadata, or None on error.
    """
    try:
        with open(filename, 'rb') as f:
            data = f.read(1000000)  # Read the first part of the file, which contains metadata

            # Find the start of the metadata
            start = data.find(b'"__metadata__":')
            if start == -1:
                return None

            # Find the end of the metadata by locating the last closing curly bracket "}"
            count = 1
            end = start + 1
            for i in range(start + 1, len(data)):
                if data[i] == ord('{'):
                    count += 1
                elif data[i] == ord('}'):
                    count -= 1
                if count == 0:
                    end = i
                    break

            metadata_str = data[start-1:end+1].decode('utf-8')

            # Convert the metadata JSON string to a dictionary
            try:
                metadata = json.loads(metadata_str)
                return metadata
            except json.JSONDecodeError:
                print(f"Error decoding JSON for file: {filename}")
                return None
    except Exception as e:
        print(f"Error reading file: {filename} - {str(e)}")
        return None

def sum_img_counts(metadata):
    """Calculates the total sum of 'img_count' values in nested dictionaries."""
    try:
        total_img_count = 0
        ss_dataset_dirs = json.loads(metadata["__metadata__"]["ss_dataset_dirs"])
        for value in ss_dataset_dirs:
            total_img_count += ss_dataset_dirs[value].get('img_count', 0)
        return total_img_count
    except:
        return None

def collect_metadata_from_directory(start_directory):
    """Recursively collects metadata from all .safetensors files in a directory."""
    data = []
    for root, _, files in os.walk(start_directory):
        for file in files:
            if file.endswith(".safetensors"):
                file_path = os.path.join(root, file)
                metadata = extract_lora_metadata(file_path)
                if metadata:
                    # Extract necessary parameters
                    file_relative_path = os.path.relpath(os.path.dirname(file_path), start_directory)
                    file_name_without_ext = os.path.splitext(file)[0]
                    print(file_name_without_ext)

                    # Add the extracted data to the list
                    row = {
                        'File Path': file_relative_path,
                        'File Name': file_name_without_ext,
                        'ss_steps': metadata["__metadata__"].get("ss_steps"),
                        'ss_unet_lr': metadata["__metadata__"].get("ss_unet_lr"),
                        'ss_network_alpha': metadata["__metadata__"].get("ss_network_alpha"),
                        'ss_network_dim': metadata["__metadata__"].get("ss_network_dim"),
                        'ss_sd_model_name': metadata["__metadata__"].get("ss_sd_model_name"),
                        'ss_learning_rate': metadata["__metadata__"].get("ss_learning_rate"),
                        'ss_epoch': metadata["__metadata__"].get("ss_epoch"),
                        'ss_network_module': metadata["__metadata__"].get("ss_network_module"),
                        'ss_lr_scheduler': metadata["__metadata__"].get("ss_lr_scheduler"),
                        'ss_optimizer': metadata["__metadata__"].get("ss_optimizer"),
                        'img_count': sum_img_counts(metadata)
                    }
                    data.append(row)
    
    # Convert to pandas DataFrame
    df = pd.DataFrame(data)
    return df

# Request the start directory from the user
start_directory = input("Enter the path to the directory for processing: ")
metadata_df = collect_metadata_from_directory(start_directory)

# Save the results to an Excel file
metadata_df.to_excel("result.xlsx", index=False)
print("Data saved to result.xlsx")
