import time
import random
from fractions import Fraction
from gradio_client import Client

class fooocusClient:
    sizes = ["704×1408", "704×1344", "768×1344", "768×1280", "832×1216", "832×1152", "896×1152", "896×1088", "960×1088", "960×1024", "1024×1024", "1024×960", "1088×960", "1088×896", 
             "1152×896", "1152×832", "1216×832", "1280×768", "1344×768", "1344×704", "1408×704", "1472×704", "1536×640", "1600×640", "1664×576", "1728×576"]
    styles =["None", "cinematic-default", "sai-3d-model", "sai-analog film", "sai-anime", "sai-cinematic", "sai-comic book", "sai-craft clay", "sai-digital art", "sai-enhance", "sai-fantasy art", 
             "sai-isometric", "sai-line art", "sai-lowpoly", "sai-neonpunk", "sai-origami", "sai-photographic", "sai-pixel art", "sai-texture", 
             "ads-advertising", "ads-automotive", "ads-corporate", "ads-fashion editorial", "ads-food photography", "ads-luxury", "ads-real estate", "ads-retail", 
             "artstyle-abstract", "artstyle-abstract expressionism", "artstyle-art deco", "artstyle-art nouveau", "artstyle-constructivist", "artstyle-cubist", "artstyle-expressionist", "artstyle-graffiti", 
             "artstyle-hyperrealism", "artstyle-impressionist", "artstyle-pointillism", "artstyle-pop art", "artstyle-psychedelic", "artstyle-renaissance", "artstyle-steampunk", "artstyle-surrealist", 
             "artstyle-typography", "artstyle-watercolor", 
             "futuristic-biomechanical", "futuristic-biomechanical cyberpunk", "futuristic-cybernetic", "futuristic-cybernetic robot", "futuristic-cyberpunk cityscape", "futuristic-futuristic", 
             "futuristic-retro cyberpunk", "futuristic-retro futurism", "futuristic-sci-fi", "futuristic-vaporwave", 
             "game-bubble bobble", "game-cyberpunk game", "game-fighting game", "game-gta", "game-mario", "game-minecraft", "game-pokemon", "game-retro arcade", "game-retro game", "game-rpg fantasy game", 
             "game-strategy game", "game-streetfighter", "game-zelda", 
             "misc-architectural", "misc-disco", "misc-dreamscape", "misc-dystopian", "misc-fairy tale", "misc-gothic", "misc-grunge", "misc-horror", "misc-kawaii", "misc-lovecraftian", "misc-macabre", 
             "misc-manga", "misc-metropolis", "misc-minimalist", "misc-monochrome", "misc-nautical", "misc-space", "misc-stained glass", "misc-techwear fashion", "misc-tribal", "misc-zentangle", 
             "papercraft-collage", "papercraft-flat papercut", "papercraft-kirigami", "papercraft-paper mache", "papercraft-paper quilling", "papercraft-papercut collage", "papercraft-papercut shadow box", 
             "papercraft-stacked papercut", "papercraft-thick layered papercut", 
             "photo-alien", "photo-film noir", "photo-hdr", "photo-long exposure", "photo-neon noir", "photo-silhouette", "photo-tilt-shift"]
    styles_sai = ["sai-3d-model", "sai-analog film", "sai-anime", "sai-cinematic", "sai-comic book", "sai-craft clay", "sai-digital art", "sai-enhance", "sai-fantasy art", 
             "sai-isometric", "sai-line art", "sai-lowpoly", "sai-neonpunk", "sai-origami", "sai-photographic", "sai-pixel art", "sai-texture"]
    styles_ads = ["ads-advertising", "ads-automotive", "ads-corporate", "ads-fashion editorial", "ads-food photography", "ads-luxury", "ads-real estate", "ads-retail"]
    styles_art = ["artstyle-abstract", "artstyle-abstract expressionism", "artstyle-art deco", "artstyle-art nouveau", "artstyle-constructivist", "artstyle-cubist", "artstyle-expressionist", "artstyle-graffiti", 
             "artstyle-hyperrealism", "artstyle-impressionist", "artstyle-pointillism", "artstyle-pop art", "artstyle-psychedelic", "artstyle-renaissance", "artstyle-steampunk", "artstyle-surrealist", 
             "artstyle-typography", "artstyle-watercolor"]
    styles_futuristic = ["futuristic-biomechanical", "futuristic-biomechanical cyberpunk", "futuristic-cybernetic", "futuristic-cybernetic robot", "futuristic-cyberpunk cityscape", "futuristic-futuristic", 
             "futuristic-retro cyberpunk", "futuristic-retro futurism", "futuristic-sci-fi", "futuristic-vaporwave"]
    styles_games = ["game-bubble bobble", "game-cyberpunk game", "game-fighting game", "game-gta", "game-mario", "game-minecraft", "game-pokemon", "game-retro arcade", "game-retro game", "game-rpg fantasy game", 
             "game-strategy game", "game-streetfighter", "game-zelda" ]
    styles_misc = ["misc-architectural", "misc-disco", "misc-dreamscape", "misc-dystopian", "misc-fairy tale", "misc-gothic", "misc-grunge", "misc-horror", "misc-kawaii", "misc-lovecraftian", "misc-macabre", 
             "misc-manga", "misc-metropolis", "misc-minimalist", "misc-monochrome", "misc-nautical", "misc-space", "misc-stained glass", "misc-techwear fashion", "misc-tribal", "misc-zentangle" ]
    styles_paper = ["papercraft-collage", "papercraft-flat papercut", "papercraft-kirigami", "papercraft-paper mache", "papercraft-paper quilling", "papercraft-papercut collage", "papercraft-papercut shadow box", 
             "papercraft-stacked papercut", "papercraft-thick layered papercut" ]
    styles_photo = ["photo-alien", "photo-film noir", "photo-hdr", "photo-long exposure", "photo-neon noir", "photo-silhouette", "photo-tilt-shift"]
    performances = ["Speed", "Quality"]

    def __init__(self):
        self.client = Client("http://127.0.0.1:7860/") 
        self.size = self.correct_size("1024×1024")
        self.style = "cinematic-default"
        self.performance = "Speed" # Speed or Quality (speed is 30 iterations, 60 for quality)
        self.nbimages = 1
        self.seed = None
        self.sharpness = 0        
    
    def info(self):
        info=f"size: {self.size}, style: {self.style}, performance: {self.performance}, nbimages: {self.nbimages}, seed: {self.seed}, sharpness: {self.sharpness}"
        # print(info)
        return info
    
    def list_sizes():
        for s in fooocusClient.sizes:
            print(f"{s} : {fooocusClient.get_ratio(s)}", end= ', ')
        return fooocusClient.sizes
    
    def get_ratio(size):
        ratio = size.replace("×","/")
        frac = Fraction(ratio).limit_denominator(100)
        return str(frac)
    
    def lists_styles():
        print(fooocusClient.styles)
        return fooocusClient.styles
    
    def correct_size(self, size):
        return size.replace("x", "×")
    
    def check_size(self, size):
        xsize = self.correct_size(size)
        if xsize not in fooocusClient.sizes:
            print(f"Size {size} not supported")
            return False
        else:
            return True

    def set_size(self, size):
        xsize = self.correct_size(size)
        if self.check_size(xsize): self.size = xsize
        
    def check_style(self, style):
        if style not in fooocusClient.styles:
            print(f"Style {style} not supported")
            return False
        else:
            return True
    
    def set_style(self, style):
        if self.check_style(style):  self.style = style

    def check_performance(self, performance):
        if performance not in fooocusClient.performances:
            print(f"Performance {performance} not supported")
            return False
        else:
            return True

    def set_performance(self, performance):
        if self.check_performance(performance):  self.performance = performance


    def generate(self, prompt, negative_prompt="", style=None, size=None, performance=None, nbimages=None, seed=None, sharpness=None, debug=False):
        if isinstance(prompt, list):
            for p in prompt:
                self.generate(p, negative_prompt, style, size, performance, nbimages, seed, sharpness, debug)
            return

        style = style if style is not None and self.check_style(style) else self.style
        size = self.correct_size(size if size is not None and self.check_size(size) else self.size)
        performance = performance if performance is not None and self.check_performance(performance) else self.performance
        nbimages = nbimages or self.nbimages
        sharpness = sharpness or self.sharpness
        seed = seed or self.seed or random.randrange(1000)

        job = self.client.submit( #submit is non blocking
            prompt,				# Prompt - str
            negative_prompt,	# Negative promt - str
            style,				# Style - str
            performance,		# Speed or Quality - str
            size,		        # Size - str - (width × height)
            nbimages,			# Nb Images to generate - int
            seed,			    # Seed - int 6 - 
            sharpness,			# Sharpness - int | float
            "sd_xl_base_1.0_0.9vae.safetensors",	# Base Model - 		['sd_xl_base_1.0_0.9vae.safetensors', 'sd_xl_refiner_1.0_0.9vae.safetensors']
            "sd_xl_refiner_1.0_0.9vae.safetensors",	# Refiner - ['None', 'sd_xl_base_1.0_0.9vae.safetensors', 'sd_xl_refiner_1.0_0.9vae.safetensors']
            "None",	# LoRA 1 - ['None', 'sd_xl_offset_example-lora_1.0.safetensors']
            -2,		# LoRA 1 Weight - int | float (between -2 and 2)
            "None",	# LoRA 2 - ['None', 'sd_xl_offset_example-lora_1.0.safetensors']
            -2,		# LoRA 2 Weight - int | float (between -2 and 2)
            "None",	# LoRA 3 - ['None', 'sd_xl_offset_example-lora_1.0.safetensors']
            -2,		# LoRA 3 Weight - int | float (between -2 and 2)
            "None",	# LoRA 4 - ['None', 'sd_xl_offset_example-lora_1.0.safetensors']
            -2,		# LoRA 4 Weight - int | float (between -2 and 2)
            "None",	# LoRA 5 - ['None', 'sd_xl_offset_example-lora_1.0.safetensors']
            -2,		# LoRA 5 Weight - int | float (between -2 and 2)
            fn_index=4)
        if debug: print(job.status())
        while not job.done():
            time.sleep(1)#seconds
            if debug: print(job.status())
        res = job.status()
        return res

    #call with : generate_all(["Sunset","Sunrise"], **{'size':'1472x704'})
    def generate_all(self, prompts, **generate_kwargs):
        print(self.info())
        for p in prompts:
            print(f"Generating: {p}")
            self.generate(p, **generate_kwargs)