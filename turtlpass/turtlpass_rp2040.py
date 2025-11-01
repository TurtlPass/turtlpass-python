from __future__ import annotations
import os
from typing import Any
import serial
from io import BytesIO
from types import TracebackType
from tqdm import tqdm
from proto import turtlpass_pb2


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

    def send_proto_command(self, cmd: turtlpass_pb2.Command) -> None:
        # ensures the device isn’t still holding text from a previous run
        self.device.reset_input_buffer()
        self.device.reset_output_buffer()

        """Send a protobuf message (with length prefix)"""
        data = cmd.SerializeToString()
        size = len(data).to_bytes(2, "little") # 2-byte length prefix
        self.device.write(size + data)

    def receive_proto_response(self) -> turtlpass_pb2.Response:
        """Receive a protobuf message (with length prefix)"""
        size_bytes = self.device.read(2)
        if len(size_bytes) < 2:
            raise IOError("Failed to read response length")
        size = int.from_bytes(size_bytes, "little")
        resp_data = self.device.read(size)
        resp = turtlpass_pb2.Response()
        resp.ParseFromString(resp_data)
        return resp
