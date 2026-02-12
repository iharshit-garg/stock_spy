from lookup import lookup
from ticker import Ticker
from data import get_history, save_data
import sys

def main():
    while True:
        print("=====================")
        print("Welcome to Stock Spy!")
        print("=====================")
        print("[1]. Basic Info")
        print("[2]. Historical Prices")

        try:
            userChoice = int(input("Please select an option: ")) #asking for user choice from the menu, user has to enter a number
        except ValueError:
            print("\nInvalid input! Only number is accepted.\n")
            continue

        SYMBOL = None
        fetch_symbol = input("Do you know the symbol of the security you want to look? ").lower() #asking if user wants to search the security symbol
        if fetch_symbol in ['no', 'n']:
            NAME = input("Enter stock name (Ex: Apple, Nvidia): ").lower()
            INSTRUMENT_TYPE = input("Enter instrument type: ").lower()

            SYMBOL = lookup(NAME, INSTRUMENT_TYPE) #assigning returned symbol to a variable
            if SYMBOL is None: #checking if lookup returns None
                print("\nSymbol Not found!")

        elif fetch_symbol in {'yes', 'y'}:
            SYMBOL = input("Enter the Symbol (Ex: AAPL, VOOG): ")

        else:
            print("\nInvalid input, please enter [yes/no] OR [y/n]\n")
        
        if SYMBOL is not None: #checking if the symbol is not found by the lookup function
            SYMBOL = SYMBOL.upper() #if lowercase, convert it to uppercase
            #configuring menu choices
            if userChoice == 1: #get basic info
                ticker_instance = Ticker(SYMBOL)
                print("\n")
                dat = ticker_instance.get_basic_info()
                for k, v in dat.items(): #using dat.items because by default dictionary returns only keys, items() returne both key and the values
                    print(f"{k}: {v}")

            elif userChoice == 2: #historic data    
                data_period = input("Enter period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max): ")
                data_interval = input("Enter interval (1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo): ")
                hist_data = get_history(SYMBOL, data_period, data_interval)
                if hist_data is None:
                    print("No data found!")
                else:
                    print(f"Total number of rows: {hist_data.shape[0]}\n")
                    print(f"First bar:\n\n{hist_data.head(1)}\n")
                    print(f"Last bar:\n\n{hist_data.tail(1)}")

                    #dataframe is multiIndex
                    print()
                    print(f"Highest High: {hist_data[SYMBOL]["High"].max()}\n")
                    print(f"Lowest Low: {hist_data[SYMBOL]["Low"].min()}\n")
                    print(f"Average Close: {hist_data[SYMBOL]["Close"].mean()}")
                    
                    #saving data
                    get_file_name = f"{SYMBOL}_{data_period}_{data_interval}.csv" #file name: symbol_period_interval.csv
                    save_data(hist_data, get_file_name)

        exit_user = input("\nDo you want to exit ([Y]es/[N]o): ").lower()
        if exit_user in ['yes', 'y']:
            sys.exit("GoodBye!")

        elif exit_user in ['no', 'n']:
            continue
        
        else:
            print("\nInvalid Input!\n")

if __name__ == "__main__":
    main()