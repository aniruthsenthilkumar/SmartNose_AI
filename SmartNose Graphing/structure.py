import pandas as pd

def read_json_file(filename):
    try:
        with open(filename, 'r') as file:
            data = pd.read_json(file)
        return data
    except FileNotFoundError:
        print("File not found.")

def main():
    filename = "test.bmespecimen"
    data = read_json_file(filename)
    if data is not None:
        print("Data from JSON file:")
        print(data)
        # If JSON file has nested objects, you can normalize them using the following:
        normalized_data = pd.json_normalize(data)
        print("Normalized Data:")
        # print(normalized_data)

if __name__ == "__main__":
    main()
