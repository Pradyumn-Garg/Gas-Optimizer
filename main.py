import shutil
import re

from fastapi import FastAPI, UploadFile, File, Form, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
from pathlib import Path

app = FastAPI()


@app.post("/")
async def root(file: UploadFile):
    # filename = "C:/Users/gargp/Desktop/Adoption.txt"
    # new_filename = Path(filename).stem + ".sol"
    print(file.filename);

    p = Path('C:/Users/gargp/Desktop/temp.txt')
    p.rename(p.with_suffix('.sol'))
    # path = Path('C:/Users/gargp/Desktop/Optimized_contracts/' + file.filename)
    # await save_upload_file(file, path)
    # return {"message": "hi World"}


@app.post("/forloop_optimize")
async def forloop(text: str):
    x = re.findall("for.*\(.*length.*\)", text);
    for i in x:
        st1=""
        ans = re.split('<|>|;|=|\s+|&', i)
        for j in ans:
            if j.find('length')!=-1:
                st1=j
                break
        st2 = st1.split(".")
        st3 = "uint _"+st2[0]+" = "+st1+";\n"

        idx = text.index(i)
        text = text[:idx] + st3 + text[idx:]
        x = i.replace(st1, "_"+st2[0]+" ")
        text = text.replace(i,x)
    return {text}

@app.post("/greaterthan_optimizer")
async def greaterthan(input_string):
    return re.sub(r'>\s*(\d+)', lambda m: f'>= {int(m.group(1))+1}', input_string)\

@app.post("/increment_optimizer")
async def increment(input_string):
    output_string = input_string.replace("i++", "++i").replace("i+=1", "++i").replace("i = i + 1", "++i")
    return output_string

async def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        upload_file.file.seek(0)
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()