import argparse
from logging import error

class Parser:

    def __init__(self, args):  
        self.args = args.strip().split(" ")
        if len(self.args) > 0 and self.args[0].startswith("-"):
            self.args.insert(0, "")
        self.parser = argparse.ArgumentParser(description='Show the history of names for a person')
        self.parser.add_argument("username",
            help="The username of the person you are searching for",
            type=str, nargs="+"
        )
        self.parser.add_argument("-m", "--max", default=5, type=int,
                            help="The maximum number of name to display")
        self.parser.add_argument("-n", "--name", action="store_true",
                            help="If the search is made by name and not nickname")


    def parse(self):
        return self.parser.parse_known_args(args=self.args)