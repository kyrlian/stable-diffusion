# stable diffusion

## Optional - venv

Create and activate python virtual env
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

to deactivate the virutal env:
```
deactivate
```

## Install
[pytorch install on windows with cuda](https://pytorch.org/get-started/locally/#windows-package-manager)
```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
```

```
pip install -r requirements
```

## Run
```
python.exe .\stablediffusion-cli.py
```

## Uninstall

On windows, huggingface models are stored in:
```
C:\Users\<user>\.cache\huggingface
```

## Ressources

### Python venv
- [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html)

### HuggingFace - Stable diffusion - Doc
- [doc stable_diffusion/text2img](https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/text2img)
- [doc stable_diffusion/img2img](https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/img2img)

### HuggingFace - Stable diffusion - Models
- [Search text-to-image models](https://huggingface.co/models?pipeline_tag=text-to-image)
- [Search image-to-image models](https://huggingface.co/models?pipeline_tag=image-to-image)
- [stable-diffusion-2-1](https://huggingface.co/stabilityai/stable-diffusion-2-1)
- [stable-diffusion-x4-upscaler](https://huggingface.co/stabilityai/stable-diffusion-x4-upscaler)
- [dreamlike-diffusion](https://huggingface.co/dreamlike-art/dreamlike-diffusion-1.0)

### HuggingFace - LLMs - Models
- [Search LLMs for stable diffusion prompting](https://huggingface.co/models?search=stable%20diffusion%20prompt)

### Articles
- [Effective and efficient diffusion](https://huggingface.co/docs/diffusers/stable_diffusion)
- [Prompt Templates for Stable Diffusion](https://github.com/Dalabad/stable-diffusion-prompt-templates)