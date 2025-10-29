import yfinance as yf
from lookup import *

def main():

    print("Stock Spy Menu")
    print("1. Lookup")
    print("2. Get Stock Data")
    choice = int(input())
    NAME = input("Enter stock name (Ex: Apple, Nvidia): ").lower()
    
    if choice == 1:
        lookup(NAME)

    elif choice == 2:
        stock(NAME)
          
if __name__ == "__main__":
    main()