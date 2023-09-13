
import csv
import time


# Initialize an empty list to store the combined strings

# Specify the CSV file path
csv_file_path = '5m Sales Records.csv'  


column1_name = 'Item Type'  
column2_name = 'Order ID'  
column3_name = 'Units Sold'

print("reading transform_data file")

def readCSV():
    combined_strings = []

    start_time = time.time()
    # Open the CSV file for reading
    with open(csv_file_path, mode='r', newline='') as file:
        # Create a CSV reader
        csv_reader = csv.DictReader(file)
        count = 0
        
        # Iterate through each row in the CSV file
        for row in csv_reader:
            # Fetch the values from the specified columns
            value1 = row[column1_name]
            value2 = row[column2_name]
            value3 = row[column3_name]
            count += 1
            if count == 1000000:
                break

            
            # Combine the values into a single string
            combined_string = f'{value1} - {value2}' 
            
            # Append the combined string to the list
            combined_strings.append([combined_string, value3])
    end_time = time.time()
    print("Total time take -> ", end_time - start_time)
    print(len(combined_strings))
    return combined_strings




