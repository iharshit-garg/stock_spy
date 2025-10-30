import yfinance as yf
from lookup import *
from ticker import *
import time
import sys

def main():
    while True:
        print("=====================")
        print("Welcome to Stock Spy!")
        print("=====================")

        NAME = input("Enter stock name (Ex: Apple, Nvidia): ").lower()
        lookup(NAME)

        time.sleep(5)
        exit_user = input("Do you want to exit [yes/no]: ").lower()
        if exit_user =='yes':
            sys.exit("GoodBye!")

if __name__ == "__main__":
    main()