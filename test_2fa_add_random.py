import argparse
import random
import string
from turtlpass.argon2_hash_generator import generate_secure_hash
from turtlpass.turtlpass_rp2040 import TurtlPassRP2040
from turtlpass.otp_management import add_otp_shared_secret, get_encrypted_otp_secrets, generate_otp_code, delete_all_secrets_from_eeprom

def test_add_random_secret(turtlpass):
    pin = random.randint(100000, 999999)
    secure_hash = generate_secure_hash(pin, "domain", "account")
    otp_shared_secret = generate_random_string(32);
    if add_otp_shared_secret(turtlpass, secure_hash, otp_shared_secret):
        return True
    else:
        print("<ERROR>")
        return False

def generate_random_string(length):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def main(device_path: str) -> None:
    with TurtlPassRP2040(device_path=device_path) as turtlpass:

        print("Deleting all secrets from EEPROM...")
        if not delete_all_secrets_from_eeprom(turtlpass):
            return

        for index in range(105):
            if not test_add_random_secret(turtlpass):
                break
            print("Current:", index)

        get_encrypted_otp_secrets(turtlpass)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test 2FA Manager - Add random secrets")
    parser.add_argument("device_path", type=str, help="Path to the TurtlPass RP2040 device ($ ls /dev/cu.* | grep usbmodem)")
    args = parser.parse_args()
    main(args.device_path)

# python3 test_2fa_add_random.py /dev/cu.usbmodem14101
