# !/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
import os
import re
import sys


def has_single_slash(s):
    return bool(re.match(r'^/.$', s))

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

cur_path = os.path.dirname(os.path.abspath(__file__))
path_dir = os.path.dirname(cur_path)
comfy_path = os.path.dirname(path_dir)

models_path=os.path.join(comfy_path,"models")
diff_path=os.path.join(models_path,"diffusers")

parser = argparse.ArgumentParser(description="Download the huggingface or modelscope model.")

parser.add_argument("-r", "--repo_id", type=str, default="smthem/test-model")
parser.add_argument("-l", "--local_dir", type=str, default="diffusers")
parser.add_argument("-m", "--mode", type=str, default="modelscope")
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


if download_mode=="modelscope":
    try:
        if filename and has_single_dot(filename):
            from modelscope.hub.file_download import model_file_download
            
            model_file_download(model_id=repo_id, file_path=filename,
                                cache_dir=os.path.join(diff_path, repo_id, filename), )
        
        elif filename and not has_single_dot(filename):
            print("下载单体文件需要download_single_file填写的是文件名")
            raise "error"
        else:
            from modelscope.hub.snapshot_download import snapshot_download
            
            model_path = snapshot_download(repo_id, cache_dir=os.path.join(diff_path, repo_id),
                                           ignore_file_pattern=ignore_patterns)
    except:
        print("改成hugging下载")
        try:
            if not local_dir:
                cache_dir = None
                model_path = None
                download_model = snapshot_download(repo_id=repo_id, ignore_patterns=ignore_patterns, max_workers=4)
            else:
                if local_dir and has_single_slash(repo_id):
                    if local_dir == "diffusers":
                        path = get_instance_path(os.path.join(diff_path, repo_id))
                    else:
                        path = get_instance_path(os.path.join(models_path, local_dir, repo_id))
                else:
                    if has_single_slash(repo_id) and not local_dir:
                        path = get_instance_path(os.path.join(diff_path, repo_id))
                    else:
                        raise "repo_id 需要填写为正确的XXX/XXX格式 "
                cache_dir = os.path.join(path, "cache")
                local_dir = os.path.normpath(path)
            if filename and has_single_dot(filename):
                hf_hub_download(repo_id=repo_id, filename=filename,
                                cache_dir=cache_dir,
                                local_dir=local_dir, resume_download=True
                                )
            elif filename and not has_single_dot(filename):
                raise "下载单体文件需要download_single_file填写的是文件名"
            else:
                snapshot_download(repo_id=repo_id, cache_dir=cache_dir, local_dir=local_dir,
                                  ignore_patterns=ignore_patterns, max_workers=4
                                  )
        except:
            try:
                if not local_dir:
                    cache_dir = None
                    model_path = None
                    local_dir_use_symlinks = True
                    snapshot_download(repo_id=repo_id, cache_dir=cache_dir, local_dir=model_path,
                                      local_dir_use_symlinks=local_dir_use_symlinks,
                                      token=token,
                                      ignore_patterns=ignore_patterns,
                                      max_workers=4
                                      )
                else:
                    if local_dir and has_single_slash(repo_id):
                        if local_dir == "diffusers":
                            path = get_instance_path(os.path.join(diff_path, repo_id))
                        else:
                            path = get_instance_path(os.path.join(models_path, local_dir, repo_id))
                    else:
                        if has_single_slash(repo_id) and not local_dir:
                            path = get_instance_path(os.path.join(diff_path, repo_id))
                        else:
                            raise "repo_id 需要填写为正确的XXX/XXX格式 "
                    cache_dir = os.path.join(path, "cache")
                    local_dir = os.path.normpath(path)
                    local_dir_use_symlinks = False
                
                if filename and has_single_dot(filename):
                    hf_hub_download(repo_id=repo_id, filename=filename, cache_dir=cache_dir,
                                    local_dir=local_dir, local_dir_use_symlinks=local_dir_use_symlinks,
                                    resume_download=True, token=token
                                    )
                else:
                    snapshot_download(repo_id=repo_id, cache_dir=cache_dir, local_dir=local_dir,
                                      local_dir_use_symlinks=local_dir_use_symlinks,
                                      token=token,
                                      ignore_patterns=ignore_patterns,
                                      max_workers=4
                                      )
            except:
                print("网络不通？")
            
else:
    try:
        if not local_dir:
            cache_dir = None
            model_path = None
            download_model = snapshot_download(repo_id=repo_id, ignore_patterns=ignore_patterns,max_workers=4)
        else:
            if local_dir and has_single_slash(repo_id):
                if local_dir == "diffusers":
                    path = get_instance_path(os.path.join(diff_path, repo_id))
                else:
                    path = get_instance_path(os.path.join(models_path, local_dir, repo_id))
            else:
                if has_single_slash(repo_id) and not local_dir:
                    path = get_instance_path(os.path.join(diff_path, repo_id))
                else:
                    raise "repo_id 需要填写为正确的XXX/XXX格式 "
            cache_dir = os.path.join(path, "cache")
            local_dir = os.path.normpath(path)
        if filename and has_single_dot(filename):
            hf_hub_download(repo_id=repo_id, filename=filename,
                                         cache_dir=cache_dir,
                                         local_dir=local_dir,resume_download=True
                                         )
        elif filename and not has_single_dot(filename):
            raise "下载单体文件需要download_single_file填写的是文件名"
        else:
            snapshot_download(repo_id=repo_id, cache_dir=cache_dir, local_dir=local_dir,
                                           ignore_patterns=ignore_patterns,max_workers=4
                                           )
    except:
        try:
            if not local_dir:
                cache_dir = None
                model_path = None
                local_dir_use_symlinks = True
                snapshot_download(repo_id=repo_id, cache_dir=cache_dir, local_dir=model_path,
                                                   local_dir_use_symlinks=local_dir_use_symlinks,
                                                   token=token,
                                                   ignore_patterns=ignore_patterns,
                                                   max_workers=4
                                                   )
            else:
                if local_dir and has_single_slash(repo_id):
                    if local_dir == "diffusers":
                        path = get_instance_path(os.path.join(diff_path, repo_id))
                    else:
                        path = get_instance_path(os.path.join(models_path, local_dir, repo_id))
                else:
                    if has_single_slash(repo_id) and not local_dir:
                        path = get_instance_path(os.path.join(diff_path, repo_id))
                    else:
                        raise "repo_id 需要填写为正确的XXX/XXX格式 "
                cache_dir = os.path.join(path, "cache")
                local_dir = os.path.normpath(path)
                local_dir_use_symlinks = False
            
            if filename and has_single_dot(filename):
                hf_hub_download(repo_id=repo_id, filename=filename, cache_dir=cache_dir,
                                                 local_dir=local_dir, local_dir_use_symlinks=local_dir_use_symlinks,
                                                 resume_download=True, token=token
                                                 )
            else:
                snapshot_download(repo_id=repo_id, cache_dir=cache_dir, local_dir=local_dir,
                                                   local_dir_use_symlinks=local_dir_use_symlinks,
                                                   token=token,
                                                   ignore_patterns=ignore_patterns,
                                                   max_workers=4
                                                   )
        except:
            print("网络不通？")
