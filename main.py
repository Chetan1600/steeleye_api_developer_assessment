from fastapi import FastAPI
from typing import List ,Optional
from datetime import datetime
from pydantic import BaseModel, Field

class TradeDetails(BaseModel):
    buySellIndicator: str = Field(description="A value of BUY for buys, SELL for sells.")
    price: float = Field(description="The price of the Trade.")
    quantity: int = Field(description="The amount of units traded.")

class Trade(BaseModel):
    asset_class: Optional[str] = Field( description="The asset class of the instrument traded. E.g. Bond, Equity, FX...etc")
    counterparty: Optional[str] = Field(description="The counterparty the trade was executed with. May not always be available")
    instrument_id: str = Field( description="The ISIN/ID of the instrument traded. E.g. TSLA, AAPL, AMZN...etc")
    instrument_name: str = Field( description="The name of the instrument traded.")
    trade_date_time: datetime = Field( description="The date-time the Trade was executed")

    trade_details: TradeDetails = Field( description="The details of the trade, i.e. price, quantity")

    trade_id: int = Field(description="The unique ID of the trade")
    trader: str = Field(description="The name of the Trader")

app = FastAPI()

# end point for List of trades 

class TradesList(BaseModel):
    trades: List[Trade]
    #total_count: int

#data_length=len(TradesList(trades=db))

@app.get("/trades")
async def list_of_trades(page_num:int = 1, page_size:int = 5):
    start = (page_num-1)*page_size
    end=start+page_size
    total_entries=len(db)
    response={
        "data": db[start:end],
        "total": total_entries,
        "count": page_size,
        "pagination": {}
    }

    if end>=total_entries:
        response['pagination']['next']=None

        if page_num>1:
            response['pagination']['previous']=f'/trades?page_num={page_num-1}&page_size={page_size}'
        else:
            response['pagination']['previous']=None
    else:
        if page_num>1:
            response['pagination']['previous']=f'/trades?page_num={page_num-1}&page_size={page_size}'
        else:
            response['pagination']['previous']=None
        response['pagination']['next']=f'/trades?page_num={page_num+1}&page_size={page_size}'

    return response


@app.get("/trades/trade_id/{id}")
async def Search_Trade_By_Id(trade_id: int):
    for trade in db:
        if trade.trade_id == trade_id:
            return trade
    return {"error": "Trade not found"}

@app.get("/trades/counter_party/{search}")
async def Search_Trade_By_counterparty(search : Optional[str]=None):
    matching=[]
    for i in db:
        if i.counterparty.lower()==search.lower():
            matching.append(i)
    if len(matching)==0:
        return f"counter party {search} not found in database"
    else:
        return matching
    
@app.get("/trades/instrumentId/{search}")
async def Search_Trade_By_InstrumentId(search : Optional[str]=None):
    matching=[]
    for i in db:
        if i.instrument_id.lower()==search.lower():
            matching.append(i)
    if len(matching)==0:
        return f"instrunment id {search} not found in database"
    else:
        return matching
    
@app.get("/trades/instrumentName/{search}")
async def Search_Trade_By_instrumentName(search : Optional[str]=None):
    matching=[]
    for i in db:
        if i.instrument_name.lower()==search.lower():
            matching.append(i)
    if len(matching)==0:
        return f"instrunment name {search} not found in database"
    else:
        return matching

@app.get("/trades/trader_name/{search}")
async def Search_Trade_By_traderName(search : Optional[str]=None):
    matching=[]
    for i in db:
        if i.trader.lower()==search.lower():
            matching.append(i)
    if len(matching)==0:
        return f"trader name {search} not found in database"
    else:
        return matching
    
@app.get("/trades/advanced_filtering")
async def Advanced_filters(
    assetClass: Optional[str] = None,
    end: Optional[datetime] = None,
    maxPrice: Optional[float] = None,
    minPrice: Optional[float] = None,
    start: Optional[datetime] = None,
    tradeType_Buy_or_Sell: Optional[str] = None   ):
    if assetClass:
        matching=[]
        for i in db:
            if i.asset_class.lower()==assetClass.lower():
                  matching.append(i)
        if len(matching)==0:
            return f"asssetClass {assetClass} not found in database"
        else:
            return matching
    if end:
        matching=[]
        for i in db:
            if i.trade_date_time <= end:
                  matching.append(i)
        if len(matching)==0:
            return f"No trades happened before {end}"
        else:
            return matching
        
    if maxPrice:
        matching=[]
        for i in db:
            if i.trade_details.price <= maxPrice:
                  matching.append(i)
        if len(matching)==0:
            return f"No trade whose value is less than {maxPrice}"
        else:
            return matching
        
    if minPrice:
        matching=[]
        for i in db:
            if i.trade_details.price >= minPrice:
                  matching.append(i)
        if len(matching)==0:
            return f"No trade whose value is greater than {minPrice}"
        else:
            return matching
        
    if start:
        matching=[]
        for i in db:
            if i.trade_date_time >= start:
                  matching.append(i)
        if len(matching)==0:
            return f"No trades happened after {start}"
        else:
            return matching
      
    if tradeType_Buy_or_Sell:
        matching=[]
        for i in db:
            if i.trade_details.buySellIndicator.lower() == tradeType_Buy_or_Sell.lower():
                  matching.append(i)
        if len(matching)==0:
            return f"The trade type should be either buy or sell"
        else:
            return matching
