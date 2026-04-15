import json
from MRTD import encode_record

INPUT_FILE = "records_decoded.json"
OUTPUT_FILE = "records_encoded.json"

def main():
    with open(INPUT_FILE, "r") as f:
        records = json.load(f)

    with open(OUTPUT_FILE, "w") as f:
        for record in records:
            encoded = encode_record(record)
            f.write(encoded + "\n")

    print("Finished encoding 10,000 records")

if __name__ == "__main__":
    main()
