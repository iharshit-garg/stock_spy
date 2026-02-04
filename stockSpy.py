from lookup import lookup
from ticker import Ticker
from data import get_history
import sys

def main():
    while True:
        print("=====================")
        print("Welcome to Stock Spy!")
        print("=====================")
        print("1. Get Basic Info")
        print("2. Get Historic Data")

        userChoice = int(input("Please select an option: "))

        fetch_symbol = input("Do you know the symbol of the security you want to look? ").lower()
        if fetch_symbol in ['no', 'n']:
            NAME = input("Enter stock name (Ex: Apple, Nvidia): ").lower()
            INSTRUMENT_TYPE = input("Enter instrument type: ").lower()
            SYMBOL = lookup(NAME, INSTRUMENT_TYPE)
        elif fetch_symbol in {'yes', 'y'}:
            SYMBOL = input("Enter the Symbol (Ex: AAPL, VOOG): ")
        else:
            sys.exit("Invalid input, please enter [yes/no] OR [y/n]")
        
        #menu choices
        if userChoice == 1:
            ticker_instance = Ticker(SYMBOL)
            print("\n")
            dat = ticker_instance.get_basic_info()
            for k, v in dat.items(): #using dat.items because by default dictionary returns only keys, items() returne both key and the values
                print(f"{k}: {v}")

        elif userChoice == 2:
            data_period = input("Enter period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max): ")
            data_interval = input("Enter interval (1d, 15m): ")
            print(get_history(SYMBOL, data_period, data_interval))

        exit_user = input("\nDo you want to exit ([Y]es/[N]o): ").lower()
        if exit_user in ['yes', 'y']:
            sys.exit("GoodBye!")
        elif exit_user in ['no', 'n']:
            continue
        else:
            sys.exit("\nInvalid Input!\n")

if __name__ == "__main__":
    main()