import yfinance as yf

def main():
    NAME = input("Enter stock name (Ex: Apple, Nvidia): ").lower()
    TYPE = input("What's the type of the financial instrument: ").lower()
    lookup(NAME,TYPE)

def lookup(security_name, instrument_type):
    dat = yf.Lookup(security_name)

    if instrument_type == 'cryptocurrency':
        print(dat.cryptocurrency)
    elif instrument_type == 'etf':
        print(dat.etf)
    elif instrument_type == 'stock':
        print(dat.stock)
    elif instrument_type == 'index':
        print(dat.index)
    else:
        print("Wrong Financial Instrument Type")

def stock(stock_name):
          pass
          
if __name__ == "__main__":
    main()