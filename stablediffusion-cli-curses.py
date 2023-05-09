
import sys
from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline, DPMSolverMultistepScheduler
import torch
import curses
from curses.textpad import Textbox

def inittxt2imgpipeline(model_id):
    # Use the DPMSolverMultistepScheduler (DPM-Solver++) scheduler here instead
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    pipe = pipe.to("cuda")
    return pipe

def initimg2imgpipeline(model_id):
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")
    return pipe

txt2imgpipeline=inittxt2imgpipeline("stabilityai/stable-diffusion-2-1")
img2imgpipeline = initimg2imgpipeline("runwayml/stable-diffusion-v1-5")

def generate(prompt,nbimages=4,srcimg=None,seed=42):
    generator = torch.Generator("cuda").manual_seed(seed)
    #TODO add negative_prompt
    if srcimg is not None:
        images = img2imgpipeline(prompt, image=srcimg, strength=0.75, guidance_scale=7.5, num_images_per_prompt=nbimages, generator=generator).images
    else:
        images = txt2imgpipeline(prompt, num_images_per_prompt=nbimages, generator=generator).images
    for idx, image in enumerate(images):
        fname = f"images/{prompt.replace(' ','-')}-{seed}-{idx}of{nbimages}.png"
        image.save(fname)
        #display(image) # open inline - for notebooks
        image.show() # open outside
    return images

def cursesmain(stdscr, userinput):
    curses.use_default_colors()
    screenwin = stdscr.derwin(0, 0)
    screenwin.border()
    inputwin = screenwin.derwin(screenwin.getmaxyx()[0] - 2, screenwin.getmaxyx()[1] - 2, 1, 1)
    textbox = Textbox(inputwin, insert_mode=True)
    screenwin.refresh()

    def settitle(txt):
        screenwin.addstr(0, 2, txt)
        screenwin.refresh()

    def setstatus(txt):
        screenwin.addstr(screenwin.getmaxyx()[0] - 1, 2, txt)
        screenwin.refresh()

    def validator(ch):  # handle key input
        if ch == 27:
            return curses.ascii.BEL  # Control-G to exit
        elif ch in (curses.KEY_BACKSPACE, curses.ascii.DEL, curses.ascii.BS, 127):
            return curses.KEY_BACKSPACE
        return ch

    def getuserinput(instruction, prompt):
        settitle(instruction)
        inputwin.addstr(0, 0, prompt)
        inputwin.refresh()
         # give input to user and return box content
        return textbox.edit(validator).strip() 

    #loop
    inimage = None
    nbbatch=4
    while True:
        if userinput != "":
            images = generate(userinput,nbbatch,inimage)
            #ask the user to choose one output to refine
            inimage = None
            choice = getuserinput(f"Choose image to keep (1-{nbbatch})","")
            if choice in list(range(1,nbbatch+1)):
                inimage = images[choice-1]
                setstatus(f"Deriving from image {choice}")
            elif choice.lower() in ["reset"]:
                userinput=""
                setstatus("Reset")
            elif choice.lower() in ["quit", "exit", "bye"]:
                break
        userinput = getuserinput("Complete the prompt, type ESC to send, Ctrl-C to quit.",userinput)


if __name__ == "__main__":
    args = sys.argv[1:]
    firstinput=""
    if len(args) > 0: firstinput = args[0]
    curses.wrapper(cursesmain,firstinput) 
