import re

def saveimage(image, prompt, seed="", postfix=""):
    cleanprompt = re.sub("( |,)", '-', prompt)[:20]
    fname = f"images/{cleanprompt}-{seed}-{postfix}.png"
    image.save(fname)
    print(f"Saved {fname}")
    return fname

def generate_all(prompts, generate, **generate_kwargs):
    # print(f"generate_all:generate_kwargs:{generate_kwargs}")
    for p in prompts:
        print(p)
        image = generate(p, **generate_kwargs)
        saveimage(image, p)
        # display(image)