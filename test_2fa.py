import argparse
import time
from turtlpass.turtlpass_rp2040 import TurtlPassRP2040
from turtlpass.otp_management import add_otp_shared_secret, get_encrypted_otp_secrets, generate_otp_code, delete_all_secrets_from_eeprom

def test_add_otp_shared_secret(turtlpass, secure_hash: str, otp_shared_secret: str) -> None:
    if add_otp_shared_secret(turtlpass, secure_hash, otp_shared_secret):
        time.sleep(.5)
        get_encrypted_otp_secrets(turtlpass)

    time.sleep(1)

def test_otp_code(turtlpass, secure_hash, expected_otp, timestamp):
    if not generate_otp_code(turtlpass, secure_hash, timestamp):
        return False

    otp_code = input("Type OTP code here: ")

    if otp_code == expected_otp:
        print("✅ OTP codes match.")
    else:
        print("❌ OTP codes do not match.")
        print(f"Expected OTP code: {expected_otp}")
    return True

def main(device_path: str) -> None:
    with TurtlPassRP2040(device_path=device_path) as turtlpass:
        test_cases = [
            {
                "secure_hash": "cfb82615cbd35b67ff2efd2bd4b70aff071d02feaa21549a587c268b3f11ef2d0bbf0673f70f4cd84072051d2bb3c64e2b5eba1a2733983534a95651ae436c5b", 
                "otp_shared_secret": "PDLTYQWSNZAUPCMY", 
                "timestamp": 1676821524, 
                "expected_otp": "007359"
            }
        ]
        print("Deleting all secrets from EEPROM...")
        if not delete_all_secrets_from_eeprom(turtlpass):
            return

        for test_case in test_cases:
            test_add_otp_shared_secret(turtlpass, test_case["secure_hash"], test_case["otp_shared_secret"])
            test_otp_code(turtlpass, test_case["secure_hash"], test_case["expected_otp"], test_case["timestamp"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test 2FA Manager - Add shared secret & Get OTP Code")
    parser.add_argument("device_path", type=str, help="Path to the TurtlPass RP2040 device ($ ls /dev/cu.* | grep usbmodem)")
    args = parser.parse_args()
    main(args.device_path)

# python3 test_2fa.py /dev/cu.usbmodem14101
