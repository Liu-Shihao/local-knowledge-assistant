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

Ollama supports a list of models available on [ollama.com/library](https://ollama.com/library 'ollama model library')

Here are some example models that can be downloaded:

| Model              | Parameters | Size  | Download                       |
| ------------------ | ---------- | ----- | ------------------------------ |
| Llama 2            | 7B         | 3.8GB | `ollama run llama2`            |
| Mistral            | 7B         | 4.1GB | `ollama run mistral`           |
| Dolphin Phi        | 2.7B       | 1.6GB | `ollama run dolphin-phi`       |
| Phi-2              | 2.7B       | 1.7GB | `ollama run phi`               |
| Neural Chat        | 7B         | 4.1GB | `ollama run neural-chat`       |
| Starling           | 7B         | 4.1GB | `ollama run starling-lm`       |
| Code Llama         | 7B         | 3.8GB | `ollama run codellama`         |
| Llama 2 Uncensored | 7B         | 3.8GB | `ollama run llama2-uncensored` |
| Llama 2 13B        | 13B        | 7.3GB | `ollama run llama2:13b`        |
| Llama 2 70B        | 70B        | 39GB  | `ollama run llama2:70b`        |
| Orca Mini          | 3B         | 1.9GB | `ollama run orca-mini`         |
| Vicuna             | 7B         | 3.8GB | `ollama run vicuna`            |
| LLaVA              | 7B         | 4.5GB | `ollama run llava`             |
| Gemma              | 2B         | 1.4GB | `ollama run gemma:2b`          |
| Gemma              | 7B         | 4.8GB | `ollama run gemma:7b`          |

> Note: You should have at least 8 GB of RAM available to run the 7B models, 16 GB to run the 13B models, and 32 GB to run the 33B models.

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

国内魔塔Ollama Model地址：[https://modelscope.cn/models/liush99/ollama_models/files](https://modelscope.cn/models/liush99/ollama_models/files)