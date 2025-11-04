import yfinance as yf
from lookup import *
from ticker import Ticker
import sys

def main():
    while True:
        print("=====================")
        print("Welcome to Stock Spy!")
        print("=====================")
        print("1. Get Basic Info")
        print("2. Get Earnings History")
        print("3. Asset Screener")

        userChoice = int(input("Please select an option: "))
        NAME = input("Enter stock name (Ex: Apple, Nvidia): ").lower()
        
        if userChoice == 1:
            lookup(NAME)
        elif userChoice == 2:
            ticker_instane = Ticker(NAME)
            ticker_instane.earningsHistory()
        elif userChoice == 3:
            pass

        exit_user = input("Do you want to exit [yes/no]: ").lower()
        if exit_user == 'yes':
            sys.exit("GoodBye!")

if __name__ == "__main__":
    main()