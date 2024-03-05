from datamodel import Order, TradingState
from Trader import Trader


# model_path = r"D:\amogh18t\Algo Trading\IMC Prosperity\model.h5"
# trader = Trader(model_path)

trader = Trader()

# Create a sample TradingState object (replace this with actual data)
# Make sure to populate the TradingState object with the necessary data
state = TradingState(
    traderData="",
    timestamp=1000,
    listings={},
    order_depths={},
    own_trades={},
    market_trades={},
    position={},
    observations={}
)

# Run the trading algorithm
result, conversions, traderData = trader.run(state)

print("Orders to send:", result)
print("Conversions requested:", conversions)
print("Trader data for next iteration:", traderData)
