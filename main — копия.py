import random
import time

def greet(user_name):
    print(f"Здравствуйте, {user_name}!")
    time.sleep(random.random() * 3)
    print("Как я могу вам помочь сегодня?")

user_name = input("Введите ваше имя: ")
greet(user_name)