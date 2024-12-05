import json


# Utility Functions
def load_jsonl_file(file_path):
    """Load actions from a JSON Lines file."""
    with open(file_path, 'r') as file:
        return [json.loads(line) for line in file]

def load_json_file(file_path):
    """Load a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def save_to_jsonl_file(data, file_path):
    """Save a list of data to a JSON Lines file."""
    with open(file_path, 'w') as file:
        for item in data:
            json.dump(item, file)
            file.write('\n')