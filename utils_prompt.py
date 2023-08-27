
import os
from dotenv import load_dotenv, find_dotenv
from langchain.llms import HuggingFaceHub

def expand(metaprompt):
    promptlist=[""]
    for part in metaprompt.split("/"):
        newpromptlist=[]
        for variation in part.split("|"):
            for partialprompt in promptlist:
                newpromptlist.append(partialprompt+variation) # combine
        promptlist=newpromptlist.copy() #ensure its a copy
    return promptlist

def progress(promptparts):
    promptlist=[]
    cp = ""
    for p in promptparts:
        cp += ("" if( cp=="") else " ") + p
        promptlist.append(cp)
    return promptlist


def generate_prompt(basicprompt):
    load_dotenv(find_dotenv()) # take environment variables from .env.
    assert os.environ.get("HUGGINGFACEHUB_API_TOKEN") is not None
    # search LLMs for stable diffusion prompting:
    # https://huggingface.co/models?pipeline_tag=text-generation&search=stable%20diffusion%20prompt&sort=downloads
    model_id="Ar4ikov/gpt2-650k-stable-diffusion-prompt-generator"
    llm = HuggingFaceHub(repo_id=model_id, model_kwargs={"temperature": 0.1, "max_length": 64})
    enriched = basicprompt + llm(basicprompt)
    print(enriched)
    return enriched


