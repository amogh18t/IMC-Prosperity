from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string

class Trader:
    def run(self, state: TradingState):
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))

        # Orders to be placed on exchange matching engine
        result = {}
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            # Initialize the list of Orders to be sent as an empty list
            orders: List[Order] = []
            # Define a fair value for the PRODUCT. Might be different for each tradable item
            # Note that this value of 10 is just a dummy value, you should likely change it!
            acceptable_price = 10
			# All print statements output will be delivered inside test results
            print("Acceptable price : " + str(acceptable_price))
            print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(len(order_depth.sell_orders)))
    
            # Order depth list come already sorted. 
            # We can simply pick first item to check first item to get best bid or offer
            if len(order_depth.sell_orders) != 0:
                best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                if int(best_ask) < acceptable_price:
                    # In case the lowest ask is lower than our fair value,
                    # This presents an opportunity for us to buy cheaply
                    # The code below therefore sends a BUY order at the price level of the ask,
                    # with the same quantity
                    # We expect this order to trade with the sell order
                    print("BUY", str(-best_ask_amount) + "x", best_ask)
                    orders.append(Order(product, best_ask, -best_ask_amount))
    
            if len(order_depth.buy_orders) != 0:
                best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                if int(best_bid) > acceptable_price:
					# Similar situation with sell orders
                    print("SELL", str(best_bid_amount) + "x", best_bid)
                    orders.append(Order(product, best_bid, -best_bid_amount))
            
            result[product] = orders
    
        # String value holding Trader state data required. 
        # It will be delivered as TradingState.traderData on next execution.
        traderData = "SAMPLE" 
        
		# Sample conversion request. Check more details below. 
        conversions = 1
        return result, conversions, traderData






# from tensorflow.keras.models import load_model
# from datamodel import OrderDepth, UserId, TradingState, Order
# from typing import List
# import string
# from typing import Dict
# import numpy as np

# class Trader:
#     def __init__(self, model_path=None):
#         self.model = load_model(model_path)

#     def run(self, state: TradingState):
#         """
#         Only method required. It takes all buy and sell orders for all symbols as an input,
#         and outputs a list of orders to be sent
#         """
#         print("traderData: " + state.traderData)
#         print("Observations: " + str(state.observations))

#         # Orders to be placed on exchange matching engine
#         result = {}
#         for product in state.order_depths:
#             order_depth: OrderDepth = state.order_depths[product]
#             # Initialize the list of Orders to be sent as an empty list
#             orders: List[Order] = []
#             # Define a fair value for the PRODUCT. Might be different for each tradable item
#             # Note that this value of 10 is just a dummy value, you should likely change it!
#             acceptable_price = 10
            
#             # Use neural network to predict whether to buy or sell
#             prediction = self.predict(product, state)
#             print("Neural network prediction for {}: {}".format(product, prediction))
            
#             if prediction == "BUY":
#                 # Place a buy order
#                 best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
#                 print("BUY", str(-best_ask_amount) + "x", best_ask)
#                 orders.append(Order(product, best_ask, -best_ask_amount))
#             elif prediction == "SELL":
#                 # Place a sell order
#                 best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
#                 print("SELL", str(best_bid_amount) + "x", best_bid)
#                 orders.append(Order(product, best_bid, -best_bid_amount))
            
#             result[product] = orders

#         # String value holding Trader state data required.
#         # It will be delivered as TradingState.traderData on next execution.
#         traderData = "SAMPLE"
        
#         # Sample conversion request. Check more details below.
#         conversions = 1
#         return result, conversions, traderData

#     def predict(self, product: str, state: TradingState) -> str:
#         # Extract relevant features from state.observations or order depth information
#         # and convert them into a format suitable for input to the neural network
#         features = self.extract_features(product, state)
        
#         # Make prediction using the neural network model
#         prediction = self.model.predict(features)
        
#         # Convert prediction to "BUY" or "SELL" based on a threshold
#         if prediction >= 0.5:
#             return "BUY"
#         else:
#             return "SELL"
    
#     def extract_features(self, product: str, state: TradingState) -> np.ndarray:
#         # Extract relevant features from the trading state or order depth information
#         order_depth: OrderDepth = state.order_depths[product]
        
#         # Calculate the total buy and sell quantity
#         total_buy_quantity = sum(order_depth.buy_orders.values())
#         total_sell_quantity = sum(order_depth.sell_orders.values())
        
#         # Calculate the bid-ask spread
#         best_bid, _ = list(order_depth.buy_orders.items())[0]
#         best_ask, _ = list(order_depth.sell_orders.items())[0]
#         spread = best_ask - best_bid
        
#         # Calculate the average bid and ask price
#         avg_bid_price = np.mean(list(order_depth.buy_orders.keys()))
#         avg_ask_price = np.mean(list(order_depth.sell_orders.keys()))
        
#         # Calculate the imbalance between buy and sell orders
#         imbalance = total_buy_quantity - total_sell_quantity
        
#         # Calculate the highest bid and lowest ask prices
#         highest_bid = max(order_depth.buy_orders.keys())
#         lowest_ask = min(order_depth.sell_orders.keys())
        
#         # Calculate the total number of buy and sell orders
#         total_buy_orders = len(order_depth.buy_orders)
#         total_sell_orders = len(order_depth.sell_orders)
        
#         # Calculate the difference between the total buy and sell quantities
#         total_quantity_diff = abs(total_buy_quantity - total_sell_quantity)
        
#         # Calculate the total number of trades in the market
#         total_trades = len(state.market_trades[product])
        
#         # Other features can be extracted similarly
        
#         # Combine all features into a numpy array
#         features = np.array([
#             total_buy_quantity, total_sell_quantity, spread, 
#             avg_bid_price, avg_ask_price, imbalance, 
#             highest_bid, lowest_ask, total_buy_orders, 
#             total_sell_orders, total_quantity_diff, total_trades
#         ])

#         return features
