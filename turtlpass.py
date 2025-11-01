from enum import Enum
from turtlpass.list_devices import list_usb_devices
from turtlpass.turtlpass_rp2040 import TurtlPassRP2040
from turtlpass.argon2_hash_generator import generate_secure_hash
from proto import turtlpass_pb2
import hashlib, unicodedata
from mnemonic import Mnemonic
from getpass import getpass
import binascii


class MenuOption(Enum):
    EXIT = 0
    GET_DEVICE_INFO = 1
    GENERATE_PASSWORD = 2
    INITIALIZE_SEED = 3
    GENERATE_MNEMONIC_AND_SEED = 4
    RESTORE_SEED_FROM_MNEMONIC = 5
    FACTORY_RESET = 6

def draw_turtle():
    print("                               ___-------___")
    print("                           _-~~             ~~-_")
    print("                        _-~                    /~-_")
    print("     /^\\__/^\\         /~  \\                   /    \\")
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
    # ANSI color codes
    BLUE = "\033[94m"    # Bright blue
    GREEN = "\033[92m"   # Bright green
    RED = "\033[91m"     # Bright red
    RESET = "\033[0m"    # Reset color
    BOLD = "\033[1m"

    print("Options:")
    print("0. <Exit>")
    print(f"1. {BLUE}Get TurtlDevice Information{RESET}")
    print(f"2. {BOLD}{GREEN}Generate Password on TurtlDevice{RESET}")
    print("3. Initialize TurtlDevice with 512-bit Seed")
    print("4. Generate 24-word Mnemonic and Derive 512-bit Seed")
    print("5. Restore 512-bit Seed from a 24-word Mnemonic")
    print(f"6. {RED}Factory Reset TurtlDevice (⚠️  DANGEROUS){RESET}")


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
    print("1. Get TurtlDevice Information")
    draw_soft_line()

    # Build protobuf command
    cmd = turtlpass_pb2.Command(type=turtlpass_pb2.CommandType.GET_DEVICE_INFO)

    # Send it to the device
    turtlpass.send_proto_command(cmd)

    resp = turtlpass.receive_proto_response()

    if not resp.success:
        print(f"\n❌ Error  : {turtlpass_pb2.ErrorCode.Name(resp.error)}")
        if resp.data:
            print(f"✉️  Message: {resp.data.decode() if isinstance(resp.data, bytes) else resp.data}")
        draw_line()
        return

    info = resp.device_info
    print(f"TurtlPass Firmware Version: {info.turtlpass_version}")
    print(f"Arduino Version: {info.arduino_version}")
    print(f"Compiler Version: {info.compiler_version}")
    print(f"nanopb Version: {info.nanopb_version}")
    print(f"Board Name: {info.board_name}")
    print(f"Unique Board ID: {info.unique_board_id.hex().upper()}")
    draw_line()


def generate_password_option(turtlpass: TurtlPassRP2040) -> None:
    draw_line()
    print("2. Generate Password on TurtlDevice")
    draw_soft_line()

    # Ask user for inputs
    length, charset = get_password_generation_params()
    secure_hash = get_input_and_hash()

    # Build protobuf command
    cmd = turtlpass_pb2.Command(
        type=turtlpass_pb2.CommandType.GENERATE_PASSWORD,
        gen_pass=turtlpass_pb2.GeneratePasswordParams(
            entropy = bytes.fromhex(secure_hash),  # raw bytes, not UTF-8 of hex
            length=length,
            charset=charset
        )
    )

    # Send it to the device
    turtlpass.send_proto_command(cmd)

    # --- Receive ---
    resp = turtlpass.receive_proto_response()

    if not resp.success:
        print(f"\n❌ Error  : {turtlpass_pb2.ErrorCode.Name(resp.error)}")
        if resp.data:
            print(f"✉️  Message: {resp.data.decode() if isinstance(resp.data, bytes) else resp.data}")
        draw_line()
        return

    del secure_hash
    print("\n✅ Password successfully generated")
    draw_line()


def get_password_generation_params() -> tuple[int, int]:
    """
    Ask the user for password length and charset selection.
    Defaults:
        length = 100
        charset = LETTERS_NUMBERS
    Returns:
        (length, charset_enum)
    """
    # --- Ask for password length ---
    while True:
        user_input = input("Enter desired password length (1-128) [\033[92mpress ENTER to use 100\033[0m]: ").strip()
        if user_input == "":
            length = 100
            break
        try:
            length = int(user_input)
            if 1 <= length <= 256:
                break
            else:
                print("❌ Please enter a number between 1 and 128 (or press Enter for default).")
        except ValueError:
            print("❌ Invalid input.")

    # --- Ask for charset ---
    print("Select character set:")
    print("1. Numbers (0–9)")
    print("2. Letters (a–z, A–Z)")
    print("3. Letters + Numbers (a–z, A–Z, 0–9)  [\033[92mdefault\033[0m]")
    print("4. Letters + Numbers + Symbols (a–z, A–Z, 0–9, symbols)")

    charset_map = {
        "1": turtlpass_pb2.Charset.NUMBERS_ONLY,
        "2": turtlpass_pb2.Charset.LETTERS_ONLY,
        "3": turtlpass_pb2.Charset.LETTERS_NUMBERS,
        "4": turtlpass_pb2.Charset.LETTERS_NUMBERS_SYMBOLS,
    }

    while True:
        charset_choice = input("Choose charset [\033[92mpress ENTER to use default\033[0m]: ").strip()
        if charset_choice == "" or charset_choice == "3":
            charset = turtlpass_pb2.Charset.LETTERS_NUMBERS
            break
        elif charset_choice in charset_map:
            charset = charset_map[charset_choice]
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4 (or press Enter for default).")

    return length, charset


