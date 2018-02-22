import os


class Prompt():
    def __init__(self):
        pass

    def prompt(self, text):
        print("-> {}".format(text))

    def clear(self):
        os.system('clear')
