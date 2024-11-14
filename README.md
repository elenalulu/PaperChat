# PaperChat
PaperChat, provide quantized models to chat wtih arXiv papers, in order to run on cpu machines. Combining paper understanding and research on mutiple papers.


1.download gguf model from: 

https://modelscope.cn/models/QuantFactory/Qwen2.5-7B-Instruct-GGUF/resolve/master/Qwen2.5-7B-Instruct.Q4_K_M.gguf


2.#unzip llama_cpp.rar and put llama_cpp file under the master path:

cd llama_cpp

llama-server.exe -m ../Qwen2.5-7B-Instruct.Q4_K_M.gguf -c 2048



3.#start another terminal:

cd chat_ui

python main.py
