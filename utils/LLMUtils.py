# Import built-in packages
import asyncio
import json

# Import downloaded packages
import aiohttp

# Import project files
from config import YGPT_FOLDER_ID, YGPT_TOKEN


async def generate_summary(messages: list[str]) -> str:
    """
    Asynchronously generates a summary by creating a response for each message in the provided list.

    Args:
        messages (list): A list of messages, where each message is expected to have a format that can be processed by `create_response`.

    Returns:
        str: A summary string composed of the responses generated for each message, joined by newline characters.

    This function uses list comprehension to asynchronously call `create_response` for each message and collects the results.
    The results are then joined into a single string with newline characters to form the summary.
    """
    # Create a list of responses by asynchronously calling create_response for each message
    res = [await create_response(message[2]) for message in messages]

    # Join the responses into a single string with newline characters
    return "\n\n".join(res)


# Define an asynchronous function to create a response using the Yandex GPT API
async def create_response(message: str) -> str:
    """
    Asynchronous function to create a response using the Yandex GPT API.

    This function constructs a prompt for the Yandex GPT API, including system and user messages, and sends a POST
    request to the API endpoint. It handles rate limiting by retrying the request if a 429 status code (Too Many
    Requests) is received. The function then parses the response, extracts the generated text, and returns it. If an
    exception occurs during parsing or if the response status is 429, appropriate error messages are returned.

    Args:
        message (str): The user input message to be processed by the Yandex GPT API.

    Returns:
        str: The generated response text from the Yandex GPT API.
    """
    prompt = {
        "modelUri": f"gpt://{YGPT_FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": "Опиши назначение инструмента 1 предложением с упоминанием его названия"
            },
            {
                "role": "user",
                "text": message
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {YGPT_TOKEN}"
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    async with aiohttp.ClientSession(headers=headers) as session:
        response = await session.post(url, json=prompt)
        tries = 10
        while response.status == 429 and tries > 0:
            await asyncio.sleep(1)
            response = await session.post(url, json=prompt)
            tries -= 1
        res = await response.text()
        try:
            res = json.loads(res)
            res = res["result"]["alternatives"]
            res = res[0]["message"]["text"]
        except Exception as e:
            if response.status == 429:
                res = "Too many requests"
            else:
                res = str(e)
        response.close()
    return res
