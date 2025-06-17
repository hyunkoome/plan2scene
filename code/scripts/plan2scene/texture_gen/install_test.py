import torch
import plan2scene.texture_gen.custom_ops.noise_kernel.noise_cuda as nc

# 더 편하게 쓰시려면 wrapper Function 또는 Python 모듈로 감싸두셨을 거예요.
# 여기서는 직접 호출 예시를 보여드립니다.

# 1) 입력 텐서와 난수 시드 생성
batch_size, dim = 1024, 2
position = torch.randn(batch_size, dim, device='cuda', dtype=torch.float32)
seed     = torch.randint(0, 10000, (batch_size,), device='cuda', dtype=torch.float32)

# 2) forward
nearest_noise, bilinear_noise = nc.forward(position, seed)

print("nearest_noise:", nearest_noise.shape)    # -> torch.Size([batch_size])
print("bilinear_noise:", bilinear_noise.shape)  # -> torch.Size([batch_size])

# 3) backward (autograd 없이 직접 호출)
d_position = torch.randn_like(position)
d_output_nearest = torch.randn(batch_size, device='cuda')
d_output_bilinear = torch.randn(batch_size, device='cuda')

# 만약 backward가 stack된 두 출력에 대해 한 번에 처리하도록 되어 있다면,
# d_outputs = torch.stack([d_output_nearest, d_output_bilinear], dim=0)
# d_pos_grad = noise_cuda_backward(position, seed, d_outputs)

# 직접 분리 호출 예시:
d_position_grad = nc.backward(position, seed)

print("d_position_grad:", d_position_grad.shape)  # -> torch.Size([batch_size, dim])
