A simple download tool for using pipeline in comfyUI   

2024-08-03 更新
--加入魔搭支持，只要模型找得到，速度可以拉满。
安装方式，pip install modelscope

--既往更新
加入0.23.0以上版本的内容   
这个版本不再需要local_dir_use_symlinks 这个属性，也支持LLM模型的下载    。  


方便快速使用pipeline的模型下载节点，主要用于快速尝试新模型，毕竟别人做插件也要时间的。  

因为主要服务于大陆玩家，所以不用英文了。此节点主要是方便下载抱脸的模型，其实懂代码的基本上用不着。      

但是当我发现用pipeline测试模型足够多的时候，我的C盘快爆掉。  我后悔没有重设缓存区，所以就把抱脸的下载库做成comfy的节点。  

当local_dir为空时，默认开启symlinks.

插件直接内置镜像站，所以镜像站有的都能下载，需要token的请用cli方法，在命令行末尾加上--token "你申请到的token"     

注意：
-----
repo_id的格式是xxxxx/xxxxx，填错就用不了。   

用法一  
-----
推荐用新的cli方法，不用每次都要开启comfyUI再下载。详细使用方法，看cli_example（不开启comfyUI下载命令示例）.txt的内容。   

用法二
----

只需填写repo_id,一键下载该模型的所有文件到comfyUI的models/diffuses 文件目录下。  

此法类同于直接在抱脸直接下载，好处是文件结构给你理好了。
    
注意————因为有些模型库文件超级多，超级大，所以建议在ignore_patterns 选择big_files模式，先只下载小文件和结构，然后用“用法二”下载对应的文件。    
注意————ignore_patterns是不下载那些文件，所以要根据自己的需要来选。默认是none，也就是都下载。  
注意————使用“用法一”时，get_single_model必须是空的才能用。

 ![](https://github.com/smthemex/ComfyUI_Pipeline_Tool/blob/main/example1.png)

调用的方法，就是填写改模型的绝对路径。

用法三
----
下载单一的文件，只需要填写repo_id并在get_single_model填写你需要的模型名，就可以下载，输出文本为模型地址  

![](https://github.com/smthemex/ComfyUI_Pipeline_Tool/blob/main/example2.png)

