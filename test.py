

# test = 1
# print("global - before-> ", id(test), test)

# def main_fun():
#     global test
#     test = 0
#     print("local - before - main_fun-> ", id(test), test)  # This will print the global variable 'test', which is 1
#     test = 3  # This updates the global variable 'test' to 2
#     print("local - after - main_fun-> ", id(test), test)

# def main():
#     function()

# def function():
#     global test
#     test = 0
#     print("local - before-> ", id(test), test)  # This will print the global variable 'test', which is 1
#     test = 2  # This updates the global variable 'test' to 2
#     print("local - after -> ", id(test), test)

# main_fun()
# # test = 2
# print(test)  # This will print the updated global variable 'test', which is now 2
# print("global - after-> ", id(test), test)

# main()
# print(test)  # This will print the updated global variable 'test', which is now 2
# print("global - after-> ", id(test), test)


class NameClass():
    def __init__(self) -> None:
        pass


test = NameClass()
print("global - before-> ", id(test), test)

def main_fun():
    global test
    test = NameClass()
    print("local - before - main_fun-> ", id(test), test)  # This will print the global variable 'test', which is 1
    test = NameClass() # This updates the global variable 'test' to 2
    print("local - after - main_fun-> ", id(test), test)

def main():
    function()

def function():
    global test
    test = NameClass()
    print("local - before-> ", id(test), test) 
    test = NameClass()
    print("local - before-> ", id(test), test)  # This will print the global variable 'test', which is 1
    test = NameClass()  # This updates the global variable 'test' to 2
    print("local - after -> ", id(test), test)

main_fun()
# test = 2
print(test)  # This will print the updated global variable 'test', which is now 2
print("global - after-> ", id(test), test)

main()
print(test)  # This will print the updated global variable 'test', which is now 2
print("global - after-> ", id(test), test)




# Test by passing varibales and objects ->  for parameters and Arguments


# class NameClass():
#     def __init__(self) -> None:
#         pass


# test = NameClass()
# print("global - before-> ", id(test), test)

# def main_fun():
#     global test
#     test = NameClass()
#     print("local - before - main_fun-> ", id(test), test)  # This will print the global variable 'test', which is 1
#     test = NameClass() # This updates the global variable 'test' to 2
#     print("local - after - main_fun-> ", id(test), test)

# def main():
#     function()

# def function(new_test):
#     # global test
#     print("local - before-> ", id(new_test), new_test) 
#     new_test = NameClass()
#     print("local - before-> ", id(new_test), new_test) 
#     new_test = NameClass()  # This updates the global variable 'test' to 2
#     print("local - after -> ", id(new_test), new_test)

# main_fun()
# # test = 2
# print(test)  # This will print the updated global variable 'test', which is now 2
# print("global - after-> ", id(test), test)

# function(test)
# print(test)  # This will print the updated global variable 'test', which is now 2
# print("global - after-> ", id(test), test)
