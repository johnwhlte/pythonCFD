import numpy as np
import random

alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
key_array = []

for i in range(0,10):
    
    key_array.append(alphabet[random.randint(0,25)])

key = ''.join(key_array)

print(key)
