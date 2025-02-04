import torch
from diffusers import AutoencoderTiny, StableDiffusionPipeline

from streamdiffusion import StreamDiffusion
from streamdiffusion.image_utils import postprocess_image

# You can load any models using diffuser's StableDiffusionPipeline
#model = "KBlueLeaf/kohaku-v2.1"
model = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model).to(
    device=torch.device("cuda"),
    dtype=torch.float16,
)

# Wrap the pipeline in StreamDiffusion
# Requires more long steps (len(t_index_list)) in text2image
# You recommend to use cfg_type="none" when text2image
stream = StreamDiffusion(
    pipe,
    t_index_list=[0, 16, 32, 45],
    torch_dtype=torch.float16,
    cfg_type="none",
)

# If the loaded model is not LCM, merge LCM
stream.load_lcm_lora()
stream.fuse_lora()
# Use Tiny VAE for further acceleration
stream.vae = AutoencoderTiny.from_pretrained("madebyollin/taesd").to(device=pipe.device, dtype=pipe.dtype)
# Enable acceleration
pipe.enable_xformers_memory_efficient_attention()
# Faster generation
#from streamdiffusion.acceleration.tensorrt import accelerate_with_tensorrt
#stream = accelerate_with_tensorrt(
#    stream, "engines", max_batch_size=2,
#)


prompt = "Cat"
# Prepare the stream
stream.prepare(prompt)

# Warmup >= len(t_index_list) x frame_buffer_size
for _ in range(4):
    stream()

# Run the stream infinitely
while True:
    x_output = stream.txt2img()
    postprocess_image(x_output, output_type="pil")[0].show()
    input_response = input("Press Enter to continue or type 'stop' to exit: ")
    if input_response == "stop":
        break