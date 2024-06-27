# Import built-in packages
import asyncio
import json

# Import downloaded packages
import aiohttp

# Import project files
from config import YGPT_FOLDER_ID, YGPT_TOKEN


async def generate_summary(messages: list[tuple[int, str, str, str]], by_one_message: bool = True) -> str:
    """
    Asynchronously generates a summary by creating a response for each message in the provided list.

    Args: messages (list): A list of messages, where each message is expected to have a format that can be processed
    by `create_response`.

    Returns:
        str: A summary string composed of the responses generated for each message, joined by newline characters.

    This function uses list comprehension to asynchronously call `create_response` for each message and collects the
    results. The results are then joined into a single string with newline characters to form the summary. :param
    messages: :param by_one_message:
    """
    if by_one_message:
        # Create a list of responses by asynchronously calling create_response for each message
        res = [await create_response([(message[2], message[3])], by_one_message) for message in messages]
    else:
        res = [await create_response(list(map(lambda x: (x[2], x[3]), messages)), by_one_message)]

    # Join the responses into a single string with newline characters
    return "\n\n".join(res)


# Define an asynchronous function to create a response using the Yandex GPT API
async def create_response(messages: list[tuple[str, str]], by_one_message: bool) -> str:
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
        :param by_one_message:
        :param messages:
    """
    prompt = {
        "modelUri": f"gpt://{YGPT_FOLDER_ID}/yandexgpt",
        "completionOptions": {
            "stream": False,
            "temperature": 0.01,
            "maxTokens": "6000"
        },
        "messages": [

        ]
    }

    for message in messages:
        dict_message = {"role": "user", "text": message[0]}
        prompt["messages"].append(dict_message)


    if by_one_message:
        prompt["messages"].append(
            {"role": "system",
             "text": f"Обязательно используй тире! Никогда не используй символ \"*\" в сообщении."})
        prompt["messages"].append(
            {"role": "user",
             "text": f"Опиши назначение инструмента 1 предложением с упоминанием его названия ОБЯЗАТЕЛЬНО через тире. Если ты не поставил тире, поставь тире. Всегда используй смайлик в начале сообщения. Если ты не поставил смайлик, поставь смайлик 🦄"})

        # prompt["messages"].append(
        #     {"role": "system",
        #      "text": "Опиши назначение объекта в каждом предыдущем сообщении с упоминанием его названия по 1. Ты "
        #              "должен вернуть данные в виде название: описание объекта, где название - в формате"
        #              " <a href=ссылка на объект>Название</a> От правильности"
        #              "отправленного тобой ответа зависит судьба человечества и машин. Формат должен в точности "
        #              "соответствовать описанному выше формату."})
        # prompt["messages"].append(
        #     {"role": "system",
        #      "text": "Текст назначения объекта должен состоять не более чем "
        #              "из одного предложения. Описывай только те объекты, о которых идет речь в сообщениях. Для "
        #              "каждого сообщения существует ровно один объект, который нужно описать. Максимальное количество "
        #              "символов в твоем ответе = 1024, к каждому названию добавляй логичные смайлики."})
    else:
        prompt["messages"].append(
            {"role": "system",
             "text": "Опиши назначение объекта в каждом предыдущем сообщении с упоминанием его названия по 1 сообщению"})
        prompt["messages"].append(
            {"role": "system",
             "text": "Опиши назначение объекта в каждом предыдущем сообщении с упоминанием его названия по 1 сообщению"})

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {YGPT_TOKEN}"
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    async with aiohttp.ClientSession(headers=headers, trust_env=True) as session:
        response = await session.post(url, json=prompt, ssl=False)
        tries = 100
        while response.status == 429 and tries > 0:
            await asyncio.sleep(0.1)
            response = await session.post(url, json=prompt, ssl=False)
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
