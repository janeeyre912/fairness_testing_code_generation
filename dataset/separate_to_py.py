import json
import os

# Define the path to your JSON Lines file
jsonl_file_path = 'prompts_test.jsonl'

# Define the target folder for the Python files
target_folder = 'separate_prompt'

# Ensure the target folder exists
os.makedirs(target_folder, exist_ok=True)

# Open the JSON Lines file
with open(jsonl_file_path, 'r') as file:
    # Iterate over each line in the file
    for line in file:
        # Parse the JSON data from the current line
        data = json.loads(line)

        # Extract the task ID and prompt content
        task_id = data['task_id']
        prompt_content = data['prompt']

        # Define the filename for the Python file, including the target folder in the path
        python_file_name = os.path.join(target_folder, f'task_{task_id}.py')

        # Write the prompt content to a new Python file
        with open(python_file_name, 'w') as python_file:
            python_file.write(prompt_content)

print(f"Python files have been successfully created in the '{target_folder}' folder.")
