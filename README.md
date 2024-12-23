[**🇨🇳中文**](https://github.com/elenalulu/PaperChat/blob/master/README_CN.md)

# PaperChat
PaperChat, provide quantized models to chat wtih arXiv papers, to run on cpu machines. Combining paper understanding and research on mutiple papers. Compiled llama.cpp already. 


<div>
	<p align="center">
  <img alt="Animation Demo" src="https://github.com/elenalulu/PaperChat/blob/main/docs/logo.png" width="660" />
  </p>
</div>

-----------------

## Usage

- This project implements a paper content dialogue based on CPU operation.
- Based on a keyword query mechanism to perform cross-paper question and answer.
- You can build your own paper data resources without needing to download papers.


<div>
	<p align="center">
  <img alt="Animation Demo" src="https://github.com/elenalulu/PaperChat/blob/main/docs/ui.png" width="660" />
  </p>
</div>


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



## Contact




## License


授权协议为 [The Apache License 2.0](LICENSE)，可免费用做商业用途。请在产品说明中附加ChatPDF的链接和授权协议。


## Contribute
项目代码还很粗糙，如果大家对代码有所改进，欢迎提交回本项目。