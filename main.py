import shutil
import re

from fastapi import FastAPI, UploadFile, File, Form, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
from pathlib import Path

app = FastAPI()


@app.post("/Loop_Optimizer")
async def Loop(file: UploadFile):
    contents = await file.read()
    text = contents.decode("utf-8")
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
    return text

'''
@app.post("/packing")
async def forloop(text: str):
    ans = re.split(';', text)
    for i in ans:
        st1=""
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
'''

@app.post("/Comparison_Optimizer")
async def Comparison_Optimizer(file: UploadFile):
    contents = await file.read()
    text = contents.decode("utf-8")
    text = re.sub(r'>\s*(\d+)', lambda m: f'>= {int(m.group(1))+1}', text)
    text = re.sub(r'<=\s*(\d+)', lambda m: f'<= {int(m.group(1))-1}', text)
    return text

@app.post("/Increment/Decrement_Optimizer")
async def Increment_Decrement_Optimizer(file: UploadFile):
    contents = await file.read()
    text = contents.decode("utf-8")
    output_string = text.replace("i++", "++i").replace("i+=1", "++i").replace("i = i + 1", "++i").replace("i += 1","++i").replace("i=i+1","++i").replace("i--", "--i").replace("i-=1", "--i").replace("i = i - 1", "--i").replace("i -= 1","--i").replace("i=i-1","--i")
    return output_string

@app.post("/Explicit Initialization of Variables to default values Optimizer")
async def Remove_var_declaration(file: UploadFile):
    contents = await file.read()
    text = contents.decode("utf-8")
    pattern = r"\b(u?int)\b\s+([a-zA-Z_]\w*)\s*=\s*0\b"
    string = re.sub(pattern, r"\1 \2", text)
    return string

@app.post("/Unsigned Integer Types Optimizer")
async def Unsigned_Integer_Types(text: str):
    # contents = await file.read()
    # text = contents.decode("utf-8")
    pattern = r"require\((\w+)\s*!=\s*(\d+)\)"
    string = re.sub(pattern, r"require(\1 > \2)", text)
    return string

@app.post("/Packing variables into a single block Optimizer")
async def Packing_variables_Optimizer(file: UploadFile):
    contents = await file.read()
    text = contents.decode("utf-8")
    pattern = r'(uint128\s+\w+;\s*)(uint256\s+\w+;\s*)(uint128\s+\w+;)'
    string = re.sub(pattern,  r'\1\3\2', text)
    return string
