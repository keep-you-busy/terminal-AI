import datetime
import logging
import os
import time

import openai
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.style import Style
from rich.theme import Theme

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='logger.log',
)

logger = logging.getLogger(__name__)

load_dotenv()

CUSTOM_THEME = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "danger": "bold red"
})

CUSTOM_STYLE = Style(color="steel_blue", blink=True, bold=True)

console = Console(theme=CUSTOM_THEME, style=CUSTOM_STYLE)

OPENAI_TOKEN = os.getenv('OPENAI_TOKEN')

openai.api_key = OPENAI_TOKEN

RETRY_PERIOD = 5
MODEL = 'gpt-3.5-turbo'
HEADERS = {
    'Authorization': f'Bearer {OPENAI_TOKEN}',
    'Content-Type': 'application/json'
}

MESSAGES = [
    {
     'role': 'system',
     'content': """You are a personal assistant for any user,
                    who will start interact with you."""
    },
    {
     'role': 'user',
     'content': """I am your owner with regular everyday issues,
                    such as finding meaning of life or choosing movie."""
    },
    {
     'role': 'assistant',
     'content': 'Good day! How can I help you today?'
    },
]


def check_tokens():
    """Checks all enviroments values"""
    logger.debug('Checking enviroment...')
    names_vars = {
        'OPENAI_TOKEN': OPENAI_TOKEN,
    }
    missing_vars = [var for var, value in names_vars.items() if not value]
    if missing_vars:
        raise SystemExit(
            f'Missing important enviroment values: {", ".join(missing_vars)}'
        )
    logger.info('Success!')


def send_message(message):
    """Sending the message from AI to console."""
    logger.debug('Sending the message...')
    try:
        console.print(Markdown(f'AI: {message}'))
        logger.info('Success!')
        logger.debug(f'Message received: "{message}"')
    except Exception as error:
        logger.error(f'Impossible to send the message: "{error}"')
        raise Exception(
            f'Impossible to send the message: "{error}"'
        )


def user_input():
    """Takes user input."""
    logger.debug('Taking input...')
    try:
        user_input = input('User:')
        MESSAGES.append({'role': 'user', 'content': user_input})
        logger.info('Success!')
    except ValueError as error:
        raise ValueError(f'Error user input: {error}')


def get_api_answer(timestamp):
    """Request to API by time stamp."""
    logger.debug('Checking API request...')
    try:
        logger.debug(
            f'Sending request to API by time stamp: '
            f'({datetime.datetime.fromtimestamp(timestamp)})'
        )
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=MESSAGES
        )
    except openai.APIError as error:
        raise openai.APIError(
            f'Error request to API: {error}'
        )
    except openai.OpenAIError as error:
        raise openai.OpenAIError(
            f'Error OpenAI: "{error}"'
        )
    logger.info('Success!')
    return response


def check_response(response):
    """Checking documentation request."""
    logger.debug('Checking documentation...')
    if not isinstance(response, dict):
        raise TypeError('Answer is not a dictionary!')
    choices = response.get('choices')
    if not choices:
        raise ValueError('Answer is without data!')
    for choice in choices:
        if not isinstance:
            raise TypeError('Data is not a dictionary!')
        message = choices[0].get('message')
        if not message:
            raise TypeError('Missing message field!')
    logger.info('Success!')
    return choices


def main():
    check_tokens()
    timestamp = int(time.time())
    new_error = None
    while True:
        user_input()
        try:
            response = get_api_answer(timestamp)
            choices = check_response(response)
            if not choices:
                raise KeyError('No answer from AI!')
            ai_response = choices[0]['message']['content']
            MESSAGES.append({'role': 'assistant', 'content': ai_response})
            send_message(ai_response)
            new_error = None
        except Exception as error:
            logger.error(error)
            if new_error != error:
                send_message(f'Bot crashed: "{error}"')
            continue
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    load_dotenv()
    main()