def get_input_and_hash() -> str:
    print()
    domain_name = input("Enter Domain Name (e.g. 'google'): ")
    account_id = input("Enter Account ID (e.g. 'user@example.com'): ")
    pin = getpass("Enter PIN (e.g. '704713'): ")
    secure_hash = generate_secure_hash(pin, domain_name, account_id)
    del domain_name, account_id, pin
    return secure_hash


def initialize_seed_option(turtlpass: TurtlPassRP2040) -> None:
    """
    Initialize the TurtlDevice with a 512-bit (64-byte) seed in hex format.
    The user must enter exactly 128 hexadecimal characters (512 bits).
    """
    draw_line()
    print("3. Initialize TurtlDevice with 512-bit Seed")
    draw_soft_line()

    # --- Prompt for seed input ---
    seed_input = input("Enter 512-bit seed as 128 hex characters: ").strip()

    # --- Validation ---
    if not seed_input:
        print("\n❌ Error: Seed input cannot be empty.")
        draw_line()
        return

    # Normalize (remove possible spaces)
    seed_input = seed_input.replace(" ", "").lower()

    if len(seed_input) != 128:
        print(f"\n❌ Error: Expected 128 hex characters (512 bits), got {len(seed_input)}.")
        draw_line()
        return

    # Ensure valid hexadecimal characters
    try:
        seed_bytes = binascii.unhexlify(seed_input)
    except (binascii.Error, ValueError):
        print("\n❌ Error: Seed must contain only valid hexadecimal characters (0-9, a-f).")
        draw_line()
        return

    # --- Build protobuf command ---
    cmd = turtlpass_pb2.Command()
    cmd.type = turtlpass_pb2.CommandType.INITIALIZE_SEED
    cmd.init_seed.seed = seed_bytes

    # --- Send command ---
    turtlpass.send_proto_command(cmd)

    # --- Receive and parse response ---
    resp = turtlpass.receive_proto_response()

    if not resp.success:
        print(f"\n❌ Error  : {turtlpass_pb2.ErrorCode.Name(resp.error)}")
        if resp.data:
            print(f"✉️  Message: {resp.data.decode() if isinstance(resp.data, bytes) else resp.data}")
        draw_line()
        return

    print("\n✅ Seed initialized successfully (512-bit seed accepted)")
    draw_line()


def generate_seed_from_mnemonic_option() -> None:
    """
    Generate a 24-word BIP-39 mnemonic and derive a 512-bit seed (PBKDF2-HMAC-SHA512).
    Compatible with BIP-39. Prints mnemonic and seed for user backup.

    PBKDF2-HMAC-SHA512 with:
      - password = mnemonic sentence (UTF-8 NFKD)
      - salt = "mnemonic" + passphrase (UTF-8 NFKD)
      - iterations = 1048576
      - key length = 64 bytes (512 bits)
    """
    draw_line()
    print("4. Generate 24-word Mnemonic and Derive 512-bit Seed")
    draw_soft_line()

    # Generate mnemonic (24 words, 256 bits entropy)
    mnemo = Mnemonic("english")
    mnemonic = mnemo.generate(strength=256)
    print(f"⚙️  Generated 24-word mnemonic:\n\n{mnemonic}\n")
    print("⚠️  Write these 24 words down and store them securely! They are your full seed.\n")

    # Get optional passphrase
    passphrase_input = getpass("Enter a new passphrase (input hidden, leave blank if none): ")
    if passphrase_input:
        passphrase = passphrase_input
        print("⚙️  Using custom passphrase.")
    else:
        passphrase = ""
        print("⚙️  No passphrase defined.")

    # Normalize inputs (BIP-39 NFKD normalization)
    mnemonic_norm = unicodedata.normalize("NFKD", mnemonic)
    salt = "mnemonic" + unicodedata.normalize("NFKD", passphrase)

    # Derive seed using PBKDF2-HMAC-SHA512
    seed_bytes = hashlib.pbkdf2_hmac(
        "sha512",
        mnemonic_norm.encode("utf-8"),
        salt.encode("utf-8"),
        iterations=1048576,  # custom 1 M (1048576); 2048 = BIP-39 standard;
        dklen=64             # 64 bytes = 512 bits, BIP-39 mnemonics standard
    )

    print("\n✅  Seed successfully derived (512-bit)") # 512-bit, 64 bytes, hex = 128 chars
    print(f"🔑  Seed (hex):\n{seed_bytes.hex()}\n")
    draw_line()


