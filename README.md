# MRTD Testing Project

## 📌 Overview
This project implements and tests basic validation and processing functions for Machine Readable Travel Documents (MRTDs) based on simplified ICAO Doc 9303 standards.

The project focuses on unit testing, code coverage, and mutation testing.

---

## 📁 Project Structure

- `MRTD.py` → Implementation of MRTD validation functions  
- `MRTDtest.py` → Unit test cases  
- `coverage report` → Test coverage output (>80%)  
- `MutPy results` → Mutation testing results  

---

## ⚙️ Implemented Functions

The following functions are implemented in `MRTD.py`:

1. `validate_passport_number`  
2. `validate_nationality_code`  
3. `validate_date_of_birth`  
4. `calculate_check_digit`  

Additional stub functions:
- `scan_passport()` (hardware simulation)  
- `fetch_passport_record()` (database simulation)  

---

## 🧪 Testing

- Unit tests are written in `MRTDtest.py`
- Mocking is used for hardware and database functions
- Multiple test cases ensure:
  - Statement coverage
  - Branch coverage
  - Condition coverage

---

## 📊 Coverage

Test coverage was measured using `coverage.py`.

Requirement:
- Minimum coverage: **80%**

---

## 🧬 Mutation Testing

Mutation testing was performed using **MutPy**.

The following metrics were recorded:
- Total mutants generated  
- Mutants killed  
- Mutants survived  

Additional test cases were added to kill surviving mutants.

---

## 🚀 How to Run

### Run Tests
```bash
pytest
