# stable diffusion & other image generation experiments

## Optional - venv

Create and activate python virtual env
```sh
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

to deactivate the virutal env:
```sh
deactivate
```

## Install

[pytorch install on windows with cuda](https://pytorch.org/get-started/locally/#windows-pip)

Cuda 11:
```sh
pip install -r requirements-torch-windows-cuda11.txt --upgrade
```

Cuda 12:
```sh
pip install -r requirements-torch-windows-cuda12.txt --upgrade
```

Other requirements:
```sh
pip install -r requirements.txt --upgrade
```

## Run the basic stable diffusion cli
```sh
python.exe .\src\sd-cli.py
```

## Use in REPL
Stable Diffusion
```sh
ipython.exe .\src\repl_sd.py
```
Fooocus
```sh
ipython.exe .\src\repl_fooocus.py
```

## Streamlit

Stable diffusion xl turbo
```sh
python -m streamlit run .\src\sdxlturbo_streamlit.py
```

Stream diffusion
```sh
python -m streamlit run .\src\stream-diffusion-streamlit.py
```

## Notebooks

See [notebooks](./src/notebooks/) for more complex examples.

- [stablediffusion with prompt variations](./src/notebooks/stablediffusion-with-prompt-variations.ipynb)
- [stablediffusion xl](./src/notebooks/stablediffusion-xl.ipynb)
- [fooocus-api](./src/notebooks/fooocus-api.ipynb) (get and run [foocus](https://github.com/lllyasviel/Fooocus) first)

## Uninstall

On windows, huggingface models are stored in:
```sh
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

### Tools
- [foocus](https://github.com/lllyasviel/Fooocus)
  
### Articles
- [Effective and efficient diffusion](https://huggingface.co/docs/diffusers/stable_diffusion)
- [Prompt Templates for Stable Diffusion](https://github.com/Dalabad/stable-diffusion-prompt-templates)