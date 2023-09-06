
import sys
import curses
from curses.textpad import Textbox
from utils_stablediffusion import simplePipeline, img2imgPipeline

def cursesmain(stdscr: curses.window, userinput):
    curses.use_default_colors()
    screenwin = stdscr.derwin(0, 0)
    inputwin = screenwin.derwin(screenwin.getmaxyx()[0] - 2, screenwin.getmaxyx()[1] - 2, 1, 1)
    textbox = Textbox(inputwin, insert_mode=True)
    txt2img = simplePipeline()
    img2img = img2imgPipeline()

    def generate(prompt, nbimages=4, srcimg=None, seed=42):
        if srcimg is not None:
            print("img2imgpipeline")
            images = img2img.generate(prompt, srcimg, nbimages).images
        else:
            print("txt2imgpipeline")
            images = txt2img.generate(prompt, nbimages).images
        for idx, image in enumerate(images):
            fname = f"images/{prompt.replace(' ','-')}-{seed}-{idx+1}of{nbimages}.png"
            image.save(fname)
            image.show() # open outside
        return images

    def redraw(title, status=None):
        screenwin.clear()
        screenwin.border()
        screenwin.addstr(0, 2, title)  # title
        if status is not None:
            screenwin.addstr(screenwin.getmaxyx()[0] - 1, 2, status)
        screenwin.refresh()

    def validator(ch):  # handle key input
        if ch == 27:
            return curses.ascii.BEL  # Control-G to exit
        elif ch in (curses.KEY_BACKSPACE, curses.ascii.DEL, curses.ascii.BS, 127):
            return curses.KEY_BACKSPACE
        return ch

    def getuserinput(title, prompt, status):
        redraw(title, status)
        inputwin.addstr(0, 0, prompt)
        # give input to user and return box content
        userinput = textbox.edit(validator).strip()
        redraw(title, f"Userinput: [{userinput}]")
        return userinput

    # main loop
    inimage = None
    nbbatch = 4
    status = "..."
    doloop = True
    while doloop:
        if userinput != "":
            generateorderivate = "Generating"
            if inimage is not None:
                generateorderivate = "Derivating"
            redraw("Working...", f"{generateorderivate}: [{userinput}]")
            images = generate(userinput, nbbatch, inimage)
            # ask the user to choose one output to refine
            inimage = None
            gotchoice = False
            while not gotchoice:
                choice = getuserinput(
                    f"Choose image to keep (1-{nbbatch})", "1", status)
                if choice.isdigit() and int(choice) in list(range(1, nbbatch+1)):
                    inimage = images[int(choice)-1]
                    status = f"Deriving from image [{choice}]"
                    gotchoice = True
                elif choice.lower() in ["reset"]:
                    userinput = ""
                    status = "Reset"
                    gotchoice = True
                elif choice.lower() in ["quit", "exit", "bye"]:
                    doloop = False
                    gotchoice = True
                    status = "Quit"
                else:
                    status = f"Incorrect choice [{choice}]"
        if doloop:
            userinput = getuserinput(
            "Complete the prompt, type ESC to send, Ctrl-C to quit.", userinput, status)


if __name__ == "__main__":
    args = sys.argv[1:]
    curses.wrapper(cursesmain, args[0] if len(args) > 0 else "")
