import argparse
from turtlpass.turtlpass_rp2040 import TurtlPassRP2040
from turtlpass.password import generate_password

def get_colors():
    return {
        "Green": "qoKaq3prxHRcfGxWbmj1qu8P5pDjWUKiXOCC5RZHjL4Nri6OQG9BKMdg3Ozs9CtJgiU39C6rgsOCWDnRHWXMZ8z19CvnTYaeYXM6",
        "Yellow": "shg9AMbLF85KEumVkitTG2r7ABZ7CQ9Cui29CwjJ6i9C1tzje3K7G58kkPSZ5wU9CjRlzs1lORTvDFLmk8qEiGkERPM3TKM1YAWX",
        "Red": "G7soHfxNcuAjTTr1H8x9CWuO4nZbZzteb08zQuy2zkrE9Az8KtvISK8mge9CKmSbuNeXiv7mtQnFMjzddHg1iO76gnYV9BWumZ2P",
        "Blue": "0gdk2XD9BULY6avFRlqooqLL1xNQmhBfIq9BlQKJINs6XOMJZVMdFdUbnq9C5dDknQsmzWrW9CXWufCeza9BgjUYjpnXb4AREj8v",
        "White": "pHYXA1Jf9ADlf1sJYxlryU75AzmngoVpaGHqo7zn5VY0ZzLWNZnX6elkfSSjedAT1QlLZGzDJQrfRb1Jv6L4kDqgwC0WS7VR5x6e",
        "Violet": "9BLaA9CpKLUNOGeWYSszODa1Zm9Ba2aFinlJuIP3q09A6DdAEHMKzoBtXLS0wiT1b01yRd8R9C9CsKk9BkFxuhZCL3B0Lpwv9Ap7",
        "Orange": "eRMod9BXmLKESToZBhe0qosuppZnNT9A8VyeNTSshBQBbB8kMx86b9ADgpvWs8HPAfSYAtgLgt9A6cYX9CAWAEOnicAqluqfLA8G",
        "Aqua": "sw8fnFfxbz200lEFWt86drLnFg9CQKZlyFTzJHyLH9ADFZtK7nMEzthN4uZxi3Si3CSK9CCwOYaZDL4kdQqmtKAFub0KvWFxgg3L",
        "Pink": "ZYYRo9AB4xci9CAauKWK2JOWBK5R0RYWeN2q7QKG0In9B9AdahCPQv4KpmLulyfZhEpHASokaxxd4tFoTtNkjwcBVzMWGK2fcOVf"
    }

def test_password(turtlpass, color, secure_hash, expected_password):
    if not generate_password(turtlpass, secure_hash):
        return False

    password = input("Type password here: ")

    if password == expected_password:
        print("✅ Passwords match.")
    else:
        print("❌ Passwords do not match.")
        print(f"Expected password: {expected_password}")
    return True

def main(device_path: str) -> None:
    with TurtlPassRP2040(device_path=device_path) as turtlpass:
        colors = get_colors()

        for color, expected_password in colors.items():
            input(f"Testing password for the color: {color}\nPress enter to continue...")
            secure_hash = "0"
            if not test_password(turtlpass, color, secure_hash, expected_password):
                return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Password Generation")
    parser.add_argument("device_path", type=str, help="Path to the TurtlPass RP2040 device ($ ls /dev/cu.* | grep usbmodem)")
    args = parser.parse_args()
    main(args.device_path)

# python3 test_password_generation.py /dev/cu.usbmodem14101
