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
```
pip install -r requirements
```

[pytorch install on windows with cuda](https://pytorch.org/get-started/locally/#windows-package-manager)
```
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
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

### Models - stable diffusion
- [stable-diffusion-2-1](https://huggingface.co/stabilityai/stable-diffusion-2-1)
- [stable-diffusion-x4-upscaler](https://huggingface.co/stabilityai/stable-diffusion-x4-upscaler)

### Models - LLMs
- [HuggingFace - search LLMs for stable diffusion prompting](https://huggingface.co/models?search=stable%20diffusion%20prompt)

### Articles
- [Effective and efficient diffusion](https://huggingface.co/docs/diffusers/stable_diffusion)
- [Prompt Templates for Stable Diffusion](https://github.com/Dalabad/stable-diffusion-prompt-templates)