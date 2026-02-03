from lookup import lookup
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

        fetch_symbol = input("Do you know the symbol of the security you want to look? ").lower()
        if fetch_symbol in ['no', 'n']:
            NAME = input("Enter stock name (Ex: Apple, Nvidia): ").lower()
            INSTRUMENT_TYPE = input("Enter instrument type: ").lower()
            SYMBOL = lookup(NAME, INSTRUMENT_TYPE)
        else:
            SYMBOL = input("Enter the Symbol (Ex: AAPL, VOOG): ")
        
        if userChoice == 1:
            ticker_instance = Ticker(SYMBOL)
            print("\n")
            dat = ticker_instance.get_basic_info()
            for k, v in dat.items(): #using dat.items because by default dictionary returns only keys, items() returne both key and the values
                print(f"{k}: {v}")

        elif userChoice == 2:
            pass
        elif userChoice == 3:
            pass

        exit_user = input("\nDo you want to exit [[Y]es/[N]o: ").lower()
        if exit_user in ['yes', 'y']:
            sys.exit("GoodBye!")
        elif exit_user in ['no', 'n']:
            continue
        else:
            print("\nInvalid Input!\n")

if __name__ == "__main__":
    main()