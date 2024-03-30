import argparse
import time
from turtlpass.turtlpass_rp2040 import TurtlPassRP2040
from turtlpass.encryption import process_encryption

def test_file_encryption(turtlpass, file_name: str) -> None:
    secure_hash = "0"
    src_file = "files/" + file_name
    dst_file = "out/" + file_name + ".enc"
    process_encryption(turtlpass, "encrypt", secure_hash, src_file, dst_file)
    print("-" * 50)
    time.sleep(1)

def test_file_decryption(turtlpass, file_name: str) -> None:
    secure_hash = "0"
    src_file = "out/" + file_name + ".enc"
    dst_file = "out/" + file_name
    process_encryption(turtlpass, "decrypt", secure_hash, src_file, dst_file)
    print("-" * 50)
    time.sleep(1)

def main(device_path: str) -> None:
    with TurtlPassRP2040(device_path=device_path) as turtlpass:
        test_cases = [
            {"file_name": "customers-100.csv"},
            {"file_name": "customers-1000.csv"},
            {"file_name": "customers-10000.csv"},
            {"file_name": "customers-100000.csv"}
        ]
        for test_case in test_cases:
            test_file_encryption(turtlpass, test_case["file_name"])

        for test_case in test_cases:
            test_file_decryption(turtlpass, test_case["file_name"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test File Encryption")
    parser.add_argument("device_path", type=str, help="Path to the TurtlPass RP2040 device ($ ls /dev/cu.* | grep usbmodem)")
    args = parser.parse_args()
    main(args.device_path)

# python3 test_file_encryption.py /dev/cu.usbmodem14101
