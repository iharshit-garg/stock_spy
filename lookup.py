import yfinance as yf
from ticker import Ticker

def lookup(security_name):
    
    instrumentTypeFields = ['cryptocurrency', 'etf', 'stock', 'index']
    dat = yf.Lookup(security_name)
    
    instrument_type = input("Enter instrument type: ").lower()
    if instrument_type in instrumentTypeFields:
        result = getattr(dat, instrument_type)

        lookedSymbols = []
        i=1
        #This loop iterates over dataframe to fetch symbols and the short name of the security. idx -> 'Symbol'
        for idx, row in result.iterrows():
                print(f"{i}. Symbol: {idx}, Short Name: {row['shortName']}", end="\n\n")
                lookedSymbols.append(idx)
                i+=1
        
        getSymbol = input(f"Select a number (1-{len(lookedSymbols)}): ")
        try:
            getSymbol = int(getSymbol)
            if 1 <= getSymbol <= len(lookedSymbols):
                chosen_symbol = lookedSymbols[getSymbol - 1]
                print(f"You selected: {chosen_symbol}")
                return chosen_symbol #return symbol so that stockSpy can pass the symbol to get the info
            else:
                 print("Out of range!")

        except ValueError:
             print("Invalid!")

    else:
         print("Invalid type!")