import yfinance as yf   

def lookup(security_name):
    
    instrumentTypeFields = ['cryptocurrency', 'etf', 'stock', 'index']
    dat = yf.Lookup(security_name)
    
    instrument_type = input("Enter instrument type: ").lower()
    if instrument_type in instrumentTypeFields:
        result = getattr(dat, instrument_type)

        i=1
        #This loop iterates over dataframe to fetch symbols and the short name of the security. idx -> 'Symbol'
        for idx, row in result.iterrows():
                print(f"{i}. Symbol: {idx}, Short Name: {row['shortName']}", end="\n\n")
                i+=1
    else:
         print("Invalid type!")