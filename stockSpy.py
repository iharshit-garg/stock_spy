import yfinance as yf
from lookup import *
from ticker import *

def main():
    print("=====================")
    print("Welcome to Stock Spy!")
    print("=====================")

    NAME = input("Enter stock name (Ex: Apple, Nvidia): ").lower()
    lookup(NAME)

if __name__ == "__main__":
    main()