import argparse
from turtlpass.argon2_hash_generator import generate_secure_hash

def test_hash_generation(domain_name: str, account_id: str, pin: int, expected_hash: str) -> None:
    secure_hash = generate_secure_hash(pin, domain_name, account_id)

    if secure_hash == expected_hash:
        print(f"✅ Hashes match for domain '{domain_name}', account '{account_id}', and PIN '{pin}'.")
    else:
        print(f"❌ Hashes do not match for domain '{domain_name}', account '{account_id}', and PIN '{pin}'.")
        print(f"Expected hash: {expected_hash}")
        print(f"Actual hash  : {secure_hash}")

def main() -> None:
    test_cases = [
        {"domain_name": "amazon", "account_id": "amazon@mail.com", "pin": 704713, "expected_hash": "cfb82615cbd35b67ff2efd2bd4b70aff071d02feaa21549a587c268b3f11ef2d0bbf0673f70f4cd84072051d2bb3c64e2b5eba1a2733983534a95651ae436c5b"},
        {"domain_name": "google", "account_id": "google@mail.com", "pin": 631571, "expected_hash": "560303a41e2e97b205d3101d00a62e4e74383d0dc58032570512df0c70a92bd9bb7fbf1aa491eefcf3618b2e5a101657de69aafae9b1d3b8e7abce8369d551ad"},
        {"domain_name": "facebook", "account_id": "facebook@mail.com", "pin": 363873, "expected_hash": "a6e5c9ff8cf0670fe58d3a4949adcb610fa7b26cee9a98d6617f5a53185e73a02d2e0a855655b704d55d54bfd84d07ae12cb2f4cdeee0f03e146cd206ccf368f"},
        {"domain_name": "twitter", "account_id": "twitter@mail.com", "pin": 180366, "expected_hash": "bcc8da7302b09ce81e8f2cca813913c2ccaf39ad7664fbf9d865952c4bae5dc3fdca57617abfd27ba8032cc3f44513f92c97bef7a48e4d89bbb05fbf9b7a6bd5"},
        {"domain_name": "linkedin", "account_id": "linkedin@mail.com", "pin": 442071, "expected_hash": "e45270ad5b032e73127ef73dd25ce42e4ac28e77aa0d0183d4ab37049f05a9f9b7dacd9590399a482b5eccce743425eb96a66117949511757b1fae45809afd7a"},
        {"domain_name": "apple", "account_id": "apple@mail.com", "pin": 246810, "expected_hash": "d1b301bf0d57357e8188dee2559fd5a5502102a4dc9b351ea4edc7f4528cfa3f08e8c1b05d39271fc081ff272955c0f02d6ba846b0939a4bf5c67c88b5f1b25b"},
        {"domain_name": "instagram", "account_id": "instagram@mail.com", "pin": 331667, "expected_hash": "bcb666368f9214e8ecd827a60e5688f145b65524befd181cf66f01b109a5134f645f5acfef53c46543cea0045c6fb9076969020ad069e09eda60b62f40e7bdbc"},
        {"domain_name": "netflix", "account_id": "netflix@mail.com", "pin": 950688, "expected_hash": "80ff877241bc18df62be0779f7cbd5c4fd88c3492e9e8d288decea7ec0be04eeaae930071dc667541f910dde74288446d6553c0d78e317e437558b1a4c1ebee0"},
        {"domain_name": "spotify", "account_id": "spotify@mail.com", "pin": 217226, "expected_hash": "5b601b1632455d3c16717d04bb49fa8197dc9da1308355309f56bd1783726ca745ae9b684ed88518859671d943f70ae60aa8065e327674d02ba5cc0dd7f3128b"}
    ]
    for test_case in test_cases:
        test_hash_generation(test_case["domain_name"], test_case["account_id"], test_case["pin"], test_case["expected_hash"])

if __name__ == "__main__":
    main()
