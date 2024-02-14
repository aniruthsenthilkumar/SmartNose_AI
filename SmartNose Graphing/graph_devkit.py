import json

def open_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("File not found.")
    except json.JSONDecodeError:
        print("JSON decoding error. Please check if the file contains valid JSON data.")

# Example usage:
file_path = "test.bmespecimen"  # Change this to the path of your JSON file
json_data = open_json_file(file_path)
if json_data:
    pass

for key in json_data:
    print(key)

print('\n')

for key in json_data['data']:
    print(key)

print('\n')

cycle_ids = []
for key in json_data['data']['cycles']:
    print(key['id'])
    cycle_ids.append(key['id'])

print(len(cycle_ids))
# for key in json_data['data']['specimenDataPoints']:
#     print(key)

