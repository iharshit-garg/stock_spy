import yfinance as yf

def main():

    print("Stock Spy Menu")
    print("1. Lookup")
    print("2. Get Stock Data")
    choice = int(input())
    NAME = input("Enter stock name (Ex: Apple, Nvidia): ").lower()
    
    if choice == 1:
        lookup(NAME)

    elif choice == 2:
        stock(NAME)

def lookup(security_name):
    instrument_type = input("Enter instrument type: ").lower()
    dat = yf.Lookup(security_name)

    if instrument_type == 'cryptocurrency':
        print(dat.cryptocurrency['shortName'])

    elif instrument_type == 'etf':
        print(dat.etf['shortName'])

    elif instrument_type == 'stock':
        for idx, row in dat.stock.iterrows():   #This loop iterates over dataframe to fetch symbols and the short name of the security. idx -> 'Symbol'
             print(f"Symbol: {idx}, Short Name: {row['shortName']}")

    elif instrument_type == 'index':
        print(dat.index['shortName'])

    else:
        print("Wrong Financial Instrument Type")

def stock(stock_name):
    dat = yf.Ticker(stock_name)
    print(dat.info)
          
if __name__ == "__main__":
    main()