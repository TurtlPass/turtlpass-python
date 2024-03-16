from __future__ import annotations
import os
from typing import Any
import serial
from io import BytesIO
from types import TracebackType
from tqdm import tqdm

class TurtlPassRP2040:
    BUFFER_SIZE = 8192
    BAUD_RATE = 115200

    def __init__(self, *, device_path: str) -> None:
        self.device_path = device_path
        self.device: Any = None

    def __enter__(self) -> TurtlPassRP2040:
        self.initialize_device()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        _exc_stack: TracebackType | None,
    ) -> None:
        if exc_type:
            print(f"Error: {exc_type.__name__}: {exc_value}")
        self.device.close()

    def initialize_device(self) -> None:
        if not os.path.exists(self.device_path):
            raise FileNotFoundError("USB device not found: ", self.device_path)
        self.device = serial.Serial(self.device_path, TurtlPassRP2040.BAUD_RATE)

    def send_command(self, command: str):
        self.device.write(str.encode(command) + b"\n")
        return self.device.readline().strip() # strip \r\n

    def send_command_read_until_end(self, command: str) -> None:
        self.device.write(str.encode(command) + b"\n")
        read = False
        while True:
            if self.device.in_waiting:
                raw = self.device.readline().strip()
                if not raw:
                    return
                print(raw.decode())
                read = True
            else:
                if read:
                    return

    def send_bytes_write_file(turtlpass: TurtlPassRP2040, src_bytes: BytesIO, dst_file: str) -> None:
        total_size = src_bytes.getbuffer().nbytes
        with open(dst_file, "wb") as f:
            with tqdm(total=total_size, unit='B', unit_scale=True, desc='TX/RX', leave=False) as pbar:
                for chunk in iter(lambda: src_bytes.read(turtlpass.BUFFER_SIZE), b''):
                    turtlpass.device.write(chunk)
                    data_received = turtlpass.device.read(len(chunk))
                    f.write(data_received)
                    pbar.update(len(chunk))
