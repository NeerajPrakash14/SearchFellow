import redis
import time 

from main.transform_data import readCSV
from main.trie import Trie

# Create a Redis connection
redis_host = 'localhost'  # Replace with your Redis server's hostname or IP address
redis_port = 6379  # Replace with your Redis server's port number
redis_db = 0  # Replace with your desired Redis database number

# Connect to Redis
r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

# # Initialize Trie
# trie = Trie()

# list_of_lists = readCSV()
# # list_of_lists = list_of_lists[0 : 100]
# print(list_of_lists[0:5])

# start_time = time.time()

# for item in list_of_lists:
#     trie.insert(item)

print("reading app.py file")


def main(searchString, trie, list_of_lists):

    # end_time = time.time()
    # print("Time taken for trie -> insert action ->", end_time - start_time)

    # start_time = time.time()
    # print("Prefix 'ba'", trie.autocomplete("ba"))
    # end_time = time.time()
    # print("Time taken for trie -> autosearch action ->", end_time - start_time)
    
    # print("trie", trie)
    # print("trie.root", trie.root)
    # print("trie.root.children", trie.root.children)


    start_time = time.time()
    matched_string_list = trie.autocomplete(searchString)
    print(f"Prefix ${searchString}", len(matched_string_list))
    end_time = time.time()
    print("Time taken for trie -> autosearch action ->", end_time - start_time) 

    start_time = time.time()
    # Sort the list based on the count element (the numeric value)
    sorted_data = sorted(matched_string_list, key=lambda x: x[1])
    end_time = time.time()
    print("Time taken for sort -> sorted_data ->", end_time) 
    print("Sort result", len(sorted_data), sorted_data[0:10]) 

    return sorted_data[0:10]


    # # Insert the list of lists into a sorted set
    # for item in list_of_lists:
    #     value = item[0]  # Assuming the first element is the value to store
    #     score = item[1]  # Assuming the second element is the score
    #     r.zadd('my_sorted_set', {value: score})
    # end_time = time.time()
    # print("Time taken for redis -> store action ->", end_time - start_time)

    # # Retrieve the sorted set
    # sorted_set_values = r.zrange('my_sorted_set', 0, -1, withscores=True)
    # print("Type of data retrived", type(sorted_set_values), sorted_set_values[0])
    # end_time = time.time()
    # print("Time taken for redis -> retrive action ->", end_time - start_time)




# if __name__ == "__main__":
#     main()
