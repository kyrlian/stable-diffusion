
import sys
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
import torch
import curses
from curses.textpad import Textbox

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

def cursesmain(stdscr, userinput):
    curses.use_default_colors()
    screenwin = stdscr.derwin(0, 0)
    screenwin.border()
    screenwin.addstr(
        0, 2, "Complete the prompt, type ESC to send, Ctrl-C to quit."
    )
    #screenwin.addstr(screenwin.getmaxyx()[0] - 1, 2, getinfo(llm))
    inputwin = screenwin.derwin(
        screenwin.getmaxyx()[0] - 2, screenwin.getmaxyx()[1] - 2, 1, 1
    )
    textbox = Textbox(inputwin, insert_mode=True)

    def validator(ch):  # handle key input
        if ch == 27:
            return curses.ascii.BEL  # Control-G to exit
        elif ch in (curses.KEY_BACKSPACE, curses.ascii.DEL, curses.ascii.BS, 127):
            return curses.KEY_BACKSPACE
        return ch

    def getuserinput(prompt):
        inputwin.addstr(0, 0, prompt)
        inputwin.refresh()
         # give input to user and return box content
        return textbox.edit(validator).strip() 

    screenwin.refresh()

    #loop
    while True:
        if userinput != "":
            generate(userinput)
        userinput = getuserinput(userinput)


if __name__ == "__main__":
    args = sys.argv[1:]
    firstinput=">"
    if len(args) > 0: firstinput = args[0]
    curses.wrapper(cursesmain,firstinput) 
