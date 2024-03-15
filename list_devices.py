import glob

def list_usb_devices():
    usb_devices = glob.glob('/dev/cu.*')
    usb_modem_devices = [device for device in usb_devices if 'usbmodem' in device]
    return usb_modem_devices
