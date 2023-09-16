import redis
import time 

from main.transform_data import readCSV
from main.trie import Trie

# Create a Redis connection
redis_host = 'localhost'  # Replace with your Redis server's hostname or IP address
redis_port = 6379  # Replace with your Redis server's port number
redis_db = 0  # Replace with your desired Redis database number

# Connect to Redis
#r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

# # Initialize Trie
# trie = Trie()

# list_of_lists = readCSV()
# # list_of_lists = list_of_lists[0 : 100]
# print(list_of_lists[0:5])

# start_time = time.time()

# for item in list_of_lists:
#     trie.insert(item)

print("reading app.py file")
sorted_set_name = 'my_sorted_set'


def main(searchString, trie, list_of_lists):

    start_time = time.time()
    matched_string_list = trie.autocomplete(searchString)
    print(f"Prefix ${searchString}", len(matched_string_list))
    end_time = time.time()
    print("Time taken for trie -> autosearch action ->", end_time - start_time) 

    start_time = time.time()
    # Sort the list based on the count element (the numeric value)
    sorted_data = sorted(matched_string_list, key=lambda x: x[1], reverse=True)
    end_time = time.time()
    print("Time taken for sort -> sorted_data ->", end_time) 
    print("Sort result", len(sorted_data), sorted_data[0:10]) 

    return sorted_data[0:10]


class SearchClass:
    # _instance = None

    # def __new__(cls):
    #     if cls._instance is None:
    #         cls._instance = super(SearchClass, cls).__new__(cls)
    #         cls._instance.trie = Trie()
    #         cls._instance.list_of_lists = readCSV()
    #     return cls._instance

    def __init__(self) -> None:
        self.trie = Trie()
        self.list_of_lists = readCSV()

    def search(self, searchString):
        print("object id -> self.trie-> ", id(self.trie))
        print("object id -> self.list_of_lists-> ", id(self.list_of_lists))
        start_time = time.time()
        matched_string_list = self.trie.autocomplete(searchString)
        end_time = time.time()
        print("Time taken for trie -> autosearch action ->", end_time - start_time) 

        start_time = time.time()
        # Sort the list based on the count element (the numeric value)
        sorted_data = sorted(matched_string_list, key=lambda x: x[1], reverse=True)
        end_time = time.time()
        print("Time taken for sort -> sorted_data ->", end_time) 
        print("Sort result", len(sorted_data), sorted_data[0:10]) 
        print("object id -> self.trie-> ", id(self.trie))
        print("object id -> self.list_of_lists-> ", id(self.list_of_lists))

        return sorted_data[0:10]
    
    def updateTrie(self, redis):
        try:
            print("object id -> self.trie-> ", id(self.trie))
            print("object id -> self.list_of_lists-> ", id(self.list_of_lists))
            self.list_of_lists = redis.zrange(sorted_set_name, 0, -1, withscores=True)
            # print("redis result -> ", self.list_of_lists[0:10])
            self.trie = Trie()
            for item in self.list_of_lists[0:2]:
                print('item -> ', item[0].decode('utf-8'), item[1])
            for item in self.list_of_lists:
                i = [item[0].decode('utf-8'), item[1]]
                self.trie.insert(i)
            print("object id -> self.trie-> ", id(self.trie))
            print("object id -> self.list_of_lists-> ", id(self.list_of_lists))

        except Exception as e:
            print("Exception -> ", str(e))
    
    def pushToRedis(self, redis):
        try:
            for item in self.list_of_lists:
                self.trie.insert(item)
                redis.zadd(sorted_set_name, {item[0]: item[1]})
        except Exception as e:
            print("Exception -> ", str(e))

    # def updateRedis(self, redis):
    #     try:

    #     except Exception as e:
        

