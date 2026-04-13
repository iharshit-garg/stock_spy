from stockspy.client import client

def lookup(security_name: str):
    tickers = [] #storing name, symbol for found symbols

    for t in client.list_tickers(
        search = security_name,
        market = "stocks",
        sort = "ticker",
        limit = 10, #top 10 results
    ):
        tickers.append([t.name, t.ticker])
    
    if not tickers:
        return None #returning None is no symbol is found for the searched security name so CLI can show the error gracefully
    else:
        for i, ticker in enumerate(tickers):
            print(f"{i+1}. name: {ticker[0]}, symbol: {ticker[1]}")
        
        get_symbol = input(f"Select a number (1-{len(tickers)}): ")
        try:
            get_symbol = int(get_symbol) #type -> int
            if 1 <= get_symbol <= len(tickers):
                chosen_symbol = tickers[get_symbol - 1][1]
                print(f"You chose: {chosen_symbol}")
                return chosen_symbol #return symbol so that stockSpy can pass the symbol to get the info
            else:
                print("Out of range!")
            
        except ValueError:
            print("Invalid")