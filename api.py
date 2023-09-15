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
import schedule
from datetime import date


import pandas as pd
from fastapi import FastAPI, Request, Form, UploadFile, File, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from main.app import main, SearchClass
from main.transform_data import readCSV
from main.trie import Trie
from data_models import UpdateCount


# start the rest api
app = FastAPI()
# middleware for cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

global search
# global test_var
app.test = "1"


redis = redis.Redis(host="localhost", port=6379, db=0)
sorted_set_name = 'my_sorted_set'
test_var = "1"

print("reading api.py", os.getpid())
# Initialize Trie
search = SearchClass()
search.pushToRedis(redis)
search.updateTrie(redis)

def get_search_object():
    return search



def print_process_id():
    print("Process ID -> ", os.getpid())

# Start the scheduler
def start_scheduler():
    schedule.every(1).minutes.do(schedule_build_trie, redis)
    while True:
        schedule.run_pending()
        time.sleep(1)


def schedule_build_trie(redis):
    global search
    global test_var
    print('starting schedule_build_trie')
    print_process_id()
    print("test_var -> ", id(test_var), test_var )
    test_var = "2"
    print("app.test -> ", id(app.test), app.test )
    app.test = "2"

    print("object id -> ", id(search))
    search.updateTrie(redis)
    print("object id -> ", id(search))
    res = search.search("Cereal_504055583")
    print("search result -> ", res)
    print('end schedule_build_trie')


# health check
@app.get('/health')
def health_check():
    """
    Health check endpoint.
    :return: 200 if the API is alive.
    """
    response = {"status": 200}

    return response


@app.get("/add_to_redis")
async def add_data_to_redis():
    global trie
    global list_of_lists
    try:
        print('calling endpoint add_to_redis')
        if list_of_lists == []:
            list_of_lists = readCSV()
        for item in list_of_lists:
            value = item[0]  # Assuming the first element is the value to store
            score = item[1]  # Assuming the second element is the score
            redis.zadd(sorted_set_name, {value: score})

        status_code = 200
        body = {'result': "data added to redis sorted set"}

    except Exception as e:
        status_code = 500
        body = {'error': "Exception(main): " + str(e)}

    return JSONResponse(body, status_code)


@app.post("/updatecount")
async def update_item_count(updatecount: UpdateCount):
    try:
        update_payloadObj = jsonable_encoder(updatecount)
        print('calling endpoint update_item_count', update_payloadObj)
        print_process_id()

        value = str(update_payloadObj['item'])

        new_score = redis.zincrby(sorted_set_name, 1, value)
        status_code = 200
        body = {'result': 'updated to - ' + str(new_score)}
    except Exception as e:
        status_code = 500
        body = {'error': "Exception(main): " + str(e)}

    return JSONResponse(body, status_code)


@app.get("/search/{searchString}")
async def get_search_string(searchString: str):
    try:
        global test_var
        search = get_search_object() # adding this as a dependency is not mandatory. This simple direct access to global var will work
        print('calling endpoint', searchString)
        print("object id -> ", id(search))
        print_process_id()
        print("test_var -> ", id(test_var),  test_var )
        test_var = "3"
        print("app.test -> ", id(app.test), app.test )
        app.test = "3"

        res = search.search(searchString)
        status_code = 200
        body = {'result': res}

    except Exception as e:
        status_code = 500
        body = {'error': "Exception(main): " + str(e)}

    return JSONResponse(body, status_code)

@app.get("/add/{value}")
async def add_to_redis(value: str):
    global trie
    global list_of_lists
    try:
        print('calling endpoint - add_to_redis', value)
        redis.zadd("test_data", {value: 0})

        status_code = 200
        body = {'result': "added"}

    except Exception as e:
        status_code = 500
        body = {'error': "Exception(main): " + str(e)}

    return JSONResponse(body, status_code)

@app.get("/update/{value}")
async def update_to_redis(value: str):
    global trie
    global list_of_lists
    try:
        print('calling endpoint - update_to_redis', value)
        new_count = redis.zincrby("test_data",1, value)

        status_code = 200
        body = {'result': new_count}

    except Exception as e:
        status_code = 500
        body = {'error': "Exception(main): " + str(e)}

    return JSONResponse(body, status_code)

@app.get("/get/{value}")
async def get_from_redis(value: str):
    global trie
    global list_of_lists
    try:
        print('calling endpoint - get_from_redis', value)
        score = redis.zscore("test_data", value)
        if score is not None:
            s = f"Score of '{value}' in 'test_data': {score}"
        else:
            s = f"'{value}' does not exist in 'test_data'"
        status_code = 200
        body = {'result': s}

    except Exception as e:
        status_code = 500
        body = {'error': "Exception(main): " + str(e)}

    return JSONResponse(body, status_code)

@app.get("/getall")
async def get_all_from_redis():
    global trie
    global list_of_lists
    try:
        print('calling endpoint - get_all_from_redis')
        score = redis.zrange('test_data', 0, -1, withscores=True)
        if score is not None:
            s = f"Score of all in 'test_data': {score}"
        else:
            s = f"Scores does not exist in 'test_data'"
        status_code = 200
        body = {'result': s}

    except Exception as e:
        status_code = 500
        body = {'error': "Exception(main): " + str(e)}

    return JSONResponse(body, status_code)


if __name__ == "__main__":

     # Start the scheduler in a new thread
    scheduler_thread = threading.Thread(target= start_scheduler)
    scheduler_thread.start()

    uvicorn.run("api:app", host="0.0.0.0", port=8002)

