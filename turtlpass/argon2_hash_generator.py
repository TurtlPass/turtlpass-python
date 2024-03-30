import argon2
import hashlib

class Argon2Parameters:
    # Define Argon2 parameters
    T_COST = 32  # Number of iterations
    PARALLELISM = 4  # Number of threads in parallel
    M_COST = 65536  # Memory cost in kibibytes (64 MiB)
    HASH_LENGTH = 64  # Hash length in bytes
    ARGON2_VERSION = argon2.low_level.Type.ID

def generate_secure_hash(pin: int, domain_name: str, account_id: str) -> str:
    # Generate salt using SHA-512
    salt_input = domain_name + account_id
    salt_hash = hashlib.sha512(salt_input.encode()).hexdigest()

    # Configure Argon2 parameters
    argon2_hash = argon2.low_level.hash_secret_raw(
        str(pin).encode(),  # PIN converted to string and encoded
        salt_hash.encode(),  # salt
        Argon2Parameters.T_COST,  # Number of iterations
        Argon2Parameters.M_COST,  # Memory cost in KiB
        Argon2Parameters.PARALLELISM,  # Number of threads
        Argon2Parameters.HASH_LENGTH,  # Output hash length
        Argon2Parameters.ARGON2_VERSION  # Argon2 version
    )

    # Convert hash value to hexadecimal
    hashed_hex = argon2_hash.hex()

    # Return hashed value
    return hashed_hex
