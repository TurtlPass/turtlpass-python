import sys
import glob

def list_usb_devices():
    """
    List USB devices across platforms.

    macOS: /dev/cu.* (filters for 'usbmodem')
    Linux: /dev/ttyUSB* and /dev/ttyACM*
    Windows: COM ports via pyserial
    """
    if sys.platform.startswith("darwin"):
        # macOS
        usb_devices = glob.glob('/dev/cu.*')
        return [device for device in usb_devices if 'usbmodem' in device]

    elif sys.platform.startswith("linux"):
        # Linux
        usb_devices = glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')
        return usb_devices

    elif sys.platform.startswith("win"):
        # Windows
        try:
            from serial.tools import list_ports
        except ImportError:
            raise ImportError("Please install pyserial: pip install pyserial")

        ports = list_ports.comports()
        return [
            port.device
            for port in ports
            if "USB" in port.description.upper() or "ACM" in port.description.upper()
        ]

    else:
        raise OSError(f"Unsupported platform: {sys.platform}")
