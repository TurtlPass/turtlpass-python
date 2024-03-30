import time
import os
from enum import Enum
from turtlpass.list_devices import list_usb_devices
from turtlpass.turtlpass_rp2040 import TurtlPassRP2040
from turtlpass.argon2_hash_generator import generate_secure_hash
from turtlpass.password import generate_password
from turtlpass.otp_management import add_otp_shared_secret, get_encrypted_otp_secrets, generate_otp_code
from turtlpass.encryption import process_encryption
from turtlpass.encryption_image import process_image_encryption

class MenuOption(Enum):
    EXIT = 0
    DEVICE_INFO = 1
    GENERATE_PASSWORD = 2
    GENERATE_OTP_CODE = 3
    ADD_OTP_SECRET = 4
    GET_ENCRYPTED_OTP = 5
    ENCRYPT_FILE = 6
    DECRYPT_FILE = 7
    ENCRYPT_IMAGE = 8
    DECRYPT_IMAGE = 9

def draw_turtle():
    print("                               ___-------___")
    print("                           _-~~             ~~-_")
    print("                        _-~                    /~-_")
    print("     /^\__/^\         /~  \\                   /    \\")
    print("   /|  O|| O|        /      \\_______________/        \\")
    print("  | |___||__|      /       /                \\          \\")
    print("  |          \\    /      /                    \\          \\")
    print("  |   (_______) /______/                        \\_________ \\")
    print("  |         / /         \\                      /            \\")
    print("   \\         \\^\\\\         \\                  /               \\     /")
    print("     \\         ||           \\______________/      _-_       //\\__//")
    print("       \\       ||------_-~~-_ ------------- \\ --/~   ~\\    || __/")
    print("         ~-----||====/~     |==================|       |/~~~~~")
    print("          (_(__/  ./     /                    \\_\\      \\.")
    print("                 (_(___/                         \\_____)_)   [art by jurcy]")
    print("")

def draw_ascii_art():
    print("████████╗██╗░░░██╗██████╗░████████╗██╗░░░░░██████╗░░█████╗░░██████╗░██████╗")
    print("╚══██╔══╝██║░░░██║██╔══██╗╚══██╔══╝██║░░░░░██╔══██╗██╔══██╗██╔════╝██╔════╝")
    print("░░░██║░░░██║░░░██║██████╔╝░░░██║░░░██║░░░░░██████╔╝███████║╚█████╗░╚█████╗░")
    print("░░░██║░░░██║░░░██║██╔══██╗░░░██║░░░██║░░░░░██╔═══╝░██╔══██║░╚═══██╗░╚═══██╗")
    print("░░░██║░░░╚██████╔╝██║░░██║░░░██║░░░███████╗██║░░░░░██║░░██║██████╔╝██████╔╝")
    print("░░░╚═╝░░░░╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═╝░░░░░╚═╝░░╚═╝╚═════╝░╚═════╝░")

def draw_line():
    print("███████████████████████████████████████████████████████████████████████████")

def draw_soft_line():
    print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")

def display_menu():
    print("Options:")
    print("0. Exit")
    print("1. Get Device Information")
    print("2. Generate Password")
    print("3. Generate OTP Code")
    print("4. Add OTP Shared Secret")
    print("5. Get Encrypted OTP Secrets")
    print("6. Encrypt File")
    print("7. Decrypt File")
    print("8. Encrypt Image (experimental)")
    print("9. Decrypt Image (experimental)")

def select_device(devices):
    if len(devices) == 1:
        device = devices[0]
        print(f"Device detected: {device}")
        return device
    else:
        print("Multiple USB devices detected:")
        for i, device in enumerate(devices, start=1):
            print(f"{i}. {device}")
        while True:
            choice = input("Select the device number: ")
            try:
                choice = int(choice)
                if 1 <= choice <= len(devices):
                    return devices[choice - 1]
                else:
                    print("Invalid choice. Please enter a number between 1 and", len(devices))
            except ValueError:
                print("Invalid input. Please enter a number.")

def get_device_information(turtlpass: TurtlPassRP2040) -> None:
    draw_line()
    print("1. Get Device Information")
    draw_soft_line()
    turtlpass.send_command_read_until_end("i")
    draw_line()

def generate_password_option(turtlpass: TurtlPassRP2040) -> None:
    draw_line()
    print("2. Generate Password")
    draw_soft_line()
    secure_hash = get_input_and_hash()
    generate_password(turtlpass, secure_hash)
    del secure_hash
    draw_line()

def generate_otp_code_option(turtlpass: TurtlPassRP2040) -> None:
    draw_line()
    print("3. Generate OTP Code")
    draw_soft_line()
    secure_hash = get_input_and_hash()
    generate_otp_code(turtlpass, secure_hash)
    del secure_hash
    draw_line()

def add_otp_shared_secret_option(turtlpass: TurtlPassRP2040) -> None:
    draw_line()
    print("4. Add OTP Shared Secret")
    draw_soft_line()
    otp_shared_secret = input("Enter OTP Shared Secret: ")
    draw_soft_line()
    secure_hash = get_input_and_hash()
    add_otp_shared_secret(turtlpass, secure_hash, otp_shared_secret)
    del secure_hash, otp_shared_secret
    draw_line()

