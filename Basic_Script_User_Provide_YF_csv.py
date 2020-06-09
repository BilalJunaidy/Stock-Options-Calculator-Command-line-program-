import csv
from sys import argv
from math import log, sqrt, exp, ceil
from scipy.stats import norm

def main():
    term = float(input("Please enter the term of the options (in years): "))
    strike_price = float(input("Please enter the strike price: "))
    stock_price = float(input("Please enter the stock price at the date of grant: "))
    risk_free_rate = float(input("Please enter the risk free rate: "))
    print("For reference, please refer to the 'https://www.bankofcanada.ca/rates/interest-rates/lookup-bond-yields/'")
    number_of_options = int(input("Please enter the number of options issued: "))
    dividend_yield_percentage = float(input("Please enter the dividend yield percent for the expected life of the option: "))
    
    
        
    with open(f"{argv[1]}") as csvfile:
        reader = csv.reader(csvfile)
        N = 1
        header = next(reader)
        old_close = next(reader)[5]
        daily_return_accum = 0
        daily_return_squared_accum = 0

        for row in reader:

            # This condition checks if the row has all elements where the row elements are NULL            
            if row[0] == "NULL":
                continue              
            price_relative = float(row[5])/float(old_close)
            old_close = row[5]
            
            daily_return = log(price_relative)
            daily_return_accum += daily_return
            
            daily_return_squared = daily_return * daily_return
            daily_return_squared_accum += daily_return_squared

            N +=1
            #This is the end of the for loop
            
        NewN = N - 1
        st_dev_daily = sqrt((daily_return_squared_accum/(NewN))-((daily_return_accum*daily_return_accum)/((NewN)*N)))
        historical_volatility = round(st_dev_daily*(sqrt(N/term)),2)
        print(f"HIstorical Volatility: {historical_volatility}")  
  
        variance = (historical_volatility * historical_volatility) 
        d1 = (log(stock_price/strike_price) + ((risk_free_rate/100) - dividend_yield_percentage +(variance/2) * term))/((sqrt(variance))*(sqrt(term)))      
        N_d1 = norm.cdf(d1, 0, 1)
        d2 = d1 - ((sqrt(variance))*(sqrt(term)))
        N_d2 = norm.cdf(d2, 0, 1)
        
        call_value = round(((exp((0 - dividend_yield_percentage) * term))*N_d1*stock_price - strike_price*(exp(0 - (risk_free_rate/100)))*N_d2),2)
        print(f"Per option call value: {call_value}")
        fair_value_option = round(number_of_options * call_value,2)
        print(f"The fair value of the options are {fair_value_option}")       
                         
if __name__=="__main__":
    main()
