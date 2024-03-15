import time
import os
from list_devices import list_usb_devices
from turtlpass_rp2040 import TurtlPassRP2040
from argon2_hash_generator import generate_secure_hash
from password import generate_password
from otp_management import add_otp_shared_secret, get_encrypted_otp_secrets, generate_otp_code
from encryption import process_encryption

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
            option = input("Select an option: ")
            if option == "0":
                print("Exiting...")
                break
            elif option == "1":
                draw_line()
                print("1. Get Device Information")
                draw_soft_line()
                turtlpass.send_command_read_until_end("i")
                draw_line()
            elif option == "2":
                draw_line()
                print("2. Generate Password")
                draw_soft_line()
                domain_name = input("Enter Domain Name (e.g. 'google'): ")
                account_id = input("Enter Account ID (e.g. 'user@example.com'): ")
                pin = input("Enter PIN (e.g. '704713'): ")
                secure_hash = generate_secure_hash(pin, domain_name, account_id)
                del domain_name, account_id, pin
                generate_password(turtlpass, secure_hash)
                del secure_hash
                draw_line()
            elif option == "3":
                draw_line()
                print("3. Generate OTP Code")
                draw_soft_line()
                domain_name = input("Enter Domain Name (e.g. 'google'): ")
                account_id = input("Enter Account ID (e.g. 'user@example.com'): ")
                pin = input("Enter PIN (e.g. '704713'): ")
                secure_hash = generate_secure_hash(pin, domain_name, account_id)
                del domain_name, account_id, pin
                generate_otp_code(turtlpass, secure_hash)
                del secure_hash
                draw_line()
            elif option == "4":
                draw_line()
                print("4. Add OTP Shared Secret")
                draw_soft_line()
                otp_shared_secret = input("Enter OTP Shared Secret: ")
                draw_soft_line()
                domain_name = input("Enter Domain Name (e.g. 'google'): ")
                account_id = input("Enter Account ID (e.g. 'user@example.com'): ")
                pin = input("Enter PIN (e.g. '704713'): ")
                secure_hash = generate_secure_hash(pin, domain_name, account_id)
                del domain_name, account_id, pin
                add_otp_shared_secret(turtlpass, secure_hash, otp_shared_secret)
                del secure_hash, otp_shared_secret
                draw_line()
            elif option == "5":
                draw_line()
                print("5. Get Encrypted OTP Secrets")
                draw_soft_line()
                get_encrypted_otp_secrets(turtlpass)
                draw_line()
            elif option == "6":
                draw_line()
                print("6. Encrypt File")
                draw_soft_line()
                src_file = input("Enter input file name (e.g. 'files/turtle.jpg'): ")
                if not os.path.isfile(src_file):
                    print("Input file not found.")
                    draw_line()
                dst_file = input("Enter output file name (e.g. 'turtle.jpg.enc'): ")
                draw_soft_line()
                domain_name = input("Enter Domain Name (e.g. 'google'): ")
                account_id = input("Enter Account ID (e.g. 'user@example.com'): ")
                pin = input("Enter PIN (e.g. '704713'): ")
                secure_hash = generate_secure_hash(pin, domain_name, account_id)
                del domain_name, account_id, pin
                process_encryption(turtlpass, "encrypt", secure_hash, src_file, dst_file)
                del secure_hash, src_file, dst_file
                draw_line()
            elif option == "7":
                draw_line()
                print("7. Decrypt File")
                draw_soft_line()
                src_file = input("Enter input file name (e.g. 'turtle.jpg.enc'): ")
                if not os.path.isfile(src_file):
                    print("Input file not found.")
                    draw_line()
                dst_file = input("Enter output file name (e.g. 'turtle.jpg'): ")
                draw_soft_line()
                domain_name = input("Enter Domain Name (e.g. 'google'): ")
                account_id = input("Enter Account ID (e.g. 'user@example.com'): ")
                pin = input("Enter PIN (e.g. '704713'): ")
                secure_hash = generate_secure_hash(pin, domain_name, account_id)
                del domain_name, account_id, pin
                process_encryption(turtlpass, "decrypt", secure_hash, src_file, dst_file)
                del secure_hash, src_file, dst_file
                draw_line()
            else:
                draw_line()
                print("Invalid option. Please try again.")
                draw_line()

if __name__ == "__main__":
    main()
