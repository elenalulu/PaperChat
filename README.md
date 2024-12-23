[**🇨🇳中文**](https://github.com/shibing624/text2vec/blob/master/README_CN.md)


<div align="center">
  <a href="https://github.com/elenalulu/PaperChat">
    <img src="https://github.com/elenalulu/PaperChat/logo.png" height="150" alt="Logo">
  </a>
</div>

-----------------

# PaperChat
PaperChat, provide quantized models to chat wtih arXiv papers, to run on cpu machines. Combining paper understanding and research on mutiple papers. Compiled llama.cpp already. 



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