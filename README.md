# 本地RAG问答系统

解析用户输入：
Web URL：html、git、jira、
文件：PDF、TXT文件
Image图像

- 问答机器人🤖
- 代码理解
- 图片识别
- 图片搜索🔍

# Setup

## Ollama
官网：https://ollama.com/

Windows系统查看ollama 帮助命令
```shell
ollama.exe serve --help
```

模型下载到本地默认目录：
- On Mac, the models will be download to `~/.ollama/models`
- On Linux (or WSL), the models will be stored at /usr/share/ollama/.ollama/models



### 常用命令
```shell
#Pull a model
ollama pull llama2
#Remove a model
ollama rm llama2
#Copy a model
ollama cp llama2 my-llama2
#List models on your computer
ollama list
#查看模型信息
ollama show --modelfile mistral
```

### 如何导入Model
Ollama supports importing GGUF models in the Modelfile:
```shell
#1.Create a file named Modelfile, with a FROM instruction with the local filepath to the model you want to import.
FROM ./vicuna-33b.Q4_0.gguf
#2.Create the model in Ollama
ollama create example -f Modelfile
#3.Run the model
ollama run example
```

###  REST API
Ollama has a REST API for running and managing models.

Generate a response

```shell
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt":"Why is the sky blue?"
}'
```
Chat with a model
```shell
curl http://localhost:11434/api/chat -d '{
  "model": "mistral",
  "messages": [
    { "role": "user", "content": "why is the sky blue?" }
  ]
}'
```