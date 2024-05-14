import string
import random

def generate_random_user():
    email = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + "@example.com"
    password = ''.join(random.choices(string.ascii_lowercase, k=10))
    name = ''.join(random.choices(string.ascii_lowercase, k=10))
    return {"email": email, "password": password, "name": name}

