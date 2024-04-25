import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
"""
请注意，默认情况下，Phi-3-mini 模型使用闪存注意力，这需要某些类型的 GPU 硬件才能运行。我们在以下 GPU 类型上进行了测试：

英伟达 A100
英伟达 A6000
英伟达 H100
如果您想在以下平台上运行模型：

NVIDIA V100 或更早一代 GPU：使用 attn_implementation="eager" 调用 AutoModelForCausalLM.from_pretrained()
GPU、CPU 和移动设备上的优化推理：使用ONNX模型128K
"""
torch.random.manual_seed(0)

phi_3_mini = model_path = "/Users/liushihao/Downloads/model/microsoft/Phi-3-mini-128k-instruct"
phi_3_mini_onnx = model_path = "/Users/liushihao/Downloads/model/microsoft/Phi-3-mini-128k-instruct-onnx/cpu_and_mobile/cpu-int4-rtn-block-32"
model = AutoModelForCausalLM.from_pretrained(
    pretrained_model_name_or_path=phi_3_mini_onnx,
    # device_map="cuda",
    torch_dtype="auto",
    trust_remote_code=True,
)
tokenizer = AutoTokenizer.from_pretrained(phi_3_mini_onnx)

messages = [
    {"role": "system", "content": "You are a helpful digital assistant. Please provide safe, ethical and accurate information to the user."},
    {"role": "user", "content": "Can you provide ways to eat combinations of bananas and dragonfruits?"},
    {"role": "assistant", "content": "Sure! Here are some ways to eat bananas and dragonfruits together: 1. Banana and dragonfruit smoothie: Blend bananas and dragonfruits together with some milk and honey. 2. Banana and dragonfruit salad: Mix sliced bananas and dragonfruits together with some lemon juice and honey."},
    {"role": "user", "content": "What about solving an 2x + 3 = 7 equation?"},
]

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
)

generation_args = {
    "max_new_tokens": 500,
    "return_full_text": False,
    "temperature": 0.0,
    "do_sample": False,
}

output = pipe(messages, **generation_args)
print(output[0]['generated_text'])
