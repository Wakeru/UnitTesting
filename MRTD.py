"""
MRTD (Machine Readable Travel Document) utility functions. These functions perform validation and basic processing based on simplified ICAO standards.
"""

VALID_NATIONALITY_CODES = {
    "USA", "CAN", "GBD", "GBN", "GBO", "GBS",
    "RKS", "EUE", "UNO", "UNA", "XBA", "XXA",
    "XXB", "XXC", "XXX", "UTO",
    "FRA", "DEU", "JPN", "IND", "BRA", "CHN", "AUS"
}


def validate_passport_number(passport_number: str) -> bool:
    """
    Validate passport number.
    Rules:
    - Must be a string
    - Must be 6 to 9 characters
    - Only letters and digits allowed
    """
    if not isinstance(passport_number, str):
        return False
    if len(passport_number) < 6 or len(passport_number) > 9:
        return False
    if not passport_number.isalnum():
        return False
    return True


def validate_nationality_code(code: str) -> bool:
    """
    Validate nationality code.
    Must be a 3-letter string from predefined ICAO-based list.
    """
    if not isinstance(code, str):
        return False
    if len(code) != 3:
        return False
    if code not in VALID_NATIONALITY_CODES:
        return False
    return True


def validate_date_of_birth(dob: str) -> bool:
    """
    Validate date of birth in YYMMDD format.
    Rules:
    - Must be a string
    - Must be 6 digits
    - Month between 01-12
    - Day between 01-31
    Note: Year is not validated (any 2-digit year is acceptable).
    """
    if not isinstance(dob, str):
        return False
    if len(dob) != 6 or not dob.isdigit():
        return False

    month = int(dob[2:4])
    day = int(dob[4:6])

    if month < 1 or month > 12:
        return False
    if day < 1 or day > 31:
        return False

    return True


def calculate_check_digit(data: str) -> int:
    """
    Calculate check digit using ICAO method.
    Weights: 7, 3, 1 repeating.
    Letters: A=10 to Z=35
    '<' = 0
    """
    if not isinstance(data, str) or not data:
        return 0

    weights = [7, 3, 1]
    total = 0

    for i, char in enumerate(data):
        if char.isdigit():
            value = int(char)
        elif char.isalpha():
            value = ord(char.upper()) - 55  # A=10
        elif char == '<':
            value = 0
        else:
            value = 0

        total += value * weights[i % 3]

    return total % 10

def encode_record(record: dict) -> str:
    """
    Convert one decoded MRTD record into two MRZ-like lines separated by a semicolon.
    """

    line1_data = record["line1"]
    line2_data = record["line2"]

    issuing_country = line1_data["issuing_country"]
    last_name = line1_data["last_name"].replace(" ", "<").upper()
    given_name = line1_data["given_name"].replace(" ", "<").upper()

    passport_number = line2_data["passport_number"]
    country_code = line2_data["country_code"]
    birth_date = line2_data["birth_date"]
    sex = line2_data["sex"]
    expiration_date = line2_data["expiration_date"]
    personal_number = line2_data["personal_number"]

    mrz_line1 = f"P<{issuing_country}{last_name}<<{given_name}"
    mrz_line2 = (
        f"{passport_number}{country_code}"
        f"{birth_date}{sex}{expiration_date}{personal_number}"
    )

    return mrz_line1 + ";" + mrz_line2


# Stub for hardware interaction
def scan_passport():
    """Simulated hardware scan function (not implemented)."""
    pass


# Stub for database interaction
def fetch_passport_record(passport_number: str):
    """Simulated database lookup (not implemented)."""
    pass
