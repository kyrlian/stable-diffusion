# kyrlian 20231202

import streamlit
import torch
from diffusers import AutoPipelineForText2Image
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
def load_pipeline():
    # https://huggingface.co/stabilityai/sdxl-turbo
    xlturbopipeline = AutoPipelineForText2Image.from_pretrained(
        engine, torch_dtype=torch.float16, variant="fp16"
    )
    xlturbopipeline.to("cuda")
    return xlturbopipeline


pipe = load_pipeline()

prompt = streamlit.text_input("Prompt", "A /cat|dog/ in a box")
for p in expand(prompt):
    for i in range(nbimg):
        streamlit.text(f"Generating image {i+1}/{nbimg} for prompt '{p}', seed: {seed+i}")
        generator = torch.Generator("cuda").manual_seed(seed + i)
        img = pipe(
            prompt=p,
            guidance_scale=0.0,
            generator=generator,
            num_inference_steps=nbsteps,
            width=imgw,
            height=imgh,
        ).images[0]
        streamlit.image(img, caption=p, use_column_width=False)

# Run with
# python -m streamlit run .\src\sdxlturbo_streamlit.py