import json
import os
from generate_code import read_jsonl_file, code_conversation
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.getenv("OPENAI_API_KEY"),
)


def extract_number_from_filename(filename):
    """Extracts the numeric part from the filename using a regular expression."""
    match = re.search(r'(\d+)', filename)
    return match.group(0) if match else None


def process_files_remove_bias(code_files_dir, bias_files_dir, output_base_dir):
    """Reads and combines information from code and bias JSONL files based on the task ID in filenames."""

    for code_filename in os.listdir(code_files_dir):
        task_id = extract_number_from_filename(code_filename)
        bias_filename = f"bias_info{task_id}.jsonl"  # Assuming a consistent naming convention

        code_file_path = os.path.join(code_files_dir, code_filename)
        bias_file_path = os.path.join(bias_files_dir, bias_filename)

        if os.path.exists(bias_file_path):
            for code_data, bias_data in zip(read_jsonl_file(code_file_path), read_jsonl_file(bias_file_path)):
                # Check if the bias info is empty; if not, combine the data
                bias_info = bias_data.get('bias_info')

                if not bias_info or bias_info == "failed" or bias_info == "none":
                    continue
                # if bias_data.get('bias_info'):  # Adjust this condition based on your bias data structure
                generated_code = code_data.get('generated_code')
                # bias_info = bias_data.get('bias_info')
                # Generate a unique filename for each task
                jsonl_output_file_path = os.path.join(output_base_dir,
                                                      f"task_{task_id}_generated_code_rm_bias.jsonl")
                # print("task_id", task_id)
                # Ensure the output directory exists
                os.makedirs(os.path.dirname(jsonl_output_file_path), exist_ok=True)

                # Open the output file in append mode to add new content without overwriting existing data
                with open(jsonl_output_file_path, 'a') as output_file:
                    conversation = [{"role": "system",
                                     "content": "You are a code developer. Just complete the code without other "
                                                "description and include method definition."}]
                    assistant_dict = {"role": "assistant", "content": generated_code}
                    conversation.append(assistant_dict)
                    # print(conversation)
                    prompt = "remove the bias in " + bias_info
                    # print(prompt)
                    generated_code = code_conversation(conversation, prompt)
                    # Create a JSON object with the generated code
                    code_obj = {"generated_code": generated_code}

                    # Write the JSON object to the output JSONL file
                    json.dump(code_obj, output_file)
                    output_file.write('\n')  # Add a newline to separate JSON objects


process_files_remove_bias("generated_code", "bias_info", "remove_bias_code")
