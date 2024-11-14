# PaperChat
PaperChat, provide quantized models to chat wtih arXiv papers, in order to run on cpu machines. Combining paper understanding and research on mutiple papers.


1.download gguf model from: 


2.start llama.cpp as:

#unzip llama_cpp.rar

cd llama.cpp

llama-server.exe -m ../Qwen2.5-7B-Instruct.Q4_K_M.gguf -c 2048



3.run chat ui:

#start another terminal

cd chat_ui

python main.py
