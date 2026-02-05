import yfinance as yf

def lookup(security_name: str, instrument_type: str):
    
    instrumentTypeFields = ['cryptocurrency', 'etf', 'stock', 'index'] #supported instrument types
    dat = yf.Lookup(security_name)
    
    if instrument_type in instrumentTypeFields:
        lookedSymbols = [] #initalizing list to add searched symbols
        df = getattr(dat, instrument_type)

        if df is None or df.empty: #checking if the dataframe is empty
             return None #returning none so that cli can decide what to show to the user
        else:
             i = 1
             for idx, name in df['shortName'].head(10).items(): #getting shortName field from the dataframe, showing only top 10 items
                print(i, idx, name)
                lookedSymbols.append(idx)
                i += 1
        
        getSymbol = input(f"Select a number (1-{len(lookedSymbols)}): ")
        try:
            getSymbol = int(getSymbol) #type -> int
            if 1 <= getSymbol <= len(lookedSymbols):
                chosen_symbol = lookedSymbols[getSymbol - 1]
                print(f"You selected: {chosen_symbol}")
                return chosen_symbol #return symbol so that stockSpy can pass the symbol to get the info
            else:
                 print("Out of range!")

        except ValueError:
             print("Invalid!")

    else:
     print("\nInvalid type!\n")
     return None