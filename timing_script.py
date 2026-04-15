import json
import time
import csv
import unittest
import subprocess
import sys

from MRTD import encode_record
import MRTDtest

INPUT_FILE = "records_decoded.json"
OUTPUT_CSV = "timing_results.csv"

def decode_record(mrz_string: str) -> dict:
    """Decode an MRZ string back into a record dict."""
    line1, line2 = mrz_string.split(";")

    country = line1[2:5]
    names = line1[5:].split("<<")
    last_name = names[0].replace("<", " ").strip()
    given_name = names[1].replace("<", " ").strip() if len(names) > 1 else ""

    passport_number = line2[0:9]
    country_code = line2[9:12]
    birth_date = line2[12:18]
    sex = line2[18]
    expiration_date = line2[19:25]
    personal_number = line2[25:]

    return {
        "line1": {"issuing_country": country, "last_name": last_name, "given_name": given_name},
        "line2": {"passport_number": passport_number, "country_code": country_code,
                  "birth_date": birth_date, "sex": sex, "expiration_date": expiration_date,
                  "personal_number": personal_number}
    }

# Load all 10,000 records once
with open(INPUT_FILE, "r") as f:
    data = json.load(f)

all_records = data["records_decoded"]

# Pre-encode all records so we have input ready for decode timing
all_encoded = [encode_record(r) for r in all_records]

# Define the subset sizes to test
sizes = [100] + list(range(1000, 11000, 1000))

results = []

for k in sizes:
    subset_decoded = all_records[:k]
    subset_encoded = all_encoded[:k]

    # --- ENCODE: WITHOUT tests ---
    start = time.perf_counter()
    encoded = [encode_record(r) for r in subset_decoded]
    time_encode_no_test = time.perf_counter() - start

    # --- ENCODE: WITH unit tests ---
    start = time.perf_counter()
    encoded_tested = [encode_record(r) for r in subset_decoded]
    subprocess.run([sys.executable, "-m", "unittest", "MRTDtest"],
                   capture_output=True)
    time_encode_with_test = time.perf_counter() - start

    # --- DECODE: WITHOUT tests ---
    start = time.perf_counter()
    decoded = [decode_record(e) for e in subset_encoded]
    time_decode_no_test = time.perf_counter() - start

    # --- DECODE: WITH unit tests ---
    start = time.perf_counter()
    decoded_tested = [decode_record(e) for e in subset_encoded]
    subprocess.run([sys.executable, "-m", "unittest", "MRTDtest"],
                   capture_output=True)
    time_decode_with_test = time.perf_counter() - start

    results.append({
        "num_records": k,
        "encode_no_test_s": round(time_encode_no_test, 6),
        "encode_with_test_s": round(time_encode_with_test, 6),
        "decode_no_test_s": round(time_decode_no_test, 6),
        "decode_with_test_s": round(time_decode_with_test, 6),
    })
    print(f"k={k} done")

# Write to CSV
with open(OUTPUT_CSV, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print(f"Done! Results saved to {OUTPUT_CSV}")