# PaperChat中文
PaperChat, provide quantized models to chat wtih arXiv papers, to run on cpu machines. Combining paper understanding and research on mutiple papers. Compiled llama.cpp already. 



本项目实现了基于CPU运行的论文内容对话
基于关键词查询机制，实现跨论文问答能力
无需下载论文，轻松构建自己的论文数据资源


## Requirements

1.download gguf model and put it under the master path: 

https://modelscope.cn/models/QuantFactory/Qwen2.5-7B-Instruct-GGUF/resolve/master/Qwen2.5-7B-Instruct.Q4_K_M.gguf


2.unzip llama_cpp.rar and put it under the master path:

```shell
cd llama_cpp

llama-server.exe -m ../Qwen2.5-7B-Instruct.Q4_K_M.gguf -c 2048
```


3.start another terminal:

```shell
cd chat_ui

python main.py
```