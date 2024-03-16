from io import BytesIO
from turtlpass.turtlpass_rp2040 import TurtlPassRP2040

def generate_password(turtlpass: TurtlPassRP2040, secure_hash: str) -> None:
    command = f"/{secure_hash}"
    resp = turtlpass.send_command(command)
    if resp == b"<PASSWORD-READY>":
        print("✅ Password Ready! Touch the sensor to be typed automatically...")
    else:
        print("❌ Password Error!")
