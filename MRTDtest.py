"""
MRTDtest.py
Unit tests for MRTD.py functions.
Uses mock for hardware (scan_passport) and database (fetch_passport_record) stubs.
"""

import unittest
from unittest.mock import patch, MagicMock
from MRTD import (
    validate_passport_number,
    validate_nationality_code,
    validate_date_of_birth,
    calculate_check_digit,
    scan_passport,
    fetch_passport_record,
)


class TestValidatePassportNumber(unittest.TestCase):

    # --- Statement / basic valid cases ---

    def test_valid_passport_6_chars(self):
        # Minimum valid length (6 alphanumeric characters)
        self.assertTrue(validate_passport_number("AB1234"))

    def test_valid_passport_9_chars(self):
        # Maximum valid length (9 alphanumeric characters)
        self.assertTrue(validate_passport_number("A12345678"))

    def test_valid_passport_all_letters(self):
        # All-letter passport number within valid length
        self.assertTrue(validate_passport_number("ABCDEF"))

    def test_valid_passport_all_digits(self):
        # All-digit passport number within valid length
        self.assertTrue(validate_passport_number("123456"))

    def test_valid_passport_mixed(self):
        # Mixed letters and digits, 7 characters
        self.assertTrue(validate_passport_number("L898902"))

    # --- Branch: wrong type ---

    def test_invalid_not_string_int(self):
        # Non-string input (integer) should return False
        self.assertFalse(validate_passport_number(123456))

    def test_invalid_not_string_none(self):
        # None input should return False
        self.assertFalse(validate_passport_number(None))

    def test_invalid_not_string_list(self):
        # List input should return False
        self.assertFalse(validate_passport_number(["AB1234"]))

    # --- Branch: length violations ---

    def test_invalid_too_short(self):
        # Length 5 is below minimum of 6
        self.assertFalse(validate_passport_number("AB123"))

    def test_invalid_too_long(self):
        # Length 10 exceeds maximum of 9
        self.assertFalse(validate_passport_number("AB12345678"))

    def test_invalid_empty_string(self):
        # Empty string has length 0, below minimum
        self.assertFalse(validate_passport_number(""))

    # --- Branch: non-alphanumeric characters ---

    def test_invalid_special_char_dash(self):
        # Dash is not alphanumeric
        self.assertFalse(validate_passport_number("AB-234"))

    def test_invalid_special_char_space(self):
        # Space is not alphanumeric
        self.assertFalse(validate_passport_number("AB 234"))

    def test_invalid_special_char_angle(self):
        # Angle bracket (MRZ filler) is not valid in passport number field
        self.assertFalse(validate_passport_number("AB<<34"))

    # --- Condition: boundary lengths ---

    def test_boundary_length_6(self):
        # Exactly 6 characters — boundary condition for minimum
        self.assertTrue(validate_passport_number("ZE1842"))

    def test_boundary_length_9(self):
        # Exactly 9 characters — boundary condition for maximum
        self.assertTrue(validate_passport_number("ZE1842265"))


