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

<img src="docs/wechat.jpg" width="200" />


## License

The product is licensed under The Apache License 2.0, which allows for free commercial use. Please include the link to PaperChat and the licensing terms in your product description.


## Contribute

The project code is still quite raw. If anyone makes improvements to the code, we welcome contributions back to this project.