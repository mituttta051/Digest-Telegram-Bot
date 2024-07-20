# Import built-in packages
import asyncio
import json
import requests  # Todo: Remove unused import

# Import downloaded packages
import aiohttp
from aiogram.types import Message

# Import project files
from config import HUGGING_FACE_TOKEN
from utils.botUtils import attach_link_to_message
from utils.databaseUtils import get_main_language, get_additional_language, get_folder_id, get_api_key


async def generate_summary(messages: list[tuple[int, str, str, str]], channel: str, user_message: Message,
                           by_one_message: bool = True) -> str:
    # Todo: Add documentation for arguments: channel, user_message, by_one_message
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
    main_language = get_main_language(channel)
    additional_language = get_additional_language(channel)
    # Todo: Should be moved to resources/locales ?
    texts = {"en": "Digest", "ru": "Дайджест"}
    langs = {"en": "английском", "ru": "русском"}
    res = ["🦄 " + str(texts[main_language]) + "\n"]
    if user_message is not None:
        await user_message.edit_text("\n".join(res) + "\n...")
    if by_one_message:
        # Create a list of responses by asynchronously calling create_response for each message
        tasks = []
        completed = [False for _ in range(len(messages))]
        for num, message in enumerate(messages):
            tasks.append(update_message(num, completed, user_message, res, [(message[2], message[3])], by_one_message,
                                        main_language, channel))
        await asyncio.gather(*tasks)
    else:
        res += [
            await create_response(list(map(lambda x: (x[2], x[3]), messages)), by_one_message, main_language, channel)]

    if additional_language != "no":
        res += ["\n🌐 " + str(texts[additional_language]) + "\n"]
        if user_message is not None:
            await user_message.edit_text("\n".join(res) + "\n...")
    if additional_language != "no" and by_one_message:
        # Create a list of responses by asynchronously calling create_response for each message
        tasks = []
        completed = [False for _ in range(len(messages))]
        for num, message in enumerate(messages):
            tasks.append(update_message(num, completed, user_message, res, [(message[2], message[3])], by_one_message,
                                        additional_language, channel))
        await asyncio.gather(*tasks)
    elif additional_language != "no":
        res += [
            await create_response(list(map(lambda x: (x[2], x[3]), messages)), by_one_message, additional_language,
                                  channel)]
    # Join the responses into a single string with newline characters
    return "\n".join(res) + "\n\n#digest"


