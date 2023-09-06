import sys
from rich import pretty
pretty.install()

from utils_stablediffusion import simplePipeline
from utils_image import saveimage

pipe = simplePipeline()

def generate(input):
    image = pipe.generate(input)
    saveimage(image, input)
    image.show()
    
