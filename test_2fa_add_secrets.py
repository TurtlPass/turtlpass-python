import argparse
import time
import random
import string
from turtlpass.argon2_hash_generator import generate_secure_hash
from turtlpass.turtlpass_rp2040 import TurtlPassRP2040
from turtlpass.otp_management import add_otp_shared_secret, get_encrypted_otp_secrets, generate_otp_code, delete_all_secrets_from_eeprom

def test_add_otp_shared_secret(turtlpass, domain_name: str, account_id: str, pin: int, otp_shared_secret: str):
    secure_hash = generate_secure_hash(pin, domain_name, account_id)
    if add_otp_shared_secret(turtlpass, secure_hash, otp_shared_secret):
        return True
    else:
        print("<ERROR>")
        return False

def main(device_path: str) -> None:
    with TurtlPassRP2040(device_path=device_path) as turtlpass:
        test_cases = [
            {"domain_name": "amazon", "account_id": "amazon@mail.com", "pin": 704713, "otp_shared_secret": "PDLTYQWSNZAUPCMY"},
            {"domain_name": "google", "account_id": "google@mail.com", "pin": 631571, "otp_shared_secret": "TKTDRDZJEUSPXABC"},
            {"domain_name": "facebook", "account_id": "facebook@mail.com", "pin": 363873, "otp_shared_secret": "UQLERGZKEOTWYMHF"},
            {"domain_name": "twitter", "account_id": "twitter@mail.com", "pin": 180366, "otp_shared_secret": "NMFDKRDBUVHXNCDYYEFXPSAMKABPTFEX"},
            {"domain_name": "linkedin", "account_id": "linkedin@mail.com", "pin": 442071, "otp_shared_secret": "NQKUOBAIWNZGJSDKFAVYXOBRUCYAYILY"},
            {"domain_name": "apple", "account_id": "apple@mail.com", "pin": 246810, "otp_shared_secret": "IYSGBTFWHPLUTDTFFHAGNOLXRQNPDUFL"},
            {"domain_name": "instagram", "account_id": "instagram@mail.com", "pin": 331667, "otp_shared_secret": "WMHAEJUDXBRSBYSBKAYSUNNHEPFGJRXYSKSYDIYYIZTGSBHHWTVHVUHZTRJJHXTE"},
            {"domain_name": "netflix", "account_id": "netflix@mail.com", "pin": 950688, "otp_shared_secret": "FHTULQWCHLNHASHWSJSJFSYYYHJZBFAMUEIZRXGLOYGOYJUVATSXHFEELSMSDFZO"},
            {"domain_name": "spotify", "account_id": "spotify@mail.com", "pin": 217226, "otp_shared_secret": "JQCHBJCZJNVEUBWWAAYTWXTETUGWGPROYXIENLVMVCPAGALKSVVLIBMIBSEACSOG" }
        ]

        print("Deleting all secrets from EEPROM...")
        if not delete_all_secrets_from_eeprom(turtlpass):
            return

        for test_case in test_cases:
            if not test_add_otp_shared_secret(turtlpass, test_case["domain_name"], test_case["account_id"], test_case["pin"], test_case["otp_shared_secret"]):
                break

        get_encrypted_otp_secrets(turtlpass)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test 2FA Manager - Add shared secrets")
    parser.add_argument("device_path", type=str, help="Path to the TurtlPass RP2040 device ($ ls /dev/cu.* | grep usbmodem)")
    args = parser.parse_args()
    main(args.device_path)

# python3 test_2fa_add_secrets.py /dev/cu.usbmodem14101
