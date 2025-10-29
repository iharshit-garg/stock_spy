import yfinance as yf
from lookup import *
from ticker import *
import sys

def main():
    print("==============")
    print("Stock Spy Menu")
    print("==============")
    print("1. Look")
    print("2. Get Info")
    print("0. Exit")
    choice = int(input("\nSelect an option: "))
    NAME = input("Enter stock name (Ex: Apple, Nvidia): ").lower() if choice != 0 else None
    
    if choice == 1:
        lookup(NAME)

    elif choice == 2:
        ticker(NAME)
          
    else:
        sys.exit("Goodbye!")

if __name__ == "__main__":
    main()