import argparse
import time
from turtlpass.turtlpass_rp2040 import TurtlPassRP2040
from turtlpass.encryption_image import process_image_encryption

def test_image_file_encryption(turtlpass, file_name: str) -> None:
    secure_hash = "0"
    src_file = "files/" + file_name
    dst_file = "out/encrypted_" + file_name
    process_image_encryption(turtlpass, "encrypt", secure_hash, src_file, dst_file)
    print("-" * 50)
    time.sleep(3)

def test_image_file_decryption(turtlpass, file_name: str) -> None:
    secure_hash = "0"
    src_file = "out/encrypted_" + file_name
    dst_file = "out/decrypted_" + file_name
    process_image_encryption(turtlpass, "decrypt", secure_hash, src_file, dst_file)
    print("-" * 50)
    time.sleep(3)

def main(device_path: str) -> None:
    with TurtlPassRP2040(device_path=device_path) as turtlpass:
        test_cases = [
            {"file_name": "turtle_x256.bmp"},
            {"file_name": "turtle_x512.bmp"},
            {"file_name": "turtle_x1024.bmp"},
            {"file_name": "turtle_x1920.bmp"}
        ]
        for test_case in test_cases:
            test_image_file_encryption(turtlpass, test_case["file_name"])
            test_image_file_decryption(turtlpass, test_case["file_name"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test File Encryption")
    parser.add_argument("device_path", type=str, help="Path to the TurtlPass RP2040 device ($ ls /dev/cu.* | grep usbmodem)")
    args = parser.parse_args()
    main(args.device_path)

# python3 test_image_file_encryption.py /dev/cu.usbmodem14101
