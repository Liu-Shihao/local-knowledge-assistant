
"""
https://huggingface.co/microsoft/Phi-3-mini-128k-instruct-onnx
int4 DML 的 ONNX 模型：Windows 上适用于 AMD、Intel 和 NVIDIA GPU 的 ONNX 模型，使用AWQ量化为 int4 。
适用于 fp16 CUDA 的 ONNX 模型：可用于为 NVIDIA GPU 运行的 ONNX 模型。
int4 CUDA 的 ONNX 模型：通过 RTN 使用 int4 量化的 NVIDIA GPU 的 ONNX 模型。
适用于 int4 CPU 和移动设备的 ONNX 模型：适用于您的 CPU 和移动设备的 ONNX 模型，通过 RTN 使用 int4 量化。上传了两个版本来平衡延迟与准确性。
"""