#!pyhon3

import sys
from utils_stablediffusion import simplePipeline as pipeline
from utils_image import saveimage

def main(firstinput):
    def generate(input):
        image = pipe.generate(input)
        saveimage(image, input)
        image.show()
    
    pipe = pipeline()
    if firstinput != "":
       generate(firstinput)
    while True:
        user_input = input(">").strip()
        if user_input in ["quit", "exit", "bye"]:
            break
        generate(user_input)

if __name__ == "__main__":
    args = sys.argv[1:]
    main(args[0] if len(args) > 0 else "" )