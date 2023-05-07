
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

def getuserinput(stdscr, initialtext):
    #TODO add box, and status info at the bottom
    stdscr.addstr(0, 0, initialtext)
    box = Textbox(stdscr, insert_mode=True)
    def validate(ch):#handle key input
        # exit with the escape key or resize
        if ch in (27,  curses.KEY_RESIZE):
            return curses.ascii.BEL  # Control-G to exit
        # delete the character to the left of the cursor - not native with box.edit()
        elif ch in (curses.KEY_BACKSPACE, curses.ascii.DEL, curses.ascii.BS, 127):
            return curses.KEY_BACKSPACE
        return ch
    stdscr.refresh()
    box.edit(validate) # give input to user
    return box.gather().strip()#return box content

def main(screen, firstinput):
    if firstinput != "":
        user_input = getuserinput(screen, firstinput)
    while True:
        user_input = getuserinput(screen, firstinput).strip()
        if user_input in ["quit", "exit", "bye"]:
            break
        generate( user_input)

if __name__ == "__main__":
    args = sys.argv[1:]
    firstinput=">"
    if len(args) > 0: firstinput = args[0]
    curses.wrapper(main,firstinput) 
