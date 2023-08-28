
import os
from dotenv import load_dotenv, find_dotenv
from langchain.llms import HuggingFaceHub

def expand(metaprompt):
    promptlist=[""]
    for part in metaprompt.split("/"):
        newpromptlist=[]
        for variation in part.split("|"):
            for partialprompt in promptlist:
                newpromptlist.append(partialprompt+variation) # combine
        promptlist=newpromptlist.copy() #ensure its a copy
    return promptlist

def progress(promptparts):
    promptlist=[]
    cp = ""
    for p in promptparts:
        cp += ("" if( cp=="") else " ") + p
        promptlist.append(cp)
    return promptlist


def generate_prompt_llm(basicprompt):
    load_dotenv(find_dotenv()) # take environment variables from .env.
    assert os.environ.get("HUGGINGFACEHUB_API_TOKEN") is not None
    # search LLMs for stable diffusion prompting:
    # https://huggingface.co/models?pipeline_tag=text-generation&search=stable%20diffusion%20prompt&sort=downloads
    model_id="Ar4ikov/gpt2-650k-stable-diffusion-prompt-generator"
    llm = HuggingFaceHub(repo_id=model_id, model_kwargs={"temperature": 0.1, "max_length": 64})
    enriched = basicprompt + llm(basicprompt)
    print(enriched)
    return enriched


aituts_style_list=["generic","anime","digital","fantasy","photography","cinematography","analogfilm","vaporwave","isometric","lowpoly","claymation","3dmodel","origami","line","pixel","texture"]
def generate_prompt_aituts(style, prompt):
    # https://aituts.com/sdxl-prompts/
    s = style.lower()
    if s == "generic": 
        positive = "breathtaking {prompt} . award-winning, professional, highly detailed"
        negative = "anime, cartoon, graphic, text, painting, crayon, graphite, abstract glitch, blurry"
    elif s == "anime":
        positive = "anime artwork {prompt} . anime style, key visual, vibrant, studio anime, highly detailed"
        negative = "photo, deformed, black and white, realism, disfigured, low contrast"
    elif s=="digital":
        positive = "concept art {prompt}. digital artwork, illustrative, painterly, matte painting, highly detailed"
        negative = "photo, photorealistic, realism, ugly"
    elif s=="fantasy":
        positive = "ethereal fantasy concept art of {prompt} . magnificent, celestial, ethereal, painterly, epic, majestic, magical, fantasy art, cover art, dreamy"
        negative = "photographic, realistic, realism, 35mm film, dslr, cropped, frame, text, deformed, glitch, noise, noisy, off-center, deformed, cross-eyed, closed eyes, bad anatomy, ugly, disfigured, sloppy, duplicate, mutated, black and white"
    elif s=="photography":
        positive = "cinematic photo {prompt} . 35mm photograph, film, bokeh, professional, 4k, highly detailed"
        negative = "drawing, painting, crayon, sketch, graphite, impressionist, noisy, blurry, soft, deformed, ugly"
    elif s=="cinematography":
        positive = "cinematic film still {prompt} . shallow depth of field, vignette, highly detailed, high budget Hollywood movie, bokeh, cinemascope, moody"
        negative = "anime, cartoon, graphic, text, painting, crayon, graphite, abstract, glitch, deformed, mutated, ugly, disfigured"
    elif s=="analogfilm":
        positive = "analog film photo {prompt} . faded film, desaturated, 35mm photo, grainy, vignette, vintage, Kodachrome, Lomography, stained, highly detailed, found footage"
        negative = "painting, drawing, illustration, glitch, deformed, mutated, cross-eyed, ugly, disfigured"
    elif s=="vaporwave":
        positive = "vaporwave synthwave style {prompt} . cyberpunk, neon, vibes, stunningly beautiful, crisp, detailed, sleek, ultramodern, high contrast, cinematic composition"
        negative = "illustration, painting, crayon, graphite, abstract, glitch, deformed, mutated, ugly, disfigured"
    elif s=="isometric":
        positive = "isometric style {prompt} . vibrant, beautiful, crisp, detailed, ultra detailed, intricate"
        negative = "deformed, mutated, ugly, disfigured, blur, blurry, noise, noisy, realistic, photographic"
    elif s=="lowpoly":
        positive = "low-poly style {prompt}. ambient occlusion, low-poly game art, polygon mesh, jagged, blocky, wireframe edges, centered composition"
        negative = "noisy, sloppy, messy, grainy, highly detailed, ultra textured, photo"
    elif s=="claymation":
        positive = "claymation style {prompt} . sculpture, clay art, centered composition, play-doh"
        negative = "sloppy, messy, grainy, highly detailed, ultra textured, photo, mutated"
    elif s=="3dmodel":
        positive = "professional 3d model {prompt} . octane render, highly detailed, volumetric, dramatic lighting"
        negative = "ugly, deformed, noisy, low poly, blurry, painting"
    elif s=="origami":
        positive = "origami style {prompt} . paper art, pleated paper, folded, origami art, pleats, cut and fold, centered composition"
        negative = "noisy, sloppy, messy, grainy, highly detailed, ultra textured, photo"
    elif s=="line":
        positive = "line art drawing {prompt} . professional, sleek, modern, minimalist, graphic, line art, vector graphics"
        negative = "anime, photorealistic, 35mm film, deformed, glitch, blurry, noisy, off-center, deformed, cross-eyed, closed eyes, bad anatomy, ugly, disfigured, mutated, realism, realistic, impressionism, expressionism, oil, acrylic"
    elif s=="pixel":
        positive = "pixel-art {prompt} . low-res, blocky, pixel art style, 16-bit graphics"
        negative = "sloppy, messy, blurry, noisy, highly detailed, ultra textured, photo, realistic"
    elif s=="texture":
        positive = "texture {prompt} top down close-up, video game"
        negative = "ugly, deformed, noisy, blurry, anime, photorealistic, 35mm film, glitch, off-center, deformed, impressionism, expressionism, oil, acrylic"
    else :
        positive = "{prompt}"
        negative = ""
    return positive.replace("{prompt}",prompt), negative