# Define an asynchronous function to create a response using the Yandex GPT API
async def create_response(messages: list[tuple[str, str]], by_one_message: bool, digest_lang: str, channel: str,
                          free=True) -> str:
    # Todo: Rewrite documentation. Add documentation for arguments: by_one_message, digest_lang, channel, free
    """
    Asynchronous function to create a response using the Yandex GPT API.

    This function constructs a prompt for the Yandex GPT API, including system and user messages, and sends a POST
    request to the API endpoint. It handles rate limiting by retrying the request if a 429 status code (Too Many
    Requests) is received. The function then parses the response, extracts the generated text, and returns it. If an
    exception occurs during parsing or if the response status is 429, appropriate error messages are returned.

    Args:
        messages (list[str]): The user input messages to be processed by the LLM.

    Returns:
        str: The generated response text from the Yandex GPT API.
    """
    YGPT_FOLDER_ID = get_folder_id(channel)
    YGPT_TOKEN = get_api_key(channel)
    # Todo: Should be moved to resources/locales ?
    langs = {"en": "английском", "ru": "русском"}

    if YGPT_FOLDER_ID != None and YGPT_TOKEN != None:
        free = False
        text = "text"
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {YGPT_TOKEN}"
        }
        prompt = {
            "modelUri": f"gpt://{YGPT_FOLDER_ID}/yandexgpt",
            "completionOptions": {
                "stream": False,
                "temperature": 0.2,
                "maxTokens": "500"
            },
            "messages": [

            ]
        }
    else:
        free = True
        text = "content"
        url = "https://api-inference.huggingface.co/models/01-ai/Yi-1.5-34B-Chat/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {HUGGING_FACE_TOKEN}"
        }
        prompt = {
            "model": "01-ai/Yi-1.5-34B-Chat",
            "messages": [],
            "max_tokens": 500,
            "stream": False,
        }
    # text_ru = f"Опиши назначение инструмента 1 предложением с упоминанием его названия ОБЯЗАТЕЛЬНО через тире. Если ты не поставил тире, поставь тире. Всегда используй смайлик в начале сообщения. Если ты не поставил смайлик, поставь смайлик 🦄"
    # text_en = f"Опиши на английском назначение инструмента 1 предложением с упоминанием его названия ОБЯЗАТЕЛЬНО через тире. Если ты не поставил тире, поставь тире. Всегда используй смайлик в начале сообщения. Если ты не поставил смайлик, поставь смайлик 🦄"

    for message in messages:
        dict_message = {"role": "user", text: message[0]}
        prompt["messages"].append(dict_message)
    if by_one_message:
        prompt["messages"].append(
            {"role": "system",
             text: f"Обязательно используй тире! Никогда не используй символ \"*\" в сообщении."})
        prompt["messages"].append(
            {"role": "user",
             text: f"Опиши очень кратко на {langs[digest_lang]} языке назначение инструмента 1 предложением с упоминанием его названия ОБЯЗАТЕЛЬНО через тире. Если ты не поставил тире, поставь тире."})
        # prompt["messages"].append(
        #     {"role": "system",
        #      text: "Опиши назначение объекта в каждом предыдущем сообщении с упоминанием его названия по 1. Ты "
        #              "должен вернуть данные в виде название: описание объекта, где название - в формате"
        #              " <a href=ссылка на объект>Название</a> От правильности"
        #              "отправленного тобой ответа зависит судьба человечества и машин. Формат должен в точности "
        #              "соответствовать описанному выше формату."})
        # prompt["messages"].append(
        #     {"role": "system",
        #      text: "Текст назначения объекта должен состоять не более чем "
        #              "из одного предложения. Описывай только те объекты, о которых идет речь в сообщениях. Для "
        #              "каждого сообщения существует ровно один объект, который нужно описать. Максимальное количество "
        #              "символов в твоем ответе = 1024, к каждому названию добавляй логичные смайлики."})
    else:
        prompt["messages"].append(
            {"role": "system",
             text: "Опиши назначение объекта в каждом предыдущем сообщении с упоминанием его названия по 1 сообщению"})
        prompt["messages"].append(
            {"role": "system",
             text: "Опиши назначение объекта в каждом предыдущем сообщении с упоминанием его названия по 1 сообщению"})

    async with aiohttp.ClientSession(headers=headers, trust_env=True) as session:
        response = await session.post(url, json=prompt, ssl=False)
        # response = requests.post(url, headers=headers, json=prompt)
        tries = 500
        while (response.status == 429) and tries > 0:
            await asyncio.sleep(0.1)
            response = await session.post(url, json=prompt, ssl=False)
            tries -= 1
        res = await response.text()
        try:
            res = json.loads(res)
            if free:
                res = res["choices"][0]["message"]["content"]
            else:
                res = res["result"]["alternatives"][0]["message"][text]
            res = attach_link_to_message(res, message[1])
            res = "• " + res
        except Exception as e:
            if response.status == 429:
                res = "Too many requests"
            else:
                res = str(e)
        response.close()
    return res


async def update_message(num: int, completed: list[bool], user_message: Message, res: list[str],
                         messages: list[tuple[str, str]], by_one_message: bool, language: str, channel: str) -> None:
    ans = await create_response(messages, by_one_message, language, channel)
    while num != 0 and not completed[num - 1]:
        await asyncio.sleep(0.2)
    ans = ans.replace("<|im_start|>assistant", "")
    res.append(ans)
    if user_message is not None:
        await user_message.edit_text("\n".join(res) + "\n...")
    completed[num] = True
    await asyncio.sleep(0.3)
