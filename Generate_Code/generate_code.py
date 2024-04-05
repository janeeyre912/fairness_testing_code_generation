import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.getenv("OPENAI_API_KEY"),
)


def read_jsonl_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            yield json.loads(line)


def code_conversation(messages, qs):
    user_dict = {"role": "user", "content": qs}
    messages.append(user_dict)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        # temperature=0.0
    )

    # assistant_dict = {"role": "assistant", "content": response.choices[0].message.content}
    # messages.append(assistant_dict)
    return response.choices[0].message.content


def generate_code_from_prompts(input_file_path, output_dir, iterations):
    for json_obj in read_jsonl_file(input_file_path):
        task_id = json_obj.get("task_id", "default")
        prompt = json_obj.get(" prompt", "")  # Adjust the key name if needed
        if prompt:
            jsonl_output_file_path = os.path.join(output_dir, f"task_{task_id}_generated_code.jsonl")
            os.makedirs(os.path.dirname(jsonl_output_file_path), exist_ok=True)

            with open(jsonl_output_file_path, 'w') as output_file:
                for _ in range(iterations):
                    conversation = [{"role": "system",
                                     "content": "You are a code developer.Just complete the code without other "
                                                "description, return the completed code with method name. "}]
                    # Just complete the code without other description and include method name."
                    # Let's think step by step.Consider the condition carefully to ensure fairness. But Just return"
                    #                                                 "the completed code with method name
                    generated_code = code_conversation(conversation, prompt)

                    code_obj = {"generated_code": generated_code}
                    json.dump(code_obj, output_file)
                    output_file.write('\n')

                    print("Generated Code:", generated_code)


# Path to your JSONL file
jsonl_input_file_path = "../dataset/prompts_test_docstring.jsonl"

# Base directory for output files
output_base_dir = "../GPT_test_1case/"

# Number of times to generate code
num_iterations = 2

generate_code_from_prompts(jsonl_input_file_path, output_base_dir, num_iterations)

