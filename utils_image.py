import os, re, glob
from PIL import Image


def saveimage(image, prompt, seed="", postfix=""):
    cleanprompt = re.sub("( |,)", '-', prompt)[:20]
    fname = f"images/{cleanprompt}-{seed}-{postfix}.png"
    image.save(fname)
    print(f"Saved {fname}")
    return fname

#call with : generate_all("Sunset"), generatefn, **{'size':'1472x704'})
def generate_all(prompts, generate, **generate_kwargs):
    # print(f"generate_all:generate_kwargs:{generate_kwargs}")
    for p in prompts:
        print(f"Generating: {p}")
        image = generate(p, **generate_kwargs)
        try:
            saveimage(image, p)
        except Exception:
            pass
        # display(image)

def display_latest(directory):
    list_of_files = glob.glob(directory + "/*.png")
    latest_file = max(list_of_files, key=os.path.getctime)
    image = Image.open(latest_file)
    image.show()
    # display(image)
