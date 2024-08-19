# kyrlian 20231202

import streamlit
import torch
from diffusers import AutoencoderTiny, StableDiffusionPipeline
from streamdiffusion import StreamDiffusion
from streamdiffusion.image_utils import postprocess_image
from sdutils.utils_prompt import expand

# streamlit config
streamlit.set_page_config(layout="wide")
engine="stabilityai/sdxl-turbo"
streamlit.title(engine)

# streamlit side pane
with streamlit.sidebar:
    streamlit.write("Image size")
    defw, defh = 23*64, 11*64
    imgw = streamlit.slider("Width", 64, 2048, defw, 64) 
    maxh = int(1024*1024 / imgw)  # limit height based on selected width
    imgh = streamlit.slider("Height", 64, maxh, defh, 64)  
    nbimg = streamlit.slider("Nb images", 1, 4, 1)
    nbsteps = streamlit.slider("Nb steps", 1, 30, 1)
    seed = streamlit.number_input("Seed", 1, 1000000, 42)

# load pipeline
@streamlit.cache_resource
def init():
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
    return stream

stream = init()

prompt = streamlit.text_input("Prompt", "A /cat|dog/ in a box")
for p in expand(prompt):
    for i in range(nbimg):
        streamlit.text(f"Generating image {i+1}/{nbimg} for prompt '{p}', seed: {seed+i}")
        x_output = stream.txt2img()
        img = postprocess_image(x_output, output_type="pil")[0]
        streamlit.image(img, caption=p, use_column_width=False)


# Run with
# python -m streamlit run .\src\stream-diffusion-streamlit.py