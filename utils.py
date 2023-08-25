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
    promptlist=[""]
    cp = ""
    for p in promptparts:
        cp = ("" if( cp=="") else " ")+p
        promptlist.append(cp)
    return promptlist

def generate_all(prompts,generate):
    for p in prompts:
        print(p)
        generate(p)

