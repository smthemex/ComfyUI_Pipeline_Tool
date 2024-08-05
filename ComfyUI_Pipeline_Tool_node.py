# !/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import re
import sys
import folder_paths
models_path = folder_paths.models_dir
base_path = folder_paths.base_path
def get_instance_path(path):
    instance_path = os.path.normpath(path)
    if sys.platform == 'win32':
        instance_path = instance_path.replace('\\', "/")
    return instance_path

def has_single_dot(s):
    return s.count('.') == 1

class Pipeline_Tool:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "repo_id": ("STRING", {"default": "ByteDance/Hyper-SD"}),
                "local_dir": ("STRING", {"default": "diffusers"}),
                "ignore_patterns": (["none", "big_files", "safetensors", "bin", "safetensors,bin",
                                     "pth", "safetensors,bin,pth", "model", "msgpack", "onnx_data", "onnx", ],),
                "max_workers": ("INT", {"default": 4, "min": 1, "max": 8, "step": 1, "display": "slider"}),
                "download_single_file": ("STRING", {"default": ""}),
                "huggingface_default_cache": ("BOOLEAN", {"default": False},),
                "use_modelscope": ("BOOLEAN", {"default": False},),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("model_path",)
    FUNCTION = "pipeline_tool"
    CATEGORY = "Pipeline_Tool"

    def pipeline_tool(self, repo_id, local_dir,ignore_patterns, max_workers, download_single_file, huggingface_default_cache,use_modelscope):
        if ignore_patterns == "none":
            ignore_patterns = None
        elif ignore_patterns == "big_files":
            ignore_patterns = ["*.safetensors", "*.bin", "*.pth", "*.model", "*.msgpack", "*.onnx_data", "*.onnx",
                               "*.gguf","*.ckpt", "*.xml"]
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
        else:
            ignore_patterns = ["*.onnx"]
        
        if local_dir != "diffusers":
            diff_path = os.path.join(models_path, local_dir)
        else:
            diff_path = os.path.join(models_path, "diffusers")
        
        if use_modelscope: #魔塔下载
            if download_single_file and has_single_dot(download_single_file):
                from modelscope.hub.file_download import model_file_download
                model_path = model_file_download(model_id=repo_id,
                                                 file_path=download_single_file,
                                                 local_dir=os.path.join(diff_path, repo_id, download_single_file),
                                                 )
                return (model_path,)
            elif download_single_file and not has_single_dot(download_single_file):
                raise "下载单体文件需要download_single_file填写的是文件名"
            else:
                from modelscope.hub.snapshot_download import snapshot_download as snapshot_download_mo
                model_path = snapshot_download_mo(repo_id, local_dir=os.path.join(diff_path, repo_id),
                                               ignore_file_pattern=ignore_patterns)
                return (model_path,)
        else:  #hub 下载
            import huggingface_hub
            hub_version = huggingface_hub.__version__
            hub_version = int(hub_version.split(".")[1])
            
            
            if hub_version >=23:
                if huggingface_default_cache == True:
                    os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
                    os.environ['_HF_DEFAULT_ENDPOINT'] = 'https://hf-mirror.com'
                    from huggingface_hub import snapshot_download
                    model_path = snapshot_download(repo_id=repo_id,  ignore_patterns=ignore_patterns,max_workers=max_workers)

                    return (model_path,)
                else:
                    path = get_instance_path(os.path.join(diff_path, repo_id))
                    cache_dir = os.path.join(path, "cache")
                    local_dir = os.path.normpath(path)
                    if download_single_file and has_single_dot(download_single_file):
                        os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
                        os.environ['_HF_DEFAULT_ENDPOINT'] = 'https://hf-mirror.com'
                        from huggingface_hub import hf_hub_download
                        model_path = hf_hub_download(repo_id=repo_id, filename=download_single_file,
                                                     cache_dir=cache_dir,
                                                     local_dir=local_dir,
                                                     resume_download=True
                                                     )

                        return (model_path,)
                    elif download_single_file and not has_single_dot(download_single_file):
                        raise "下载单体文件需要download_single_file填写的是文件名"
                    else:
                        os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
                        os.environ['_HF_DEFAULT_ENDPOINT'] = 'https://hf-mirror.com'
                        from huggingface_hub import snapshot_download
                        model_path = snapshot_download(repo_id=repo_id, cache_dir=cache_dir, local_dir=local_dir,
                                                       ignore_patterns=ignore_patterns,
                                                       max_workers=max_workers
                                                       )
                        return (model_path,)
                
            else:
                if huggingface_default_cache == True:
                    os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
                    os.environ['_HF_DEFAULT_ENDPOINT'] = 'https://hf-mirror.com'
                    from huggingface_hub import snapshot_download
                    cache_dir = None
                    model_path = None
                    local_dir_use_symlinks = True
                    model_path = snapshot_download(repo_id=repo_id, cache_dir=cache_dir, local_dir=model_path,
                                                       max_workers=max_workers, ignore_patterns=ignore_patterns,
                                                       local_dir_use_symlinks=local_dir_use_symlinks,
                                                       )
                    return (model_path,)
                else:
                    local_dir_use_symlinks = False
                    path = get_instance_path(os.path.join(diff_path, repo_id))
                    cache_dir = os.path.join(path, "cache")
                    local_dir = os.path.normpath(path)
                    if download_single_file and has_single_dot(download_single_file):
                        os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
                        os.environ['_HF_DEFAULT_ENDPOINT'] = 'https://hf-mirror.com'
                        from huggingface_hub import hf_hub_download
                        model_path = hf_hub_download(repo_id=repo_id, filename=download_single_file,
                                                     cache_dir=cache_dir,
                                                     local_dir=local_dir,
                                                     local_dir_use_symlinks=local_dir_use_symlinks, resume_download=True
                                                     )
                        return (model_path,)
                    elif download_single_file and not has_single_dot(download_single_file):
                        raise "下载单体文件需要download_single_file填写的是文件名"
                    else:
                        os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
                        os.environ['_HF_DEFAULT_ENDPOINT'] = 'https://hf-mirror.com'
                        from huggingface_hub import snapshot_download
                        model_path = snapshot_download(repo_id=repo_id, cache_dir=cache_dir, local_dir=local_dir,
                                                       local_dir_use_symlinks=local_dir_use_symlinks,
                                                       ignore_patterns=ignore_patterns,
                                                       max_workers=max_workers
                                                       )
                        return (model_path,)
            
NODE_CLASS_MAPPINGS = {
    "Pipeline_Tool": Pipeline_Tool
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Pipeline_Tool": "Pipeline_Tool"
}