class TestValidateNationalityCode(unittest.TestCase):

    # --- Valid ICAO nationality codes from Section 5 ---

    def test_valid_usa(self):
        # USA is a valid ICAO nationality code
        self.assertTrue(validate_nationality_code("USA"))

    def test_valid_fra(self):
        # FRA (France) is a valid ICAO nationality code
        self.assertTrue(validate_nationality_code("FRA"))

    def test_valid_deu(self):
        # DEU (Germany) is a valid ICAO nationality code
        self.assertTrue(validate_nationality_code("DEU"))

    def test_valid_jpn(self):
        # JPN (Japan) is a valid ICAO nationality code
        self.assertTrue(validate_nationality_code("JPN"))

    def test_valid_ind(self):
        # IND (India) is a valid ICAO nationality code
        self.assertTrue(validate_nationality_code("IND"))

    def test_valid_bra(self):
        # BRA (Brazil) is a valid ICAO nationality code
        self.assertTrue(validate_nationality_code("BRA"))

    def test_valid_aus(self):
        # AUS (Australia) is a valid ICAO nationality code
        self.assertTrue(validate_nationality_code("AUS"))

    def test_valid_can(self):
        # CAN (Canada) is a valid ICAO nationality code
        self.assertTrue(validate_nationality_code("CAN"))

    def test_valid_chn(self):
        # CHN (China) is a valid ICAO nationality code
        self.assertTrue(validate_nationality_code("CHN"))

    def test_valid_uto(self):
        # UTO is used in ICAO example documents
        self.assertTrue(validate_nationality_code("UTO"))

    def test_valid_xxx(self):
        # XXX is the ICAO code for unspecified/stateless nationality
        self.assertTrue(validate_nationality_code("XXX"))

    def test_valid_xxa(self):
        # XXA is the ICAO code for stateless persons (Apatride)
        self.assertTrue(validate_nationality_code("XXA"))

    # --- Branch: wrong type ---

    def test_invalid_not_string_int(self):
        # Integer input should return False
        self.assertFalse(validate_nationality_code(840))

    def test_invalid_not_string_none(self):
        # None input should return False
        self.assertFalse(validate_nationality_code(None))

    # --- Branch: wrong length ---

    def test_invalid_too_short(self):
        # 2-letter code is invalid (must be exactly 3)
        self.assertFalse(validate_nationality_code("US"))

    def test_invalid_too_long(self):
        # 4-letter code is invalid
        self.assertFalse(validate_nationality_code("USAA"))

    def test_invalid_empty_string(self):
        # Empty string has wrong length
        self.assertFalse(validate_nationality_code(""))

    # --- Branch: not in valid set ---

    def test_invalid_code_not_in_set(self):
        # ZZZ is not in the ICAO valid nationality codes list
        self.assertFalse(validate_nationality_code("ZZZ"))

    def test_invalid_lowercase(self):
        # Lowercase version of a valid code should fail (case-sensitive)
        self.assertFalse(validate_nationality_code("usa"))

    def test_invalid_numeric_string(self):
        # Numeric string of length 3 is not a valid nationality code
        self.assertFalse(validate_nationality_code("123"))


class TestValidateDateOfBirth(unittest.TestCase):

    # --- Valid dates ---

    def test_valid_dob_standard(self):
        # Standard valid date: August 12, 1974 (from ICAO example)
        self.assertTrue(validate_date_of_birth("740812"))

    def test_valid_dob_jan_first(self):
        # January 1st — minimum valid month and day
        self.assertTrue(validate_date_of_birth("900101"))

    def test_valid_dob_dec_31(self):
        # December 31st — maximum valid month and day
        self.assertTrue(validate_date_of_birth("991231"))

    def test_valid_dob_feb(self):
        # February date — month 02 is valid
        self.assertTrue(validate_date_of_birth("850228"))

    # --- Branch: wrong type ---

    def test_invalid_not_string_int(self):
        # Integer input should return False
        self.assertFalse(validate_date_of_birth(740812))

    def test_invalid_not_string_none(self):
        # None input should return False
        self.assertFalse(validate_date_of_birth(None))

    # --- Branch: wrong length ---

    def test_invalid_too_short(self):
        # 5-digit string is too short
        self.assertFalse(validate_date_of_birth("74081"))

    def test_invalid_too_long(self):
        # 7-digit string is too long
        self.assertFalse(validate_date_of_birth("7408121"))

    def test_invalid_empty_string(self):
        # Empty string fails length check
        self.assertFalse(validate_date_of_birth(""))

    # --- Branch: non-digit characters ---

    def test_invalid_contains_letters(self):
        # Letters in the date string should return False
        self.assertFalse(validate_date_of_birth("74AB12"))

    def test_invalid_contains_space(self):
        # Space character should return False
        self.assertFalse(validate_date_of_birth("74 812"))

    # --- Branch / Condition: month boundaries ---

    def test_invalid_month_zero(self):
        # Month 00 is out of range (must be 01-12)
        self.assertFalse(validate_date_of_birth("740012"))

    def test_invalid_month_13(self):
        # Month 13 is out of range
        self.assertFalse(validate_date_of_birth("741312"))

    def test_valid_month_boundary_01(self):
        # Month 01 (January) is valid lower boundary
        self.assertTrue(validate_date_of_birth("740101"))

    def test_valid_month_boundary_12(self):
        # Month 12 (December) is valid upper boundary
        self.assertTrue(validate_date_of_birth("741201"))

    # --- Branch / Condition: day boundaries ---

    def test_invalid_day_zero(self):
        # Day 00 is out of range (must be 01-31)
        self.assertFalse(validate_date_of_birth("740800"))

    def test_invalid_day_32(self):
        # Day 32 is out of range
        self.assertFalse(validate_date_of_birth("740832"))

    def test_valid_day_boundary_01(self):
        # Day 01 is valid lower boundary
        self.assertTrue(validate_date_of_birth("740801"))

    def test_valid_day_boundary_31(self):
        # Day 31 is valid upper boundary
        self.assertTrue(validate_date_of_birth("740831"))


