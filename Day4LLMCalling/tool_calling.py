import json
from Day4LLMCalling.tool_list import get_ticket_price,set_ticket_price, image_generation_function


def handle_tool_call(message):
    responses = []

    for tool_call in message.tool_calls:
        response_object = None
        content = ''
        arguments = json.loads(tool_call.function.arguments)
        function = function_map[tool_call.function.name]
        function_response = function(**arguments)
        if hasattr(function_response, 'filename'):
            response_object = function_response  
            content = "Image generated successfully."
        else:
            content = str(function_response)

        response = {
            'role':'tool',
            'content':content,
            'tool_call_id':tool_call.id
        }

        responses.append(response)
    return responses, arguments, response_object

function_map = {
    "get_ticket_price":get_ticket_price,
    'set_ticket_price':set_ticket_price,
    'image_generation_function':image_generation_function
    
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


image_generation_function = {
    "name": "image_generation_function",
    "description": "Generates an image from a text prompt using an AI image model. Use this tool whenever the user asks to generate, create, draw, or produce an image.",
    "parameters": {
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
                "description": "A descriptive prompt for the image to generate. Be detailed and specific — include subject, style, lighting, colors, and mood where relevant. Example: 'A futuristic cityscape at night with neon lights reflected in rain puddles, cinematic style'."
            }
        },
        "required": ["text"]
    }
}

tools = [{'type':'function','function':price_function},
         {'type':'function','function':image_generation_function}]



    