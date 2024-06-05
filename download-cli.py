# !/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
import os
import pkg_resources

os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
from huggingface_hub import snapshot_download, hf_hub_download
dir_path = os.path.dirname(os.path.abspath(__file__))
parser = argparse.ArgumentParser(description="Download the huggingface model.")

parser.add_argument("-r", "--repo_id", type=str, default="smthem/test-model")
parser.add_argument("-l", "--local_dir", type=str, default="models/diffusers")
parser.add_argument("-i", "--ignore_patterns", type=str, default="None")
parser.add_argument("-f", "--filename", type=str, default="")
parser.add_argument("-t", "--token", type=str, default="")

args = parser.parse_args()
repo_id = args.repo_id
local_dir = args.local_dir
ignore_patterns = args.ignore_patterns
filename = args.filename
token = args.token

if ignore_patterns == "big_files":
    ignore_patterns = ["*.safetensors", "*.bin", "*.pth", "*.model", "*.msgpack", "*.onnx_data", "*.onnx", "*.gguf",
                       "*.ckpt", "*.xml"]
elif ignore_patterns == "safetensors":
    ignore_patterns = ["*.safetensors"]
elif ignore_patterns == "bin":
    ignore_patterns = ["*.bin"]
elif ignore_patterns == "safetensors,bin":
    ignore_patterns = ["*.safetensors", "*.bin"]
elif ignore_patterns == "pth":
    ignore_patterns = ["*.pth"]
elif ignore_patterns == "safetensors,bin,pth":
    ignore_patterns = ["*.safetensors", "*.bin", "*.pth"]
elif ignore_patterns == "model":
    ignore_patterns = ["*.model"]
elif ignore_patterns == "msgpack":
    ignore_patterns = ["*.msgpack"]
elif ignore_patterns == "onnx_data":
    ignore_patterns = ["*.onnx_data"]
elif ignore_patterns == "onnx":
    ignore_patterns = ["*.onnx"]
else:
    ignore_patterns = None

hub_version = pkg_resources.get_distribution('huggingface_hub').version
hub_version = float(hub_version.split(".", 1)[-1])
if hub_version >= 23.0:  #0.23.0 delete local_dir_use_symlinks option
    if local_dir == "":
        download_model = snapshot_download(repo_id=repo_id, max_workers=4)
    else:
        path_dir = os.path.dirname(dir_path)
        path = os.path.dirname(path_dir)
        repo_list = repo_id.split('/')
        dir_list = local_dir.split('/')
        path = os.path.join(path, f"{dir_list[0]}", f"{dir_list[1]}", f"{repo_list[0]}", f"{repo_list[1]}")
        cache_dir = os.path.join(path, "cache")
        model_path = os.path.normpath(path)
        local_dir_use_symlinks = False

    if len(filename) > 0:
        get_model_path = hf_hub_download(repo_id=repo_id, filename=filename, cache_dir=cache_dir,
                                         local_dir=model_path,
                                         resume_download=True, token=token
                                         )
    else:
        download_model = snapshot_download(repo_id=repo_id, cache_dir=cache_dir, local_dir=model_path,
                                           token=token,
                                           ignore_patterns=ignore_patterns,
                                           max_workers=4
                                           )
else:
    if local_dir == "":
        cache_dir = None
        model_path = None
        local_dir_use_symlinks = True
        download_model = snapshot_download(repo_id=repo_id, cache_dir=cache_dir, local_dir=model_path,
                                           local_dir_use_symlinks=local_dir_use_symlinks,
                                           token=token,
                                           ignore_patterns=ignore_patterns,
                                           max_workers=4
                                           )
    else:
        path_dir = os.path.dirname(dir_path)
        path = os.path.dirname(path_dir)
        repo_list = repo_id.split('/')
        dir_list = local_dir.split('/')
        path = os.path.join(path, f"{dir_list[0]}", f"{dir_list[1]}", f"{repo_list[0]}", f"{repo_list[1]}")
        cache_dir = os.path.join(path, "cache")
        model_path = os.path.normpath(path)
        local_dir_use_symlinks = False

    if len(filename) > 0:
        get_model_path = hf_hub_download(repo_id=repo_id, filename=filename, cache_dir=cache_dir,
                                         local_dir=model_path, local_dir_use_symlinks=local_dir_use_symlinks,
                                         resume_download=True, token=token
                                         )
    else:
        download_model = snapshot_download(repo_id=repo_id, cache_dir=cache_dir, local_dir=model_path,
                                           local_dir_use_symlinks=local_dir_use_symlinks,
                                           token=token,
                                           ignore_patterns=ignore_patterns,
                                           max_workers=4
                                           )
