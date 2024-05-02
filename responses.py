from random import choice, randint

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '': 
        return 'no message for a wholesome bot??'
    #elif 'hello' in lowered: 
    #    return 'hello there!'
    elif 'hello there' in lowered: 
        return 'general kenobi!'
    elif 'roll dice' in lowered: 
        return f'you rolled a {randint(1, 21)}'
    elif 'rain' in lowered: 
        return 'furry'
    elif 'einar' in lowered: 
        return 'femboy'
    elif 'will you marry me' in lowered: 
        return 'fine, just this once... <3'
    #else: 
        #return choice(['im not sure what you mean. '
        #                'try asking me to roll a dice or say hello', 
        #                'i dont understand that command. '
        #                'try saying hello or asking me to roll a dice'])