import sys
from rich import pretty
pretty.install()

# from sdutils.utils_stablediffusion import simplePipeline as pipeline
from sdutils.utils_stablediffusion import sdxlturboPipeline as pipeline

from sdutils.utils_image import saveimage

pipe = pipeline()

def generate(input):
    image = pipe.generate(input)
    saveimage(image, input)
    image.show()
    
g=generate

pretty.pprint('use generate("prompt") or g("prompt") to generate an image, exit() to quit')
