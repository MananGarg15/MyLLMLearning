import json


def handle_tool_call(message):
    final_response = []

    for tool_call in message.tool_calls:
        if tool_call.function.name =='get_ticket_price':
            arguments = json.loads(tool_call.function.arguments)
            city = arguments.get('destination_city')
            price_response = get_ticket_price(city)
            response = {
                'role':'tool',
                'content':price_response,
                'tool_call_id':tool_call.id
            }

        final_response.append(response)
    return final_response


ticket_prices = {"london": "$799", "paris": "$899", "tokyo": "$1400", "berlin": "$499"}

def get_ticket_price(destination_city:str):
    print(f"tool called for {destination_city}")
    price = ticket_prices.get(destination_city.lower(),'Price is not known')
    return f"The ticket price for {destination_city} is {price}"