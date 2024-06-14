import asyncio
import json
import logging

import aiohttp

from config import YGPT_FOLDER_ID, YGPT_TOKEN


async def generate_summary(messages):
    res = [await create_response(message[2]) for message in messages]
    return "\n\n".join(res)


async def create_response(message):
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
    return res
