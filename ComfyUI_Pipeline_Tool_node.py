# !/usr/bin/env python
# -*- coding: UTF-8 -*-

import os

dir_path = os.path.dirname(os.path.abspath(__file__))


class Pipeline_Tool:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "repo_id": ("STRING", {"default": "ByteDance/Hyper-SD"}),
                "local_dir": ("STRING", {"default": "models/diffusers"}),
                "ignore_patterns": (["none", "big_files", "safetensors", "bin", "safetensors,bin",
                                     "pth", "safetensors,bin,pth", "model", "msgpack", "onnx_data", "onnx", ],),
                "max_workers": ("INT", {"default": 4, "min": 1, "max": 8, "step": 1, "display": "slider"}),
                "download_single_file": ("STRING", {"default": "None"}),
                "use_default_cache_dir": ("BOOLEAN", {"default": False},)
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("model_path",)
    FUNCTION = "pipeline_tool"
    CATEGORY = "Pipeline_Tool"

    def pipeline_tool(self, repo_id, local_dir,
                      ignore_patterns, max_workers, download_single_file, use_default_cache_dir):
        if use_default_cache_dir == True:
            cache_dir = None
            local_dir = None
            local_dir_use_symlinks = True
        else:
            local_dir_use_symlinks = False
            path_dir = os.path.dirname(dir_path)
            path = os.path.dirname(path_dir)
            repo_list = repo_id.split('/')
            dir_list = local_dir.split('/')
            path = os.path.join(path, f"{dir_list[0]}", f"{dir_list[1]}", f"{repo_list[0]}", f"{repo_list[1]}")
            cache_dir = os.path.join(path, "cache")
            local_dir = os.path.normpath(path)

        if ignore_patterns == "none":
            ignore_patterns = None
        elif ignore_patterns == "big_files":
            ignore_patterns = ["*.safetensors", "*.bin", "*.pth", "*.model", "*.msgpack", "*.onnx_data", "*.onnx",
                               "*.gguf", "*.xml"]
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

        s = len(download_single_file)
        if s > 0:
            os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
            from huggingface_hub import hf_hub_download
            model_path = hf_hub_download(repo_id=repo_id, filename=download_single_file, cache_dir=cache_dir,
                                         local_dir=local_dir,
                                         local_dir_use_symlinks=local_dir_use_symlinks, resume_download=True
                                         )
            return (model_path,)
        else:
            os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
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
