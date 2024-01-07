import random
import string

class Random_names:
    def __init__(self):
        self.alphabets = string.ascii_letters
        self.numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def generate(self, name:str) -> str:
        rand_name = ''
        count = 0

        while count != 5:
            if count%2:
                digit = random.choice(self.numbers)
                rand_name += str(digit)
            else:
                letter = random.choice(self.alphabets)
                rand_name += letter
            count += 1
        
        return rand_name
