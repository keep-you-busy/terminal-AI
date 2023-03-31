import datetime
import logging
import time

import openai
from rich.console import Console
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.style import Style
from rich.theme import Theme

from config.config import settings

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='logger.log',
)

logger = logging.getLogger(__name__)

console = Console(
    theme=Theme(settings.CUSTOM_THEME),
    style=Style(**settings.CUSTOM_STYLE)
    )

progress = Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    )

openai.api_key = settings.OPENAI_TOKEN

MESSAGES = settings.get('MESSAGES')


def check_tokens():
    """Checks all enviroments values"""
    logger.debug('Checking enviroment...')
    names_vars = {
        'OPENAI_TOKEN': settings.OPENAI_TOKEN,
        'MODEL': settings.MODEL,
        'RETRY_PERIOD': settings.RETRY_PERIOD,
        'MESSAGES': settings.MESSAGES
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
        console.print('\n ', Markdown(f'AI: {message}', style='none'))
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
        user_input = input('\n User: ')
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
            model=settings.get('MODEL'),
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


if __name__ == '__main__':
    check_tokens()
    timestamp = int(time.time())
    new_error = None
    while True:
        user_input()
        with progress:
            task = progress.add_task("[green]Processing...")
            try:
                response = get_api_answer(timestamp)
                choices = check_response(response)
                if not choices:
                    raise KeyError('No answer from AI!')
                ai_response = choices[0]['message']['content']
                MESSAGES.append({'role': 'assistant', 'content': ai_response})
                progress.stop()
                progress.remove_task(task_id=task)
                send_message(ai_response)
                new_error = None
            except Exception as error:
                logger.error(error)
                if new_error != error:
                    send_message(f'Bot crashed: "{error}"')
                continue
            finally:
                time.sleep(settings.get('RETRY_PERIOD'))
