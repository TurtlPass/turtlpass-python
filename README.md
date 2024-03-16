<p align="center">
<img src="https://raw.githubusercontent.com/TurtlPass/turtlpass-firmware-arduino/main/assets/icon.png" alt="logo" width=90>
<h3 align="center">TurtlPass Python</h3>
<p align="center">
TurtlPass client application written in Python. It provides a simple command-line interface (CLI) for interacting with TurtlPass-enabled devices connected via USB. This project aims to demonstrate all features present in the TurtlPass Firmware 2.X.X for RP2040 microcontroller-based devices.</p>


## ⚡ Features

* **TurtlPass Device Interaction**
	* Communicate with TurtlPass-enabled devices connected via USB
* **Generate Passwords**
	* Generate strong passwords securely using TurtlPass
* **Generate OTP Codes**
	* Generate one-time passwords (OTP) for two-factor authentication
* **Add OTP Shared Secrets to EEPROM**
	* Add OTP shared secrets securely to the TurtlPass device
* **Encrypt and Decrypt Files**
	* Encrypt and decrypt files using TurtlPass for secure storage


## Requirements
* Python 3+
* RP2040-based TurtlPass device
* USB cable


## Installation
1. Clone the repository:

	```bash
	git clone https://github.com/TurtlPass/turtlpass-python.git
	```

2. Navigate to the project directory:

	```bash
	cd turtlpass-python
	```

3. Install dependencies:

	```bash
	pip install -r requirements.txt
	```

## Usage

1. Connect your RP2040-based TurtlPass device to your computer via USB.

2. Run the `turtlpass.py` script:

	```bash
	python turtlpass.py
	```

3. Follow the on-screen instructions to interact with the TurtlPass device and perform various actions.

	```
	                               ___-------___
	                           _-~~             ~~-_
	                        _-~                    /~-_
	     /^\__/^\         /~  \                   /    \
	   /|  O|| O|        /      \_______________/        \
	  | |___||__|      /       /                \          \
	  |          \    /      /                    \          \
	  |   (_______) /______/                        \_________ \
	  |         / /         \                      /            \
	   \         \^\\         \                  /               \     /
	     \         ||           \______________/      _-_       //\__//
	       \       ||------_-~~-_ ------------- \ --/~   ~\    || __/
	         ~-----||====/~     |==================|       |/~~~~~
	          (_(__/  ./     /                    \_\      \.
	                 (_(___/                         \_____)_)   [art by jurcy]
	
	████████╗██╗░░░██╗██████╗░████████╗██╗░░░░░██████╗░░█████╗░░██████╗░██████╗
	╚══██╔══╝██║░░░██║██╔══██╗╚══██╔══╝██║░░░░░██╔══██╗██╔══██╗██╔════╝██╔════╝
	░░░██║░░░██║░░░██║██████╔╝░░░██║░░░██║░░░░░██████╔╝███████║╚█████╗░╚█████╗░
	░░░██║░░░██║░░░██║██╔══██╗░░░██║░░░██║░░░░░██╔═══╝░██╔══██║░╚═══██╗░╚═══██╗
	░░░██║░░░╚██████╔╝██║░░██║░░░██║░░░███████╗██║░░░░░██║░░██║██████╔╝██████╔╝
	░░░╚═╝░░░░╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═╝░░░░░╚═╝░░╚═╝╚═════╝░╚═════╝░
	Welcome to TurtlPass!
	Device detected: /dev/cu.usbmodem14101
	Options:
	0. Exit
	1. Get Device Information
	2. Generate Password
	3. Generate OTP Code
	4. Add OTP Shared Secret
	5. Get Encrypted OTP Secrets
	6. Encrypt File
	7. Decrypt File
	Select an option:
	```


## Sample Files

In the `/files` directory, you'll find several sample files of varying sizes. These files are provided to facilitate testing and demonstrate the encryption and decryption capabilities of TurtlPass. The sample CSV files have been sourced from [here](https://github.com/datablist/sample-csv-files).


## Contributing

Contributions are welcome! If you find any bugs or have suggestions for new features, please open an issue or submit a pull request.


## 📄 License

TurtlPass Python is released under the [MIT License](https://github.com/TurtlPass/turtlpass-python/blob/master/LICENSE).
