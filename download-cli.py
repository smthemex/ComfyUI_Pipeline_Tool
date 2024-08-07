# !/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
import os
import re
import sys

def has_single_dot(s):
    return s.count('.') == 1
def get_instance_path(path):
    instance_path = os.path.normpath(path)
    if sys.platform == 'win32':
        instance_path = instance_path.replace('\\', "/")
    return instance_path

os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
os.environ['_HF_DEFAULT_ENDPOINT'] = 'https://hf-mirror.com'

from huggingface_hub import snapshot_download, hf_hub_download
import huggingface_hub
hub_version=huggingface_hub.__version__
hub_version=int(hub_version.split(".")[1])

cur_path = os.path.dirname(os.path.abspath(__file__))
path_dir = os.path.dirname(cur_path)
comfy_path = os.path.dirname(path_dir)

models_path=os.path.join(comfy_path,"models")

parser = argparse.ArgumentParser(description="Download the huggingface or modelscope model.")
parser.add_argument("-r", "--repo_id", type=str, default="smthem/test-model")
parser.add_argument("-l", "--local_dir", type=str, default="diffusers")
parser.add_argument("-m", "--mode", type=str, default="hg")
parser.add_argument("-i", "--ignore_patterns", type=str, default="None")
parser.add_argument("-f", "--filename", type=str, default="")
parser.add_argument("-t", "--token", type=str, default="")

args = parser.parse_args()
repo_id = args.repo_id
download_mode=args.mode
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

if local_dir!="diffusers":
    diff_path = os.path.join(models_path, local_dir)
else:
    diff_path=os.path.join(models_path,"diffusers")

if download_mode=="ms":
    try:
        if filename and has_single_dot(filename):
            from modelscope.hub.file_download import model_file_download
            
            model_file_download(model_id=repo_id, file_path=filename,
                                local_dir=os.path.join(diff_path, repo_id, filename), )
        
        elif filename and not has_single_dot(filename):
            print("下载单体文件需要download_single_file填写的是文件名")
            raise "error"
        else:
            from modelscope.hub.snapshot_download import snapshot_download as snapshot_download_mo
            
            snapshot_download_mo(repo_id, local_dir=diff_path,
                                           ignore_file_pattern=ignore_patterns)
    except:
        raise "error"
        
else: #download_mode=="hg"
    if hub_version>=23:
        if not local_dir:
            cache_dir = None
            model_path = None
            download_model = snapshot_download(repo_id, ignore_patterns=ignore_patterns,max_workers=4)
        else:
            local_dir = os.path.join(diff_path, repo_id)
            cache_dir = os.path.join(local_dir, "cache")
            if filename and has_single_dot(filename):
                hf_hub_download(repo_id=repo_id, filename=filename,
                                cache_dir=cache_dir,token=token,
                                local_dir=local_dir, resume_download=True
                                )
            elif filename and not has_single_dot(filename):
                raise "下载单体文件需要download_single_file填写的是文件名"
            else:
                snapshot_download(repo_id, cache_dir=cache_dir, local_dir=local_dir,token=token,
                                  ignore_patterns=ignore_patterns, max_workers=4)
        
    else:
        if not local_dir:
            cache_dir = None
            model_path = None
            local_dir_use_symlinks = "auto"
            snapshot_download(repo_id, cache_dir=cache_dir, local_dir=model_path,
                                               local_dir_use_symlinks=local_dir_use_symlinks,
                                               token=token,
                                               ignore_patterns=ignore_patterns,
                                               max_workers=4
                                               )
        else:
            path = get_instance_path(os.path.join(diff_path, repo_id))
            cache_dir = os.path.join(path, "cache")
            local_dir = os.path.normpath(path)
            local_dir_use_symlinks = False
            if filename and has_single_dot(filename):
                hf_hub_download(repo_id, filename=filename, cache_dir=cache_dir,
                                local_dir=local_dir, local_dir_use_symlinks=local_dir_use_symlinks,
                                resume_download=True, token=token
                                )
            else:
                snapshot_download(repo_id, cache_dir=cache_dir, local_dir=local_dir,
                                  local_dir_use_symlinks=local_dir_use_symlinks,
                                  token=token,
                                  ignore_patterns=ignore_patterns,
                                  max_workers=4
                                  )
            
