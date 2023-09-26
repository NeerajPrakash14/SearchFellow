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
import pickle

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

# Event to signal when the calculate function is done
calculate_done = threading.Event()

print("reading api.py", os.getpid())
# Initialize Trie
redis.flushall()
redis.set('test', 'Hello! This is a sample test string')
search = SearchClass()
search.pushToRedis(redis)
search.updateTrie(redis)
trie_global = search.trie.root
list_of_lists = readCSV()

def get_search_object():
    return search

def get_test_object():
    return test_var


def print_process_id():
    print("Process ID -> ", os.getpid())
def print_thread_id():
    print("Thread id -> ", threading.get_ident())
    

def autocomplete(prefix, redis, id, root, last_string, new_string):
    print("*****START autocomplete*******", prefix, redis, id, root, last_string, new_string)
    results = []
    node = root

    if(prefix is not None or prefix != ""):
        # Traverse to the last node of the prefix
        for char in prefix: 
            if char not in node.children:
                return results
            node = node.children[char]
    
    print("before saving to redis -> ", node, node.children, node.is_end_of_word)
    serialized_obj = pickle.dumps(node)
    redis.set(id, serialized_obj)
    redis.set(100, new_string)


    # Perform a depth-first search to find all words with the given prefix
    find_words_with_prefix(node, prefix, results)
    print("*****END autocomplete*******")

    return results

def find_words_with_prefix(node, current_prefix, results):
    if node.is_end_of_word:
        results.append([current_prefix, node.count])
    for char, child_node in node.children.items():
        find_words_with_prefix(child_node, current_prefix + char, results)

# Start the scheduler
def start_scheduler():
    schedule.every(3).minutes.do(schedule_build_trie, redis)
    while True:
        schedule.run_pending()
        time.sleep(1)


def schedule_build_trie(redis):
    print('start schedule_build_trie')
    global search
    # time.sleep(20)
    print_process_id()
    print_thread_id()
    # global test_var
    # test_var = get_test_object()
    # print("test_var -> ", id(test_var),  test_var )
    # test_var = "2"
    # print("test_var -> ", id(test_var),  test_var )

    # all_global_vars = globals().keys()
    # print("Global Variables:")
    # for var in all_global_vars:
    #     print(var)
    #     if var == 'search':
    #         print("Global Variables -> search ", var, id(all_global_vars['search']))

    # local_vars = schedule_build_trie.__code__.co_varnames
    # print("\nLocal Variables (in my_function):")
    # for var in local_vars:
    #     print(var)
    #     if var == 'search':
    #         print("nLocal Variables -> search ", var, id(local_vars['search']))
    # print("search object id -> ", id(search))

    # print("search.trie object id -> ", id(search.trie))
    search.updateTrie(redis)
    # print("search object id -> ", id(search))
    res = search.search("Cereal_504055583")
    # calculate_done.set()
    # print("search result -> ", res)
    print('end schedule_build_trie')


def find_difference(last, new):
    print("*****find_difference*****", last, new)
    difference = ""
    for char in new:
        if char not in last:
            difference += char
    return difference

@app.get("/search/{searchString}/{id}")
async def get_search_string(searchString: str, id: int):
    try:
        print_process_id()
        print("thread id -> ", threading.get_ident())
        print("id -> ", id)
        trie_local = None
        last_string = ""
        retrieved_data = redis.get(id)
        last_search_string = redis.get(100)
        if retrieved_data is not None:
            deserialized_obj = pickle.loads(retrieved_data)
            trie_local = deserialized_obj
            print("Key found in Redis")
            # print("trie_local -> child node children-> ",trie_local.children['e'].children, trie_local.children['e'].is_end_of_word)  
        else:
            print("Key not found in Redis")
            trie_local = trie_global
        
        if last_search_string is not None:
            last_string = last_search_string.decode('utf-8')

        print("trie_local -> ", trie_local, trie_local.children, trie_local.is_end_of_word)  
        prefix = find_difference(last_string, searchString)
        # time.sleep(5)
        # global test_var
        # global search
        # print("test_var -> ", id(test_var),  test_var )
        # test_var = "3"
        # search = get_search_object() 
        # print('calling endpoint', searchString)
        # print("object id -> ", id(search.trie))
        # print("test_var -> ", id(test_var),  test_var )
        # test_var = "3"
        # print("app.test -> ", id(app.test), app.test )
        # app.test = "3"
        # all_global_vars = globals().keys()
        # print("Global Variables:")
        # for var in all_global_vars:
        #     print(var)
        #     if var == 'search':
        #         print("Global Variables -> search ", var, id(all_global_vars['search']))

        # local_vars = get_search_string.__code__.co_varnames
        # print("\nLocal Variables (in my_function):")
        # for var in local_vars:
        #     print(var)
        #     if var == 'search':
        #         print("nLocal Variables -> search ", var, id(local_vars['search']))

        # res = search_local.search(searchString)
        matched_string_list = autocomplete(prefix, redis, id, trie_local, last_string, searchString)

        start_time = time.time()
        # Sort the list based on the count element (the numeric value)
        sorted_data = sorted(matched_string_list, key=lambda x: x[1], reverse=True)
        end_time = time.time()
        print("Time taken for sort -> sorted_data ->", end_time) 
        # print("Sort result", len(sorted_data), sorted_data[0:10]) 
        # print("object id -> self.trie-> ", id(self.trie))
        # print("object id -> self.list_of_lists-> ", id(self.list_of_lists))

        return sorted_data[0:10]
        status_code = 200
        body = {'result': res}

    except Exception as e:
        status_code = 500
        body = {'error': "Exception(main): " + str(e)}

    return JSONResponse(body, status_code)


@app.get("/fetchfromredis")
async def fetch_from_redis():
    try:
        print('calling endpoint - fetch_from_redis')
        value = redis.get('test').decode('utf-8')
        status_code = 200
        body = {'result': value}

    except Exception as e:
        status_code = 500
        body = {'error': "Exception(main): " + str(e)}

    return JSONResponse(body, status_code)



@app.get("/sort")
async def sort_list():
    try:
        global search
        print('calling endpoint - sort_list')
        print("Length of list -> ", len(list_of_lists))
        start_time = time.time()
        sorted_data = sorted(list_of_lists, key=lambda x: x[1], reverse=True)
        end_time = time.time()
        print("Time taken for sort -> sorted_data ->", end_time - start_time) 
        status_code = 200
        body = {'result': sorted_data}

    except Exception as e:
        status_code = 500
        body = {'error': "Exception(main): " + str(e)}

    return JSONResponse(body, status_code)

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
    # scheduler_thread.start()

    uvicorn.run("api:app", host="0.0.0.0", port=8002, reload=True, workers=1)

    # Main thread
    while True:
        # Wait for the calculation to finish
        calculate_done.wait()
        
        # Print the updated variable
        print("Updated test_var:", test_var)
        
        # Reset the event for the next calculation
        calculate_done.clear()

        # Sleep or perform other actions as needed
        time.sleep(10)  #

    # start_scheduler()