# Mock database

db:List[Trade]=[
    
Trade(asset_class="Equity", counterparty="XYZ Bank", instrument_id="AAPL", instrument_name="Apple Inc", 
      trade_date_time=datetime(2022, 4, 1, 12, 30), trade_details=TradeDetails(buySellIndicator="BUY", price=150.0, quantity=100),
        trade_id=1, trader="John Smith"), 
                
Trade(asset_class="FX", counterparty="ABC Bank", instrument_id="EURUSD", instrument_name="Euro/US Dollar", 
      trade_date_time=datetime(2022, 3, 31, 9, 45), trade_details=TradeDetails(buySellIndicator="SELL", price=1.1750, quantity=5000), 
      trade_id=2, trader="Jane Doe"),

Trade(asset_class="Bond", counterparty="DEF Bank", instrument_id="US00123ABC45", instrument_name="US Treasury 10-year Bond",
       trade_date_time=datetime(2022, 4, 2, 14, 15), trade_details=TradeDetails(buySellIndicator="BUY", price=98.5, quantity=1000), 
       trade_id=3, trader="Bob Johnson"),

Trade(asset_class="Equity", counterparty="XYZ Bank", instrument_id="AAPL", instrument_name="Apple Inc", 
      trade_date_time=datetime(2022, 4, 1, 12, 30), trade_details=TradeDetails(buySellIndicator="BUY", price=150.0, quantity=100),
        trade_id=4, trader="John Smith"), 

Trade(asset_class="FX", counterparty="ABC Bank", instrument_id="EURUSD", instrument_name="Euro/US Dollar", 
      trade_date_time=datetime(2022, 3, 31, 9, 45), trade_details=TradeDetails(buySellIndicator="SELL", price=1.1750, quantity=5000),
        trade_id=5, trader="Jane Doe"),

Trade(asset_class="Bond", counterparty="DEF Bank", instrument_id="US00123ABC45", instrument_name="US Treasury 10-year Bond",
       trade_date_time=datetime(2022, 4, 2, 14, 15), trade_details=TradeDetails(buySellIndicator="BUY", price=98.5, quantity=1000), 
       trade_id=6, trader="Bob Johnson"),
    
Trade(asset_class="FX", counterparty="ABC Bank", instrument_id="GBPUSD", instrument_name="British Pound/US Dollar",
       trade_date_time=datetime(2022, 4, 5, 10, 30), trade_details=TradeDetails(buySellIndicator="BUY", price=1.3800, quantity=3000), 
       trade_id=7, trader="John Smith"),
    
Trade(asset_class="Equity", counterparty="XYZ Bank", instrument_id="GOOGL", instrument_name="Alphabet Inc",
       trade_date_time=datetime(2022, 4, 6, 16, 45), trade_details=TradeDetails(buySellIndicator="SELL", price=2300.0, quantity=50), 
       trade_id=8, trader="Jane Doe"),

Trade(asset_class="Bond", counterparty="DEF Bank", instrument_id="US00459GQT52", instrument_name="US Treasury 5-year Bond", 
      trade_date_time=datetime(2022, 4, 7, 13, 15), trade_details=TradeDetails(buySellIndicator="SELL", price=98.25, quantity=500),
        trade_id=9, trader="Bob Johnson"),

Trade(asset_class="Equity", counterparty="XYZ Bank", instrument_id="MSFT", instrument_name="Microsoft Corporation", 
      trade_date_time=datetime(2022, 4, 8, 14, 0), trade_details=TradeDetails(buySellIndicator="BUY", price=260.0, quantity=75),
        trade_id=10, trader="John Smith"),

Trade(asset_class="FX", counterparty="ABC Bank", instrument_id="AUDUSD", instrument_name="Australian Dollar/US Dollar", 
      trade_date_time=datetime(2022, 4, 9, 11, 30), trade_details=TradeDetails(buySellIndicator="SELL", price=0.7500, quantity=10000), 
      trade_id=11, trader="Jane Doe"),
    
Trade(asset_class="Bond", counterparty="DEF Bank", instrument_id="US912828M645", instrument_name="US Treasury 30-year Bond", 
      trade_date_time=datetime(2022, 4, 12, 9, 0), trade_details=TradeDetails(buySellIndicator="BUY", price=100.0, quantity=500), 
      trade_id=12, trader="Bob Johnson"),

Trade(asset_class="FX", counterparty="XYZ Bank", instrument_id="GBPUSD", instrument_name="British Pound/US Dollar", 
      trade_date_time=datetime(2022, 4, 3, 14, 30), trade_details=TradeDetails(buySellIndicator="BUY", price=1.3900, quantity=10000),
        trade_id=13, trader="John Smith"),

Trade(asset_class="Equity", counterparty="DEF Bank", instrument_id="MSFT", instrument_name="Microsoft Corporation", 
      trade_date_time=datetime(2022, 4, 4, 10, 15), trade_details=TradeDetails(buySellIndicator="SELL", price=300.0, quantity=200), 
      trade_id=14, trader="Jane Doe"),

Trade(asset_class="FX", counterparty="ABC Bank", instrument_id="USDJPY", instrument_name="US Dollar/Japanese Yen", 
      trade_date_time=datetime(2022, 4, 5, 9, 0), trade_details=TradeDetails(buySellIndicator="SELL", price=110.50, quantity=10000), 
      trade_id=15, trader="Bob Johnson") 

]