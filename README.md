[**🇨🇳中文**](https://github.com/elenalulu/PaperChat/blob/master/README_CN.md)


<div align="center">
	<a>
  <img alt="Logo" src="https://github.com/elenalulu/PaperChat/blob/main/docs/logo.png" width="860" />
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