#!/usr/bin/env python

from os import getenv
import os
import json
import traceback
import uvicorn
import aioredis
import redis
import asyncio
import time
import threading
from datetime import date


import pandas as pd
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from main.app import main
from main.transform_data import readCSV
from main.trie import Trie


# start the rest api
app = FastAPI()




# redis = redis.Redis(host="localhost", port=6379, db=0)



# Initialize Trie
trie = Trie()
list_of_lists = []

if list_of_lists == []:
    list_of_lists = readCSV()
    # list_of_lists = list_of_lists[0 : 100]
    print(list_of_lists[0:5])

    for item in list_of_lists:
        trie.insert(item)


# middleware for cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# health check
@app.get('/health')
def health_check():
    """
    Health check endpoint.
    :return: 200 if the API is alive.
    """
    response = {"status": 200}

    return response




@app.get("/search/{searchString}")
async def get_search_string(searchString: str):
    global trie
    global list_of_lists
    try:
        print('calling endpoint', searchString)
        res = main(searchString, trie, list_of_lists)
        status_code = 200
        body = {'result': res}

    except Exception as e:
        status_code = 500
        body = {'error': "Exception(main): " + str(e)}

    return JSONResponse(body, status_code)



if __name__ == "__main__":


    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)



# from fastapi import FastAPI
# import threading

# app = FastAPI()

# data_manager = []

# def process():
#     return ['hello']

# data_manager = process()

# @app.get("/get_data")
# async def get_data():
#     # Access the global data_manager instance
#     global data_manager

#     if data_manager is None:
#         data_manager = data_manager

#     return {"data": data_manager}