class TestCalculateCheckDigit(unittest.TestCase):

    # --- Known ICAO example values ---

    def test_check_digit_icao_example_passport_number(self):
        # From ICAO doc example: passport number "L898902C3" -> check digit 6
        self.assertEqual(calculate_check_digit("L898902C3"), 6)

    def test_check_digit_icao_example_dob(self):
        # From ICAO doc example: date of birth "740812" -> check digit 2
        self.assertEqual(calculate_check_digit("740812"), 2)

    def test_check_digit_icao_example_expiry(self):
        # From ICAO doc example: expiry "120415" -> check digit 9
        self.assertEqual(calculate_check_digit("120415"), 9)

    def test_check_digit_all_zeros(self):
        # All zeros should produce check digit 0
        self.assertEqual(calculate_check_digit("000000"), 0)

    def test_check_digit_single_digit_zero(self):
        # Single '0' with weight 7 -> 0*7=0, mod 10 = 0
        self.assertEqual(calculate_check_digit("0"), 0)

    def test_check_digit_single_digit_one(self):
        # Single '1' with weight 7 -> 1*7=7, mod 10 = 7
        self.assertEqual(calculate_check_digit("1"), 7)

    def test_check_digit_letter_a(self):
        # 'A' = 10, weight 7 -> 10*7=70, mod 10 = 0
        self.assertEqual(calculate_check_digit("A"), 0)

    def test_check_digit_filler_characters(self):
        # '<' = 0, so all fillers should produce 0
        self.assertEqual(calculate_check_digit("<<<<<<"), 0)

    def test_check_digit_mixed_filler_and_digits(self):
        # Mixed: "ZE184226B<<<<<" personal number from ICAO example -> check digit 1
        self.assertEqual(calculate_check_digit("ZE184226B<<<<<"), 1)

    def test_check_digit_weight_rotation(self):
        # Verifies weights cycle: positions 0,1,2 use 7,3,1 then repeat
        # "111": 1*7 + 1*3 + 1*1 = 11, mod 10 = 1
        self.assertEqual(calculate_check_digit("111"), 1)

    def test_check_digit_weight_rotation_4_chars(self):
        # "1111": 1*7+1*3+1*1+1*7=18, mod 10 = 8
        self.assertEqual(calculate_check_digit("1111"), 8)

    # --- Branch: invalid input ---

    def test_check_digit_empty_string(self):
        # Empty string should return 0 per implementation
        self.assertEqual(calculate_check_digit(""), 0)

    def test_check_digit_not_string_int(self):
        # Non-string input (integer) should return 0
        self.assertEqual(calculate_check_digit(123456), 0)

    def test_check_digit_not_string_none(self):
        # None input should return 0
        self.assertEqual(calculate_check_digit(None), 0)

    def test_check_digit_unknown_special_char(self):
        # Unrecognized special character (e.g. '@') should be treated as 0
        # '@' -> value 0, weight 7 -> 0; mod 10 = 0
        self.assertEqual(calculate_check_digit("@"), 0)

    def test_check_digit_uppercase_letters(self):
        # 'Z' = 35, weight 7 -> 35*7=245, mod 10 = 5
        self.assertEqual(calculate_check_digit("Z"), 5)

    def test_check_digit_lowercase_treated_as_upper(self):
        # Lowercase 'a' should be treated same as 'A' = 10*7=70, mod 10 = 0
        self.assertEqual(calculate_check_digit("a"), 0)

    def test_check_digit_usa_country_code(self):
        # "USA": U=30*7=210, S=28*3=84, A=10*1=10 -> 304, mod 10 = 4
        self.assertEqual(calculate_check_digit("USA"), 4)

    def test_check_digit_deu_country_code(self):
        # "DEU": D=13*7=91, E=14*3=42, U=30*1=30 -> 163, mod 10 = 3
        self.assertEqual(calculate_check_digit("DEU"), 3)

    def test_check_digit_jpn_country_code(self):
        # "JPN": J=19*7=133, P=25*3=75, N=23*1=23 -> 231, mod 10 = 1
        self.assertEqual(calculate_check_digit("JPN"), 1)


