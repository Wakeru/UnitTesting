import json
from MRTD import encode_record

INPUT_FILE = "records_decoded.json"
OUTPUT_FILE = "records_encoded.json"

def main():
    with open(INPUT_FILE, "r") as f:
        data = json.load(f)
        records = data["records_decoded"]

    with open(OUTPUT_FILE, "w") as f:
        for record in records:
            encoded = encode_record(record)
            f.write(encoded + "\n")

    print(f"Finished encoding {len(records)} records")

if __name__ == "__main__":
    main()