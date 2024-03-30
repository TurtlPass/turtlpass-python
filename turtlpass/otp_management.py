import time
from io import BytesIO
from turtlpass.turtlpass_rp2040 import TurtlPassRP2040

def generate_otp_code(turtlpass: TurtlPassRP2040, secure_hash: str, timestamp = int(time.time())):
    command = f"@{secure_hash}:{timestamp}"
    resp = turtlpass.send_command(command)
    if resp == b"<OTP-READY>":
        print("✅ OTP code is Ready! Touch the sensor to be typed automatically...")
        return True
    else:
        print("❌ OTP Error")
        print(resp)
        return False

def add_otp_shared_secret(turtlpass: TurtlPassRP2040, secure_hash: str, otp_shared_secret: str):
    command = f"+{secure_hash}:{otp_shared_secret}"
    resp = turtlpass.send_command(command)
    if resp == b"<OTP-ADDED>":
        print("➕ OTP shared secret was added to the EEPROM")
        return True
    else:
        print("❌ OTP Error")
        print(resp)
        return False

def get_encrypted_otp_secrets(turtlpass: TurtlPassRP2040) -> None:
    turtlpass.send_command_read_until_end("?")

def delete_all_secrets_from_eeprom(turtlpass: TurtlPassRP2040):
    command = f"*"
    resp = turtlpass.send_command(command)
    if resp == b"<OTP-RESET>":
        print("🗑️  All OTP shared secrets deleted from EEPROM")
        return True
    else:
        print("❌ OTP Reset Error")
        print(resp)
        return False