class TestScanPassport(unittest.TestCase):

    def test_scan_passport_returns_none_by_default(self):
        # scan_passport is a hardware stub; should return None when not mocked
        result = scan_passport()
        self.assertIsNone(result)

    @patch("MRTD.scan_passport")
    def test_scan_passport_mock_returns_mrz_lines(self, mock_scan):
        # Mock the hardware scanner to return two valid MRZ lines (ICAO example)
        mock_scan.return_value = (
            "PPUTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<",
            "L898902C36UTO7408122F1204159ZE184226B<<<<<10"
        )
        result = mock_scan()
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        self.assertIn("ERIKSSON", result[0])

    @patch("MRTD.scan_passport")
    def test_scan_passport_mock_returns_usa_passport(self, mock_scan):
        # Mock scanner returning a USA passport MRZ
        mock_scan.return_value = (
            "PPUSASMITH<<JOHN<PAUL<<<<<<<<<<<<<<<<<<<<<<<<",
            "A12345674USA8001011M2501015<<<<<<<<<<<<<<<6"
        )
        result = mock_scan()
        self.assertIn("USA", result[1])

    @patch("MRTD.scan_passport")
    def test_scan_passport_mock_scan_failure(self, mock_scan):
        # Simulate hardware scan failure returning None
        mock_scan.return_value = None
        result = mock_scan()
        self.assertIsNone(result)

    @patch("MRTD.scan_passport")
    def test_scan_passport_mock_called_once(self, mock_scan):
        # Verify the scan function is called exactly once
        mock_scan.return_value = ("line1", "line2")
        mock_scan()
        mock_scan.assert_called_once()


class TestFetchPassportRecord(unittest.TestCase):

    def test_fetch_passport_record_returns_none_by_default(self):
        # fetch_passport_record is a DB stub; should return None when not mocked
        result = fetch_passport_record("AB1234")
        self.assertIsNone(result)

    @patch("MRTD.fetch_passport_record")
    def test_fetch_passport_record_mock_valid_usa(self, mock_fetch):
        # Mock DB returning a record for a USA passport holder
        mock_fetch.return_value = {
            "passport_number": "A1234567",
            "nationality": "USA",
            "dob": "800101",
            "expiry": "300101",
            "surname": "SMITH",
            "given_names": "JOHN"
        }
        record = mock_fetch("A1234567")
        self.assertEqual(record["nationality"], "USA")
        self.assertEqual(record["dob"], "800101")

    @patch("MRTD.fetch_passport_record")
    def test_fetch_passport_record_mock_valid_fra(self, mock_fetch):
        # Mock DB returning a record for a FRA (France) passport holder
        mock_fetch.return_value = {
            "passport_number": "FR12345",
            "nationality": "FRA",
            "dob": "750615",
            "expiry": "290615",
        }
        record = mock_fetch("FR12345")
        self.assertEqual(record["nationality"], "FRA")

    @patch("MRTD.fetch_passport_record")
    def test_fetch_passport_record_mock_not_found(self, mock_fetch):
        # Simulate DB returning None when passport number is not found
        mock_fetch.return_value = None
        result = mock_fetch("NOTEXIST")
        self.assertIsNone(result)

    @patch("MRTD.fetch_passport_record")
    def test_fetch_passport_record_mock_called_with_correct_arg(self, mock_fetch):
        # Verify the DB function is called with the correct passport number
        mock_fetch.return_value = {}
        mock_fetch("ZE184226")
        mock_fetch.assert_called_once_with("ZE184226")

    @patch("MRTD.fetch_passport_record")
    def test_fetch_passport_record_mock_deu_passport(self, mock_fetch):
        # Mock DB returning a record for a DEU (Germany) passport holder
        mock_fetch.return_value = {
            "passport_number": "C1K2L3M4",
            "nationality": "DEU",
            "dob": "920310",
            "expiry": "270310",
        }
        record = mock_fetch("C1K2L3M4")
        self.assertEqual(record["nationality"], "DEU")
        self.assertTrue(validate_nationality_code(record["nationality"]))

    @patch("MRTD.fetch_passport_record")
    def test_fetch_passport_record_mock_jpn_dob_validated(self, mock_fetch):
        # Mock DB for JPN passport and validate the returned DOB with validate_date_of_birth
        mock_fetch.return_value = {
            "passport_number": "TK987654",
            "nationality": "JPN",
            "dob": "881115",
        }
        record = mock_fetch("TK987654")
        self.assertTrue(validate_date_of_birth(record["dob"]))

