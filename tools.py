import os

import piexif
import json
import numpy as np
from PIL import Image, ImageSequence, ImageOps
import torchvision.transforms.functional as F
from collections import namedtuple
import folder_paths
from io import BytesIO
import requests



class SaveNamedImage:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "seed": ("INT", {"default": -1}),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
                "filename_suffix": ("STRING", {"default": ".png"}),
                "callback_url": ("STRING", {"default": ""}),
                "generate_id": ("STRING", {"default": "-1"}),
                "timeout": ("INT", {"default": 5}),
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "run_it"

    OUTPUT_NODE = True

    CATEGORY = "biubiubiu/Image"

    def callback(self, url, timeout, results):
        try:
            requests.post(url=url, json=results, timeout=timeout)
        except Exception as e:
            print(e)

    def run_it(
        self,
        images,
        seed,
        filename_prefix="ComfyUI",
        filename_suffix=".png",
        callback_url="",
        timeout=5,
        generate_id="",
    ):
        full_output_folder, filename, counter, subfolder, filename_prefix = (
            folder_paths.get_save_image_path(
                filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0]
            )
        )

        results = list()
        for batch_number, image in enumerate(images):
            i = 255.0 * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))


            filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
            file = f"{filename_with_batch_num}_{counter:05}_{filename_suffix}"
            file_path = os.path.join(full_output_folder, file)
            custom_exif = {}
            if seed != -1:
                custom_exif['seed'] = seed
            custom_exif_json = json.dumps(custom_exif)
            exif_dict = {}
            exif_ifd = {piexif.ExifIFD.UserComment: custom_exif_json.encode()}
            exif_dict = {"0th": {}, "Exif": exif_ifd, "1st": {},
                    "thumbnail": None, "GPS": {}}
            exif_bytes = piexif.dump(exif_dict)

            img.save(file_path, exif=exif_bytes)

            results.append(
                {
                    "filename": file,
                    "subfolder": subfolder,
                    "type": self.type,
                    "generate_id": generate_id,
                }
            )
            counter += 1

        if callback_url != "":
            self.callback(callback_url, timeout, results)

        return {"ui": {"images": results}}