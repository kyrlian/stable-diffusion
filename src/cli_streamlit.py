# kyrlian 20231202

import torch
from diffusers import AutoPipelineForText2Image
import streamlit

streamlit.set_page_config(layout="wide")
streamlit.title("Stable diffusion")

def fix(n):
    return int(n/64)*64

# streamlit side pane
with streamlit.sidebar:
    streamlit.write("Image size")
    imgw = fix(streamlit.slider("Width",1,2048,1472))
    maxh = fix(1024000 / imgw)#limit height based on selected width
    imgh = fix(streamlit.slider("Height",1,maxh,704))
    nbimg = streamlit.slider("Nb images",1,4,2)
    nbsteps = streamlit.slider("Nb steps",1,30,2)
    seed = streamlit.number_input("Seed", 1, 1000000, 42)

# load pipeline
@streamlit.cache_resource
def load_pipeline():       
    # https://huggingface.co/stabilityai/sdxl-turbo 
    xlturbopipeline = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16")
    xlturbopipeline.to("cuda")
    return xlturbopipeline

pipe = load_pipeline()

def expand(metaprompt):
    promptlist=[""]
    for part in metaprompt.split("/"):
        newpromptlist=[]
        for variation in part.split("|"):
            for partialprompt in promptlist:
                newpromptlist.append(partialprompt+variation) # combine
        promptlist=newpromptlist.copy() #ensure its a copy
    return promptlist

def generate(p,i):
    generator= torch.Generator("cuda").manual_seed(seed+i)
    image = pipe(prompt=p, num_inference_steps=nbsteps, height=imgh, width=imgw, guidance_scale=0.0, generator=generator).images[0]
    streamlit.image(image, caption=p, use_column_width=False)

prompt = streamlit.text_input("Prompt", "A /cat|dog/ in a box")
for p in expand(prompt):
    for i in range(nbimg):
        generate(p,i)