def restore_seed_from_user_mnemonic() -> None:
    """
    Restore or generate a BIP-39 seed from a user-provided mnemonic and optional passphrase.
    The derived seed will be 512 bits (64 bytes), compliant with BIP-39.
    """
    draw_line()
    print("5. Restore 512-bit Seed from a 24-word Mnemonic")
    draw_soft_line()

    mnemo = Mnemonic("english")

    # Prompt for mnemonic input
    print("🧠  Please enter your 24-word mnemonic phrase:")
    mnemonic_input = input(">>> ").strip()

    # Basic validation
    if not mnemonic_input:
        print("\n❌  Error: mnemonic cannot be empty.")
        draw_line()
        return

    # Normalize spaces and validate word count
    mnemonic_words = mnemonic_input.split()
    if len(mnemonic_words) != 24:
        print(f"\n❌  Invalid mnemonic length: expected 24 words, got {len(mnemonic_words)}.")
        print("    Please ensure you entered exactly 24 words separated by spaces.")
        draw_line()
        return

    # Normalize spacing (replace multiple spaces, strip ends)
    mnemonic_input = " ".join(mnemonic_input.split())

    # Validate mnemonic
    if not mnemo.check(mnemonic_input):
        print("\n⚠️  Invalid mnemonic: checksum or wordlist mismatch.")
        print("    Please ensure you entered all words correctly.")
        draw_line()
        return
    print("✅  Mnemonic is valid.")

    # Optional passphrase
    passphrase_input = getpass("Enter your passphrase (input hidden, leave blank if none): ")
    passphrase = passphrase_input or ""
    if passphrase:
        print("⚙️  Using provided passphrase.")
    else:
        print("⚙️  No passphrase defined.")

    # Normalize (NFKD) per BIP-39
    mnemonic_norm = unicodedata.normalize("NFKD", mnemonic_input)
    salt = "mnemonic" + unicodedata.normalize("NFKD", passphrase)

    # Derive seed using PBKDF2-HMAC-SHA512
    seed_bytes = hashlib.pbkdf2_hmac(
        "sha512",
        mnemonic_norm.encode("utf-8"),
        salt.encode("utf-8"),
        iterations=1048576,  # custom 1 M (1048576); 2048 = BIP-39 standard;
        dklen=64             # 64 bytes = 512 bits, BIP-39 mnemonics standard
    )
    print("\n✅  Seed successfully derived (512-bit)")
    print(f"🔑  Seed (hex):\n{seed_bytes.hex()}\n")


def factory_reset_option(turtlpass: TurtlPassRP2040) -> None:
    draw_line()
    print("6. Factory Reset TurtlDevice (⚠️  DANGEROUS)")
    draw_soft_line()

    # Confirmation prompt
    confirm = input("⚠️ This will ERASE all data on your TurtlDevice. Type 'YES' to confirm: ").strip()
    if confirm.upper() != "YES":
        print("\n❎ Factory reset canceled by user")
        draw_line()
        return

    cmd = turtlpass_pb2.Command(type=turtlpass_pb2.CommandType.FACTORY_RESET)
    turtlpass.send_proto_command(cmd)

    resp = turtlpass.receive_proto_response()
    if resp is None:
        print("\n❌ No response or framing error")
        draw_line()
        return

    if not resp.success:
        print(f"\n❌ Error  : {turtlpass_pb2.ErrorCode.Name(resp.error)}")
        if resp.data:
            print(f"✉️  Message: {resp.data.decode() if isinstance(resp.data, bytes) else resp.data}")
        draw_line()
        return

    print(f"\n✅ Factory Reset Success")
    draw_line()


def handle_option(option: MenuOption, turtlpass: TurtlPassRP2040) -> None:
    match option:
        case MenuOption.GET_DEVICE_INFO:
            get_device_information(turtlpass)
        case MenuOption.GENERATE_PASSWORD:
            generate_password_option(turtlpass)
        case MenuOption.INITIALIZE_SEED:
            initialize_seed_option(turtlpass)
        case MenuOption.GENERATE_MNEMONIC_AND_SEED:
            generate_seed_from_mnemonic_option()
        case MenuOption.RESTORE_SEED_FROM_MNEMONIC:
            restore_seed_from_user_mnemonic()
        case MenuOption.FACTORY_RESET:
            factory_reset_option(turtlpass)
        case _:
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
                option = MenuOption(user_input_int)
            except ValueError:
                print("Invalid option.")
                continue

            if option == MenuOption.EXIT:
                print("Exiting...")
                break
            else:
                handle_option(option, turtlpass)

if __name__ == "__main__":
    main()
