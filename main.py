import asyncio
import time


from pydantic import BaseModel
from fastapi import FastAPI


class Message(BaseModel):
    content: str
    group_id: int
    token: str

    def __str__(self):
        return self.content


app = FastAPI(debug=True)

"""
actions to send message:
    get user from token
    check if user is in group
    validate message
    get group users
    send message to users
    save message into database
"""

groups = {1: {"name": "sisterslab", "users": ["ayşe", "fatma", "mehmet", "ali"]}}

users = {
    "ayşe": {"age": 20, "mother_name": "halime"},
    "fatma": {"age": 24, "mother_name": "zeynep"},
    "mehmet": {"age": 22, "mother_name": "rahime"},
    "ali": {"age": 25, "mother_name": "ceylan"},
}


@app.post("/send_message")
async def send_message(message: Message):
    start = time.time()
    user = await get_user_from_token(message.token)
    is_user_in_group = await validate_user(user["name"], message.group_id)  # 0.4
    if not is_user_in_group:
        print("User not in group. You cannot send message")
        end = time.time()
        print(f"it took {end - start} seconds to send message")
        return

    is_valid = is_valid_message(message.content)
    if not is_valid:
        print("You cannot send a message longer than 40 words")
        end = time.time()
        print(f"it took {end - start} seconds to send message")
        return

    users = await get_group_users(message.group_id)  # 0.6
    users.remove(user["name"])
    send_message_users_coro = send_message_to_users(users)
    asyncio.create_task(send_message_users_coro)
    save_message_coro = save_message_into_db(message)
    asyncio.create_task(save_message_coro)
    end = time.time()
    print(f"it took {end - start} seconds to send message")
    return message


async def save_message_into_db(message):
    await asyncio.sleep(0.2)
    print("Message is saved")


async def send_message_to_users(users_name):
    tasks = []
    for user_name in users_name:
        task = send_message_to_user(user_name)
        tasks.append(task)

    await asyncio.gather(*tasks)


async def send_message_to_user(user_name):
    await asyncio.sleep(0.2)
    print(f"Message is sent to {user_name}")


async def get_group_users(group_id):
    group = await get_group_from_db(group_id)
    return group["users"]


def is_valid_message(content):
    words = content.split(" ")
    return len(words) < 40


async def validate_user(user_name, group_id):
    group = await get_group_from_db(group_id)
    return user_name in group["users"]


async def get_group_from_db(id):
    await asyncio.sleep(0.2)
    return groups[id]


async def get_user_from_token(token: str):
    user_name = decrypt_token(token)
    return await get_user_from_db(user_name)


def decrypt_token(token: str):
    return token[::-1]


async def get_user_from_db(user_name: str):
    await asyncio.sleep(0.2)
    return {**users.get(user_name, {}), "name": user_name}
