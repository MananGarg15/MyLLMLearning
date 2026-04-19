import json
from Day4LLMCalling.tool_list import get_ticket_price,set_ticket_price


def handle_tool_call(message):
    final_response = []

    for tool_call in message.tool_calls:
        arguments:dict = json.loads(tool_call.function.arguments)
        function = function_map[tool_call.function.name]
        price_response = function(**arguments)
        response = {
            'role':'tool',
            'content':price_response,
            'tool_call_id':tool_call.id
        }

        final_response.append(response)
    return final_response

function_map = {
    "get_ticket_price":get_ticket_price,
    'set_ticket_price':set_ticket_price
}

price_function = {
    "name": "set_ticket_price",
    "description": "Manages a database of flight ticket prices. Can be used to save prices, look up a specific city's price, or filter cities based on price thresholds.",
    "parameters": {
      "type": "object",
      "properties": {
        "destination_city": {
          "type": "string",
          "description": "The name of the city (e.g., 'London'). Required for 'set' and 'get_by_name' actions."
        },
        "price": {
          "type": "integer",
          "description": "The ticket price in USD. Required for 'set', 'get_by_price', and filter actions."
        },
        "action": {
          "type": "string",
          "enum": [
            "set",
            "get_by_name",
            "get_by_price",
            "filter_by_price_min",
            "filter_by_price_max"
          ],
          "description": "The database operation to perform. 'set' saves/updates a price; 'get_by_name' finds one city; 'get_by_price' finds cities with an exact price; 'filter_by_price_min' finds cities at or above a price; 'filter_by_price_max' finds cities at or below a price."
        }
      },
      "required": ["action"]
    }
  }

tools = [{'type':'function','function':price_function}]



    