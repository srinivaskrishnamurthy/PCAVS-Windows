import torch
print(torch.cuda.is_available())  # True means PyTorch has CUDA support
print(torch.version.cuda)         # Shows the CUDA version PyTorch was built with