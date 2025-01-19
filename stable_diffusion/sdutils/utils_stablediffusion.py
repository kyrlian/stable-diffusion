from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler, StableDiffusionXLPipeline, StableDiffusionPipeline, StableDiffusionImg2ImgPipeline
from diffusers import AutoPipelineForText2Image
import torch

class simplePipeline:
    def __init__(self, model_id="stabilityai/stable-diffusion-2-1"):
        # Use the DPMSolverMultistepScheduler (DPM-Solver++) scheduler here instead
        pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
        _ = pipe.to("cuda")
        self.pipe = pipe

    def generate(self, prompt, seed=None, **generatekwargs):
        if (seed is not None): generatekwargs["generator"] = torch.Generator("cuda").manual_seed(seed)
        images = self.pipe(prompt, **generatekwargs).images
        return (images[0] if len(images)==1 else images)

class img2imgPipeline:
    def __init__(self, model_id="runwayml/stable-diffusion-v1-5"):
        pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
            model_id, torch_dtype=torch.float16)
        _ = pipe.to("cuda")
        self.pipe = pipe

    def generate(self, prompt, srcimg, nbimages=1, seed=None):
        generator = torch.Generator("cuda").manual_seed(seed) if (seed is not None) else None
        images = self.pipe(prompt, image=srcimg, strength=0.75, guidance_scale=7.5,
                                 num_images_per_prompt=nbimages, generator=generator).images
        return (images[0] if len(images)==1 else images)


class sdxlPipeline:
    # https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/stable_diffusion_xl#diffusers.StableDiffusionXLPipeline
    def __init__(self, model_id="stable-diffusion-xl-base-1.0"):
        pipe = StableDiffusionXLPipeline.from_pretrained(model_id, torch_dtype=torch.float16, use_safetensors=True, variant="fp16")
        _ = pipe.to("cuda")
        # pipe.unet = torch.compile(pipe.unet, mode="reduce-overhead", fullgraph=True) # Not supported on windows yet
        self.pipe = pipe

    def generate(self, prompt1, seed=None, **generatekwargs):
        # generator = torch.Generator("cuda").manual_seed(seed)
        if (seed is not None): generatekwargs["generator"] = torch.Generator("cuda").manual_seed(seed)
        images = self.pipe(prompt1, **generatekwargs).images
        return (images[0] if len(images)==1 else images)

class sdxlturboPipeline:
    # https://huggingface.co/stabilityai/sdxl-turbo
    def __init__(self, model_id="stabilityai/sdxl-turbo"):
        xlturbopipeline = AutoPipelineForText2Image.from_pretrained(model_id, torch_dtype=torch.float16, variant="fp16")
        xlturbopipeline.to("cuda")
        self.pipe = xlturbopipeline

    def generate(self, prompt1, seed=None, **generatekwargs):
        if (seed is not None): generatekwargs["generator"] = torch.Generator("cuda").manual_seed(seed)
        # num_inference_steps=1, guidance_scale=0.0
        images = self.pipe(prompt=prompt1, guidance_scale=0.0, **generatekwargs).images
        return (images[0] if len(images)==1 else images)

class sdRefinerPipeline:
    def __init__(self, model_id = "stabilityai/stable-diffusion-xl-base-1.0", refiner_id = "stabilityai/stable-diffusion-xl-refiner-1.0"):
        base = DiffusionPipeline.from_pretrained(
            model_id, torch_dtype=torch.float16, variant="fp16", use_safetensors=True
        )
        _ = base.to("cuda")
        self.base = base
        refiner = DiffusionPipeline.from_pretrained(
            refiner_id,
            text_encoder_2=base.text_encoder_2,
            vae=base.vae,
            torch_dtype=torch.float16,
            use_safetensors=True,
            variant="fp16",
        )
        _ = refiner.to("cuda")
        self.refiner = refiner

    def generate(self, prompt, seed=None):
        # Define how many steps and what % of steps to be run on each experts (80/20) here
        n_steps = 40
        high_noise_frac = 0.8
        generator = torch.Generator("cuda").manual_seed(seed) if (seed is not None) else None
        # run both experts
        base_image = self.base(
            prompt=prompt,
            num_inference_steps=n_steps,
            denoising_end=high_noise_frac,
            output_type="latent",
            generator=generator
        ).images[0]
        refined_image = self.refiner(
            prompt=prompt,
            num_inference_steps=n_steps,
            denoising_start=high_noise_frac,
            image=base_image,
            generator=generator
        ).images[0]
        return refined_image
