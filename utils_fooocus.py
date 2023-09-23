import time
import random
from fractions import Fraction
from gradio_client import Client

class fooocusClient:
    sizes = ["704×1408", "704×1344", "768×1344", "768×1280", "832×1216", "832×1152", "896×1152", "896×1088", "960×1088", "960×1024", "1024×1024", "1024×960", "1088×960", "1088×896", 
             "1152×896", "1152×832", "1216×832", "1280×768", "1344×768", "1344×704", "1408×704", "1472×704", "1536×640", "1600×640", "1664×576", "1728×576"]
    # Fooocus V2 is not really a style, but triggers prompt extension
    styles = ["Fooocus V2", "Default (Slightly Cinematic)", 
            "SAI 3D Model", "SAI Analog Film", "SAI Anime", "SAI Cinematic", "SAI Comic Book", "SAI Craft Clay", "SAI Digital Art", "SAI Enhance", "SAI Fantasy Art", "SAI Isometric", "SAI Line Art", "SAI Lowpoly", "SAI Neonpunk", "SAI Origami", "SAI Photographic",
            "SAI Pixel Art", "SAI Texture", "Ads Advertising", "Ads Automotive", "Ads Corporate", "Ads Fashion Editorial", "Ads Food Photography", "Ads Luxury", "Ads Real Estate", "Ads Retail", 
            "Artstyle Abstract", "Artstyle Abstract Expressionism", "Artstyle Art Deco", "Artstyle Art Nouveau", "Artstyle Constructivist", "Artstyle Cubist", "Artstyle Expressionist", "Artstyle Graffiti", "Artstyle Hyperrealism", "Artstyle Impressionist", 
            "Artstyle Pointillism", "Artstyle Pop Art", "Artstyle Psychedelic", "Artstyle Renaissance", "Artstyle Steampunk", "Artstyle Surrealist", "Artstyle Typography", "Artstyle Watercolor", 
            "Futuristic Biomechanical", "Futuristic Biomechanical Cyberpunk", "Futuristic Cybernetic", "Futuristic Cybernetic Robot", "Futuristic Cyberpunk Cityscape", "Futuristic Futuristic", "Futuristic Retro Cyberpunk", "Futuristic Retro Futurism", 
            "Futuristic Sci Fi", "Futuristic Vaporwave", 
            "Game Bubble Bobble", "Game Cyberpunk Game", "Game Fighting Game", "Game Gta", "Game Mario", "Game Minecraft", "Game Pokemon", "Game Retro Arcade", "Game Retro Game", "Game Rpg Fantasy Game", "Game Strategy Game", "Game Streetfighter", "Game Zelda", 
            "Misc Architectural", "Misc Disco", "Misc Dreamscape", "Misc Dystopian", "Misc Fairy Tale", "Misc Gothic", "Misc Grunge", "Misc Horror", "Misc Kawaii", "Misc Lovecraftian", "Misc Macabre", "Misc Manga", "Misc Metropolis", "Misc Minimalist", 
            "Misc Monochrome", "Misc Nautical", "Misc Space", "Misc Stained Glass", "Misc Techwear Fashion", "Misc Tribal", "Misc Zentangle", 
            "Papercraft Collage", "Papercraft Flat Papercut", "Papercraft Kirigami", "Papercraft Paper Mache", "Papercraft Paper Quilling", "Papercraft Papercut Collage", "Papercraft Papercut Shadow Box", "Papercraft Stacked Papercut", 
            "Papercraft Thick Layered Papercut", "Photo Alien", "Photo Film Noir", "Photo Hdr", "Photo Long Exposure", "Photo Neon Noir", "Photo Silhouette", "Photo Tilt Shift", "Cinematic Diva", "Abstract Expressionism", "Academia", "Action Figure", 
            "Adorable 3D Character", "Adorable Kawaii", "Art Deco", "Art Nouveau", "Astral Aura", "Avant Garde", "Baroque", "Bauhaus Style Poster", "Blueprint Schematic Drawing", "Caricature", "Cel Shaded Art", "Character Design Sheet", "Classicism Art", 
            "Color Field Painting", "Colored Pencil Art", "Conceptual Art", "Constructivism", "Cubism", "Dadaism", "Dark Fantasy", "Dark Moody Atmosphere", "Dmt Art Style", "Doodle Art", "Double Exposure", "Dripping Paint Splatter Art", "Expressionism", 
            "Faded Polaroid Photo", "Fauvism", "Flat 2d Art", "Fortnite Art Style", "Futurism", "Glitchcore", "Glo Fi", "Googie Art Style", "Graffiti Art", "Harlem Renaissance Art", "High Fashion", "Idyllic", "Impressionism", "Infographic Drawing",
            "Ink Dripping Drawing", "Japanese Ink Drawing", "Knolling Photography", "Light Cheery Atmosphere", "Logo Design", "Luxurious Elegance", "Macro Photography", "Mandola Art", "Marker Drawing", "Medievalism", "Minimalism", 
            "Neo Baroque", "Neo Byzantine", "Neo Futurism", "Neo Impressionism", "Neo Rococo", "Neoclassicism", "Op Art", "Ornate And Intricate", "Pencil Sketch Drawing", "Pop Art 2", "Rococo", "Silhouette Art", "Simple Vector Art", "Sketchup", 
            "Steampunk 2", "Surrealism", "Suprematism", "Terragen", "Tranquil Relaxing Atmosphere", "Sticker Designs", "Vibrant Rim Light", "Volumetric Lighting", "Watercolor 2", "Whimsical And Playful"]
    performances = ["Speed", "Quality"]

    def __init__(self):
        self.client = Client("http://127.0.0.1:7860/") 
        self.size = self.correct_size("1024×1024")
        self.styles = [fooocusClient.styles[0]]
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
        
    def check_styles(self, styles):
        for style in styles:
            if style not in fooocusClient.styles:
                print(f"Style {style} not supported")
                return False
        return True
    
    def set_styles(self, styles):
        if self.check_styles(styles):  self.styles = styles

    def check_performance(self, performance):
        if performance not in fooocusClient.performances:
            print(f"Performance {performance} not supported")
            return False
        else:
            return True

    def set_performance(self, performance):
        if self.check_performance(performance):  self.performance = performance


    def generate(self, prompt, negative_prompt="", styles=None, size=None, performance=None, nbimages=None, seed=None, sharpness=None, debug=False):
        if isinstance(prompt, list):
            for p in prompt:
                self.generate(p, negative_prompt, styles, size, performance, nbimages, seed, sharpness, debug)
            return

        styles = styles if styles is not None and self.check_styles(styles) else self.styles
        size = self.correct_size(size if size is not None and self.check_size(size) else self.size)
        performance = performance if performance is not None and self.check_performance(performance) else self.performance
        nbimages = nbimages or self.nbimages
        sharpness = sharpness or self.sharpness
        seed = seed or self.seed or random.randrange(1000)

        job = self.client.submit( #submit is non blocking
            prompt,				# Prompt - str
            negative_prompt,	# Negative promt - str
            styles,			# Styles - [str]
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
            False,	# bool - use 'Input Image'
            "Howdy!",	# str ??
            "Disabled",	# Upscale or Variation - str - Disabled, Vary (Subtle), Vary (Strong), Upscale (1.5x), Upscale (2x), Upscale (Fast 2x) 
            "",	# Upscale image - str - filepath or URL to image
            ["Left"],	# Inpaint or Outpaint directions - List[str] - Left, Right, Top, Bottom
            "",	# Inpaint or outpaint - str - filepath or URL to image
            fn_index=13
            )
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

if __name__ == "__main__":
    cl = fooocusClient()
    print(cl.info())
    print(f"Loaded Fooocus client as 'cl'")