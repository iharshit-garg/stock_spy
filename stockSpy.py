from lookup import lookup
from ticker import Ticker
from data import get_history
import sys

def main():
    while True:
        print("=====================")
        print("Welcome to Stock Spy!")
        print("=====================")
        print("[1]. Basic Info")
        print("[2]. Historical Prices")

        userChoice = int(input("Please select an option: ")) #asking for user choice from the menu, user has to enter a number

        fetch_symbol = input("Do you know the symbol of the security you want to look? ").lower() #asking if user wants to search the security symbol
        if fetch_symbol in ['no', 'n']:
            NAME = input("Enter stock name (Ex: Apple, Nvidia): ").lower()
            INSTRUMENT_TYPE = input("Enter instrument type: ").lower()

            SYMBOL = lookup(NAME, INSTRUMENT_TYPE) #assigning returned symbol to a variable
            if SYMBOL is None:
                continue

        elif fetch_symbol in {'yes', 'y'}:
            SYMBOL = input("Enter the Symbol (Ex: AAPL, VOOG): ")

        else:
            print("\nInvalid input, please enter [yes/no] OR [y/n]\n")
            continue
        
        #configuring menu choices
        if userChoice == 1: #get basic info
            ticker_instance = Ticker(SYMBOL)
            print("\n")
            dat = ticker_instance.get_basic_info()
            for k, v in dat.items(): #using dat.items because by default dictionary returns only keys, items() returne both key and the values
                print(f"{k}: {v}")

        elif userChoice == 2: #historic data    
            data_period = input("Enter period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max): ")
            data_interval = input("Enter interval (1d, 15m): ")
            hist_data = get_history(SYMBOL, data_period, data_interval)
            if hist_data is None:
                continue

        exit_user = input("\nDo you want to exit ([Y]es/[N]o): ").lower()
        if exit_user in ['yes', 'y']:
            sys.exit("GoodBye!")

        elif exit_user in ['no', 'n']:
            continue
        
        else:
            print("\nInvalid Input!\n")

if __name__ == "__main__":
    main()