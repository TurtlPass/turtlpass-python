<p align="center">
  <img src="https://raw.githubusercontent.com/TurtlPass/turtlpass-firmware-arduino/master/assets/icon.png" alt="Logo" width="133"/>
</p>

<h2 align="center">🔗 TurtlPass Ecosystem</h2>

<p align="center">
  🐢 <a href="https://github.com/TurtlPass/turtlpass-firmware-arduino"><b>Firmware</b></a> •
  💾 <a href="https://github.com/TurtlPass/turtlpass-protobuf"><b>Protobuf</b></a> •
  💻 <a href="https://github.com/TurtlPass/turtlpass-python"><b>Host</b></a> •
  🌐 <a href="https://github.com/TurtlPass/turtlpass-chrome-extension"><b>Chrome</b></a> •
  📱 <a href="https://github.com/TurtlPass/turtlpass-android"><b>Android</b></a>
</p>

---

# 💻 TurtlPass Host (Python CLI)

[![](https://img.shields.io/github/v/release/TurtlPass/turtlpass-python?color=green&label=Release&logo=python)](https://github.com/TurtlPass/turtlpass-python/releases/latest "GitHub Release")
[![](https://img.shields.io/badge/Python-v3.10+-green?logo=python)](https://docs.python.org/3.10/ "Python 3.10+")
[![](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT "License: MIT")
[![](https://img.shields.io/badge/Documentation-green?label=GitBook&logo=gitbook)](https://ryanamaral.gitbook.io/turtlpass "GitBook Documentation")

A minimal **host-side command-line client** for interacting with **TurtlPass** hardware devices via USB.
Generate passwords, manage cryptographic seeds, and control your TurtlPass device **securely and locally** — all from the terminal.

---

## ⚡ Features

* 🔌 **Automatic Device Detection** — Instantly detects connected TurtlPass devices
* 🔐 **Secure Password Generation** — Fully configurable length & charset
* 🧬 **Seed Management** — Initialize, generate, or restore 512-bit seeds from 24-word BIP-39 mnemonics
* 💥 **Factory Reset** — Safely reset your device to factory defaults
* 🔒 **Hardware Security** — All cryptography happens on-device; seeds never leave the TurtlPass

---

## ⚙️ Requirements

* Python **3.10+**
* **TurtlPass device**
* **USB cable** with data support

---

## 📦 Installation

```bash
git clone https://github.com/TurtlPass/turtlpass-python.git
cd turtlpass-python
python -m pip install -r requirements.txt
```

---

## 🚀 Usage

1. Plug in your **TurtlPass** device and run:

   ```bash
   python turtlpass.py
   ```

2. Choose from the interactive menu:

   ```
   ████████╗██╗░░░██╗██████╗░████████╗██╗░░░░░██████╗░░█████╗░░██████╗░██████╗
   ╚══██╔══╝██║░░░██║██╔══██╗╚══██╔══╝██║░░░░░██╔══██╗██╔══██╗██╔════╝██╔════╝
   ░░░██║░░░██║░░░██║██████╔╝░░░██║░░░██║░░░░░██████╔╝███████║╚█████╗░╚█████╗░
   ░░░██║░░░██║░░░██║██╔══██╗░░░██║░░░██║░░░░░██╔═══╝░██╔══██║░╚═══██╗░╚═══██╗
   ░░░██║░░░╚██████╔╝██║░░██║░░░██║░░░███████╗██║░░░░░██║░░██║██████╔╝██████╔╝
   ░░░╚═╝░░░░╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═╝░░░░░╚═╝░░╚═╝╚═════╝░╚═════╝░
   Welcome to TurtlPass!
   Device detected: /dev/cu.usbmodem14101
   Options:
   0. <Exit>
   1. Get TurtlDevice Information
   2. Generate Password on TurtlDevice
   3. Initialize TurtlDevice with 512-bit Seed
   4. Generate 24-word Mnemonic and Derive 512-bit Seed
   5. Restore 512-bit Seed from a 24-word Mnemonic
   6. Factory Reset TurtlDevice (⚠️ DANGEROUS)
   Select an option: 
   ```

---

## 📖 Usage Example: Generate a Password

```
2. Generate Password on TurtlDevice
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
Enter desired password length (1-128) [press ENTER to use 100]: 128
Select character set:
1. Numbers (0–9)
2. Letters (a–z, A–Z)
3. Letters + Numbers (a–z, A–Z, 0–9)  [default]
4. Letters + Numbers + Symbols (a–z, A–Z, 0–9, symbols)
Choose charset [press ENTER to use default]: 4

Enter Domain Name (e.g. 'google'): github
Enter Account ID (e.g. 'user@example.com'): turtlpass@ryanamaral.com
Enter PIN (e.g. '704713'): ******

✅ Password successfully generated
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
```

All passwords are generated **on-device**, ensuring maximum security.

---

## 💻 Supported Platforms

| OS      | Status      |
| ------- | ----------- |
| Linux   | ✅ Supported |
| macOS   | ✅ Supported |
| Windows | ✅ Supported |

---

## 🧰 Troubleshooting

* **Device not detected:** Ensure USB cable supports data transfer and device is plugged in
* **Linux users:** You may need to add a `udev` rule for USB access
* **macOS users:** Check `/dev/cu.*` to find the connected device
* **Windows users:** Verify COM port and drivers

---

## 📚 Dependencies

* [argon2-cffi](https://pypi.org/project/argon2-cffi/) — Secure Argon2 key derivation and password hashing
* [pyserial](https://pypi.org/project/pyserial/) — USB communication with the TurtlPass device
* [protobuf](https://pypi.org/project/protobuf/) — Protocol Buffers serialization for device messages
* [mnemonic](https://pypi.org/project/mnemonic/) — BIP-39 mnemonic generation and seed handling

---

## 📜 License

This repository is licensed under the [MIT License](./LICENSE).