# ===== ADDITIONAL TEST CASES TO KILL SURVIVING MUTANTS =====

class TestAdditionalMutantKillers(unittest.TestCase):

    # --- Missing nationality code coverage (mutants #34-51, #54-57) ---

    def test_valid_gbd(self):
        # Kills #34, #35: 'GBD' replaced — British Dependent Territories citizen
        self.assertTrue(validate_nationality_code("GBD"))

    def test_valid_gbn(self):
        # Kills #36, #37: 'GBN' replaced — British National (Overseas)
        self.assertTrue(validate_nationality_code("GBN"))

    def test_valid_gbo(self):
        # Kills #38, #39: 'GBO' replaced — British Overseas citizen
        self.assertTrue(validate_nationality_code("GBO"))

    def test_valid_gbs(self):
        # Kills #40, #41: 'GBS' replaced — British Subject
        self.assertTrue(validate_nationality_code("GBS"))

    def test_valid_rks(self):
        # Kills #42, #43: 'RKS' replaced — Kosovo
        self.assertTrue(validate_nationality_code("RKS"))

    def test_valid_eue(self):
        # Kills #44, #45: 'EUE' replaced — European Union emergency travel document
        self.assertTrue(validate_nationality_code("EUE"))

    def test_valid_uno(self):
        # Kills #46, #47: 'UNO' replaced — United Nations Organization laissez-passer
        self.assertTrue(validate_nationality_code("UNO"))

    def test_valid_una(self):
        # Kills #48, #49: 'UNA' replaced — United Nations agency
        self.assertTrue(validate_nationality_code("UNA"))

    def test_valid_xba(self):
        # Kills #50, #51: 'XBA' replaced — stateless document code
        self.assertTrue(validate_nationality_code("XBA"))

    def test_valid_xxb(self):
        # Kills #54, #55: 'XXB' replaced — stateless persons (1954 Convention)
        self.assertTrue(validate_nationality_code("XXB"))

    def test_valid_xxc(self):
        # Kills #56, #57: 'XXC' replaced — travel docs under other instruments
        self.assertTrue(validate_nationality_code("XXC"))

    # --- Alpha character value in check digit (mutant #1) ---

    def test_check_digit_alpha_value(self):
        # Kills #1: ord(char.upper()) - 55 mutated to + 55
        # A = ord('A') - 55 = 65 - 55 = 10; with +55 it would be 120
        # "A" alone: value=10, weight=7, total=70, 70%10=0
        self.assertEqual(calculate_check_digit("A"), 0)
        # "B" = 11 * 7 = 77, 77%10 = 7
        self.assertEqual(calculate_check_digit("B"), 7)
        # "Z" = 35 * 7 = 245, 245%10 = 5
        self.assertEqual(calculate_check_digit("Z"), 5)

    # --- Date-of-birth day slice (mutants #83, #123) ---

    def test_dob_day_slice_boundary(self):
        # Kills #83 (dob[4:6] -> dob[4:7]) and #123 (dob[4:6] -> dob[4:])
        # Day=32 is invalid; a broken slice returns wrong day value and passes
        self.assertFalse(validate_date_of_birth("990132"))

    # --- Filler character '<' in check digit (mutants #94, #95, #119) ---

    def test_check_digit_filler_char_is_specifically_angle_bracket(self):
        # Kills #94 (char=='<' -> char=='mutpy'), #95 (char=='<' -> char==''),
        # and #119 (char=='<' -> char!='<')
        # '<' must specifically map to value=0 via its own branch
        self.assertEqual(calculate_check_digit("<"), 0)
        # Known ICAO example: "L898902C3" -> check digit 6
        self.assertEqual(calculate_check_digit("L898902C3"), 6)
        # MRZ with fillers: "<<<" should give 0
        self.assertEqual(calculate_check_digit("<<<"), 0)


if __name__ == "__main__":
    unittest.main()
