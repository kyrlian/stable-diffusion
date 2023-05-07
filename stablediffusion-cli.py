import sys
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
import torch

def initdiffusionpipeline(model_id):
    # Use the DPMSolverMultistepScheduler (DPM-Solver++) scheduler here instead
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    pipe = pipe.to("cuda")
    return pipe

diffusionpipeline=initdiffusionpipeline("stabilityai/stable-diffusion-2-1")

def generate(prompt,seed=42):
    generator = torch.Generator("cuda").manual_seed(seed)
    image = diffusionpipeline(prompt,generator=generator).images[0]
    fname = f"images/{prompt.replace(' ','-')}-{seed}.png"
    image.save(fname)
    #display(image) # open inline - for notebooks
    image.show() # open outside
    return image

def main(firstinput):
    if firstinput != "":
        res = generate(firstinput)
    while True:
        user_input = input(">").strip()
        if user_input in ["quit", "exit", "bye"]:
            break
        res = generate( user_input)

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) > 0:
        main(args[0])
    else:
        main("")