def get_encrypted_otp_secrets_option(turtlpass: TurtlPassRP2040) -> None:
    draw_line()
    print("5. Get Encrypted OTP Secrets")
    draw_soft_line()
    get_encrypted_otp_secrets(turtlpass)
    draw_line()

def encrypt_file_option(turtlpass: TurtlPassRP2040) -> None:
    draw_line()
    print("6. Encrypt File")
    draw_soft_line()
    src_file = input("Enter input file name (e.g. 'files/customers-100.csv'): ")
    if not os.path.isfile(src_file):
        print("Input file not found.")
        draw_line()
        return
    dst_file = input("Enter output file name (e.g. 'customers-100.csv.enc'): ")
    draw_soft_line()
    secure_hash = get_input_and_hash()
    process_encryption(turtlpass, "encrypt", secure_hash, src_file, dst_file)
    del secure_hash, src_file, dst_file
    draw_line()

def decrypt_file_option(turtlpass: TurtlPassRP2040) -> None:
    draw_line()
    print("7. Decrypt File")
    draw_soft_line()
    src_file = input("Enter input file name (e.g. 'customers-100.csv.enc'): ")
    if not os.path.isfile(src_file):
        print("Input file not found.")
        draw_line()
        return
    dst_file = input("Enter output file name (e.g. 'customers-100.csv'): ")
    draw_soft_line()
    secure_hash = get_input_and_hash()
    process_encryption(turtlpass, "decrypt", secure_hash, src_file, dst_file)
    del secure_hash, src_file, dst_file
    draw_line()

# Image (experimental)
def encrypt_image_option(turtlpass: TurtlPassRP2040) -> None:
    draw_line()
    print("8. Encrypt Image (experimental)")
    draw_soft_line()
    src_file = input("Enter input file name (e.g. 'files/turtle_x256.bmp'): ")
    if not os.path.isfile(src_file):
        print("Input image file not found.")
        draw_line()
        return
    dst_file = input("Enter output file name (e.g. 'encrypted_turtle.bmp'): ")
    draw_soft_line()
    secure_hash = get_input_and_hash()
    process_image_encryption(turtlpass, "encrypt", secure_hash, src_file, dst_file)
    del secure_hash, src_file, dst_file
    draw_line()

# Image (experimental)
def decrypt_image_option(turtlpass: TurtlPassRP2040) -> None:
    draw_line()
    print("9. Decrypt Image (experimental)")
    draw_soft_line()
    src_file = input("Enter input file name (e.g. 'encrypted_turtle.bmp'): ")
    if not os.path.isfile(src_file):
        print("Input image file not found.")
        draw_line()
        return
    dst_file = input("Enter output file name (e.g. 'turtle_x256.bmp'): ")
    draw_soft_line()
    secure_hash = get_input_and_hash()
    process_image_encryption(turtlpass, "decrypt", secure_hash, src_file, dst_file)
    del secure_hash, src_file, dst_file
    draw_line()

def get_input_and_hash() -> str:
    domain_name = input("Enter Domain Name (e.g. 'google'): ")
    account_id = input("Enter Account ID (e.g. 'user@example.com'): ")
    pin = input("Enter PIN (e.g. '704713'): ")
    secure_hash = generate_secure_hash(pin, domain_name, account_id)
    del domain_name, account_id, pin
    return secure_hash

def handle_option(option: MenuOption, turtlpass: TurtlPassRP2040) -> None:
    if option == MenuOption.DEVICE_INFO:
        get_device_information(turtlpass)
    elif option == MenuOption.GENERATE_PASSWORD:
        generate_password_option(turtlpass)
    elif option == MenuOption.GENERATE_OTP_CODE:
        generate_otp_code_option(turtlpass)
    elif option == MenuOption.ADD_OTP_SECRET:
        add_otp_shared_secret_option(turtlpass)
    elif option == MenuOption.GET_ENCRYPTED_OTP:
        get_encrypted_otp_secrets_option(turtlpass)
    elif option == MenuOption.ENCRYPT_FILE:
        encrypt_file_option(turtlpass)
    elif option == MenuOption.DECRYPT_FILE:
        decrypt_file_option(turtlpass)
    elif option == MenuOption.ENCRYPT_IMAGE:
        encrypt_image_option(turtlpass)
    elif option == MenuOption.DECRYPT_IMAGE:
        decrypt_image_option(turtlpass)
    else:
        print("Invalid option.")

def main() -> None:
    draw_turtle()
    draw_ascii_art()
    print("Welcome to TurtlPass!")

    usb_devices = list_usb_devices()
    if not usb_devices:
        print("No USB devices detected.")
        print("Exiting...")
        return

    device_path = select_device(usb_devices)
    with TurtlPassRP2040(device_path=device_path) as turtlpass:
        while True:
            display_menu()
            user_input = input("Select an option: ")
            try:
                user_input_int = int(user_input)
                if user_input_int == MenuOption.EXIT.value:
                    print("Exiting...")
                    break
                elif 1 <= user_input_int <= MenuOption.DECRYPT_IMAGE.value:
                    handle_option(MenuOption(user_input_int), turtlpass)
                else:
                    print("Invalid option. Please enter a number between 0 and", MenuOption.DECRYPT_IMAGE.value)
            except ValueError:
                print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()
