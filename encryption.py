import time
import os
from io import BytesIO
from turtlpass_rp2040 import TurtlPassRP2040
from checksum import calculate_checksum

def process_encryption(turtlpass: TurtlPassRP2040, mode: str, secure_hash: str, src_file: str, dst_file: str) -> None:
    if os.path.isfile(dst_file):
        os.remove(dst_file)

    if mode == "encrypt":
        start = time.time()
        encrypt_file(turtlpass, secure_hash, src_file, dst_file)
        print("Encryption took %.2fs" % (time.time() - start))

        time.sleep(1)

        tmp_file = src_file + ".tmp"
        if os.path.isfile(tmp_file):
            os.remove(tmp_file)

        start = time.time()
        decrypt_file(turtlpass, secure_hash, dst_file, tmp_file)
        print("Verification/Decryption took %.2fs" % (time.time() - start))

        src_checksum = calculate_checksum(src_file)
        tmp_checksum = calculate_checksum(tmp_file)
        os.remove(tmp_file)
        if src_checksum == tmp_checksum:
            print("✅ Checksums match. Verification successful.")
        else:
            print("❌ Checksums do not match. Verification failed.")
            os.remove(dst_file)

    elif mode == "decrypt":
        start = time.time()
        decrypt_file(turtlpass, secure_hash, src_file, dst_file)
        print("Decryption took %.2fs" % (time.time() - start))
        print("✅ Decryption successful.")

    else:
        raise ValueError("Invalid mode. Must be 'encrypt' or 'decrypt'.")

def encrypt_file(turtlpass: TurtlPassRP2040, secure_hash: str, src_file: str, dst_file: str) -> None:
    print("Encrypting file:", src_file)
    with open(src_file, "rb") as f:
        src_bytes = BytesIO(f.read())
    send_file_write_response(turtlpass, "encrypt", secure_hash, src_bytes, dst_file)
    print("Encrypted file written successfully: ", dst_file)

def decrypt_file(turtlpass: TurtlPassRP2040, secure_hash: str, src_file: str, dst_file: str) -> None:
    print("Decrypting file:", src_file)
    with open(src_file, "rb") as f:
        src_bytes = BytesIO(f.read())
    send_file_write_response(turtlpass, "decrypt", secure_hash, src_bytes, dst_file)
    print("Decrypted file written successfully: ", dst_file)

def send_file_write_response(turtlpass: TurtlPassRP2040, mode: str, secure_hash: str, src_bytes: BytesIO, dst_file: str) -> None:
    if mode not in {"encrypt", "decrypt"}:
        raise ValueError("Invalid mode. Must be 'encrypt' or 'decrypt'.")

    command = ">" if mode == "encrypt" else "<"
    response_expected = b"<ENCRYPTING>" if mode == "encrypt" else b"<DECRYPTING>"

    resp = turtlpass.send_command(command)
    if resp != response_expected:
        raise ValueError(f"Unexpected response from device: {resp}")

    turtlpass.send_bytes_write_file(src_bytes, dst_file)
