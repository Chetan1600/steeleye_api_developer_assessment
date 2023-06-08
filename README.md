# steeleye_api_developer_assessment
API created for a trading data using fastAPI with endpoints such as list_of_all_trades, search_trade_by_id etc

The code defines a number of endpoints for interacting with a trade database. These endpoints allow users to list all trades, search for trades by ID, counterparty, instrument ID, instrument name, trader name, or advanced filtering criteria.

The TradeDetails class defines the details of a trade, such as the price and quantity. Trade class defines details of a trade such as insturnment id, trade date, asset_class, trader_name etc.

The db variable is a list of Trade objects.

The app variable is an instance of the FastAPI framework.

The "list_of_trades" endpoint uses the get method of the app variable to define an endpoint that can be used to list all trades.

The "search_trade_by_id" endpoint uses the get method of the app variable to define an endpoint that can be used to search for a trade by ID.

The "search_trade_by_counterparty" endpoint uses the get method of the app variable to define an endpoint that can be used to search for a trade by counterparty.

The "search_trade_by_instrument_id" endpoint uses the get method of the app variable to define an endpoint that can be used to search for a trade by instrument ID.

The "search_trade_by_instrument_name" endpoint uses the get method of the app variable to define an endpoint that can be used to search for a trade by instrument name.

The "search_trade_by_trader_name" endpoint uses the get method of the app variable to define an endpoint that can be used to search for a trade by trader name.

The "advanced_filtering" endpoint uses the get method of the app variable to define an endpoint that can be used to search for trades that meet the specified filtering criteria.
