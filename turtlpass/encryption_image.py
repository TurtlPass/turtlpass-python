import time
import os
import zlib
import hashlib
import numpy as np
from io import BytesIO
from PIL import Image
from enum import Enum
from typing import Union
from tqdm import tqdm
from turtlpass.turtlpass_rp2040 import TurtlPassRP2040

def process_image_encryption(turtlpass: TurtlPassRP2040, mode: str, secure_hash: str, src_file: str, dst_file: str) -> None:
    # open source and destination image files
    src_image = Image.open(src_file)
    dst_image = Image.new(src_image.mode, src_image.size)  # create a new image as a clone of the source

    # prepare to iterate over pixels
    src_pixels = src_image.load()
    dst_pixels = dst_image.load()

    action = "Encrypting" if mode == "encrypt" else "Decrypting"
    print(f"{action}...")
    print("Image file:", src_file)

    command = ">" if mode == "encrypt" else "<"
    response_expected = b"<ENCRYPTING>" if mode == "encrypt" else b"<DECRYPTING>"

    resp = turtlpass.send_command(command)
    if resp != response_expected:
        raise ValueError(f"Unexpected response from device: {resp}")

    # get total number of pixels
    width, height = src_image.size
    total_pixels = width * height

    chunk_size = 8190 # multiple of 3
    
    # calculate total number of chunks
    total_chunks = int(np.ceil(total_pixels / chunk_size))

    # tqdm for progress bar
    with tqdm(total=total_chunks, unit='chunk') as pbar:
        # Iterate over chunks of pixels
        for chunk_idx in range(total_chunks):
            # get the starting and ending index of the current chunk
            start_idx = chunk_idx * chunk_size
            end_idx = min((chunk_idx + 1) * chunk_size, total_pixels)

            # initialize chunk data
            chunk_data = bytearray()

            # iterate over pixels in the current chunk
            for pixel_idx in range(start_idx, end_idx):
                # convert pixel index to coordinates
                y, x = divmod(pixel_idx, width)

                # extract RGB values from source image
                pixel_value = src_pixels[x, y]

                if len(pixel_value) == 4:
                    r, g, b, _ = pixel_value  # Unpack RGB values, ignoring alpha channel
                else:
                    r, g, b = pixel_value  # Unpack RGB values without alpha channel

                # convert RGB to byte array
                rgb_bytearray = bytearray([r, g, b])

                # append RGB byte array to chunk data
                chunk_data.extend(rgb_bytearray)

            response_chunk = turtlpass.send_bytes_get_response(chunk_data)

            # write encrypted or decrypted chunk data to destination image
            for pixel_idx, offset in enumerate(range(start_idx, end_idx)):
                # convert pixel index to coordinates
                y, x = divmod(offset, width)

                # get start and end byte index for the current pixel
                start_byte_idx = pixel_idx * 3
                end_byte_idx = start_byte_idx + 3

                # get encrypted RGB values for the current pixel
                rgb_bytearray = response_chunk[start_byte_idx:end_byte_idx]

                # write encrypted or decrypted RGB values to destination image
                dst_pixels[x, y] = tuple(rgb_bytearray)

            # update progress bar
            pbar.update(1)

    # save the destination image
    dst_image.save(dst_file)
    print(f"{action} completed. Image written to:", dst_file)

    # close files
    src_image.close()
    dst_image.close()
