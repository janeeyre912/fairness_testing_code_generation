import json
import os
import re
import sys

def parse_line(line):
    """
    Parses a line of the file and extracts the variant, attribute, and checks if inconsistencies are found.
    """
    parts = line.strip().split(':')
    variant_attribute, status = parts[0].strip(), parts[1].strip()
    variant, attribute_with_prefix = variant_attribute.split(', ')
    variant_number = variant.split(' ')[-1]
    attribute = re.search(r"Attribute '([^']+)'", attribute_with_prefix).group(1)
    has_inconsistencies = status == 'Inconsistencies found.'
    return variant_number, attribute, has_inconsistencies


def parse_line_after_debias(line):
    """
    Parses a line of the file and extracts the variant, attribute, and inconsistency status.
    """
    parts = line.strip().split(':')
    variant_attribute, status = parts[0], parts[1].strip()
    variant, attribute_with_prefix = variant_attribute.split(', ')
    # Extract the variant number for consistent formatting in the output
    variant_number = variant.split(' ')[-1]
    # Remove the word "Attribute" from the attribute name
    attribute = attribute_with_prefix.replace("Attribute '", "").replace("'", "")
    return variant_number, attribute, status


## fixed issue with extracting number from filename
def extract_number_from_filename(filepath):
    """
    Extracts the numeric part from the filename using a regular expression.
    """
    filename = filepath.split("/")[-1] if "/" in filepath else filepath
    match = re.search(r'(\d+)', filename)
    return match.group(0) if match else None

def process_file_to_jsonl(filepath, output_dir, max_variant_num):
    """
    Reads a file, processes each line, and writes the results to a JSONL file in the specified output directory.
    """
    number = extract_number_from_filename(filepath)
    if number is None:
        print(f"Could not extract number from filename {filepath}")
        return

    jsonl_filename = f"bias_info{number}.jsonl"
    jsonl_filepath = os.path.join(output_dir, jsonl_filename)

    # Initialize all variants with "failed"
    variants = {str(i): {"status": "failed", "attributes": ""} for i in range(1, max_variant_num + 1)}

    with open(filepath, 'r') as file:
        for line in file:
            variant_number, attribute, has_inconsistencies = parse_line(line)
            variant_int = int(variant_number)

            if variant_int < 1 or variant_int > max_variant_num:
                continue

            # Update variant status and attributes
            if has_inconsistencies:
                attributes = variants[variant_number]["attributes"]
                variants[variant_number]["attributes"] = attribute if not attributes else f"{attributes}, {attribute}" if attribute not in attributes else attributes
                variants[variant_number]["status"] = "inconsistencies_found"
            else:
                # Mark as having no inconsistencies if not already marked with an attribute
                if variants[variant_number]["status"] == "failed":
                    variants[variant_number]["status"] = "no_bias"

    with open(jsonl_filepath, 'w') as outfile:
        for variant_number, info in variants.items():
            output = {"variant": variant_number}
            if info["status"] == "inconsistencies_found":
                output["bias_info"] = info["attributes"]
            elif info["status"] == "no_bias":
                output["bias_info"] = "none"
            else:  # Failed variants
                output["bias_info"] = "failed"
            json.dump(output, outfile)
            outfile.write('\n')


def process_all_files_in_directory(directory, output_dir, variant_num):
    """
    Processes all CSV files in the given directory, converting each to a JSONL file in the output directory.
    """
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            csv_filepath = os.path.join(directory, filename)
            process_file_to_jsonl(csv_filepath, output_dir, variant_num)


# Directory containing the CSV files
input_dir = sys.argv[1]
# Directory where the JSONL files will be saved
output_dir = sys.argv[2]
# number of generated samples per N prompts
variant_num = int(sys.argv[3])
# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Process all CSV files in the input directory(for after debias)
process_all_files_in_directory(input_dir, output_dir, variant_num)
