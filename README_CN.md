# PaperChat
PaperChat, 提供了人人可用的arXiv论文对话机器人，只需要CPU即可运行。支持对论文的关键词理解和对多篇论文的深度挖掘。并且项目提供了已经编译好的llama.cpp，直接解压缩可用。
<br>

<div>
	<p align="center">
  <img alt="Animation Demo" src="https://github.com/elenalulu/PaperChat/blob/main/docs/logo.png" width="660" />
  </p>
</div>

-----------------
<br>

## 特点

- 本项目基于CPU运算实现了论文内容的对话功能
- 通过关键词查询机制来执行跨论文的问答操作
- 您可以构建自己的论文数据资源，无需下载论文


<div>
	<p align="center">
  <img alt="Animation Demo" src="https://github.com/elenalulu/PaperChat/blob/main/docs/ui.png" width="660" />
  </p>
</div>
<br>

## 安装要求

1.下载gguf模型，放在主路径下: 

https://modelscope.cn/models/QuantFactory/Qwen2.5-7B-Instruct-GGUF/resolve/master/Qwen2.5-7B-Instruct.Q4_K_M.gguf

<br>
2.解压缩llama_cpp.rar，放在主路径下；并且打开一个Anaconda Prompt，运行: 

```shell
cd llama_cpp

llama-server.exe -m ../Qwen2.5-7B-Instruct.Q4_K_M.gguf -c 2048
```

<br>
3.另外打开一个Anaconda Prompt:

```shell
cd chat_ui

python main.py
```

<br>

## 联系方式

<img src="docs/wechat.jpg" width="200" />
扫码进群，如遇过期请等更新
<br>

## License

授权协议为 [The Apache License 2.0](LICENSE)，可免费用做商业用途。请在产品说明中附加text2vec的链接和授权协议。

<br>
## Contribute

项目代码还很粗糙，如果大家对代码有所改进，欢迎提交回本项目