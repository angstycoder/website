from decouple import config
from aiohttp import ClientSession
import asyncio
from json import dumps


class BotStats:
    def __init__(self):
        self.base = "https://discord.com/api"
        self.header = {
            "Authorization": f"Bot {config('BOT_TOKEN')}",
            'Content-type': 'application/json'
        }
        self.loop = asyncio.get_event_loop()

    async def request(self, url: str):
        async with ClientSession() as session:
            result = await session.get(url=url, headers=self.header)
            result = await result.json()
        return result

    def run_loop(self, endpoint_attr: list, method: str = None):
        if len(endpoint_attr) == 3:
            endpoint, attribute, webhook_data = endpoint_attr
        else:
            endpoint, attribute = endpoint_attr

        url = f"{self.base}/{endpoint}/{attribute}"
        if method == "POST":
            return self.loop.run_until_complete(self.webhook_post(url=url, data=webhook_data))
        return self.loop.run_until_complete(self.request(url=url))

    def get_stats(self):
        stats = {}
        guilds = self.run_loop(endpoint_attr=['users/@me', 'guilds'])
        stats['guild_count'] = len(guilds)
        mem_cnt = 0
        for guild in guilds:
            id = guild['id']
            guild = self.run_loop(endpoint_attr=['guilds', f'{id}?with_counts=True'])
            if guild is not None:
                mem_cnt += guild['approximate_member_count']
        stats['member_count'] = mem_cnt
        return stats

    async def webhook_post(self, url: str, data: dict):
        async with ClientSession() as session:
            result = await session.post(url=url, headers=self.header, data=dumps(data))
        return result

    def send_webhook(self, message: str):
        data = {
            "username": "Status",
            "avatar_url": "https://i.ibb.co/SyTx61L/pulse.png",
            "content": message
        }

        webhook = self.run_loop(endpoint_attr=['webhooks', f"{config('WEBHOOK_ID')}/{config('WEBHOOK_TOKEN')}", data]
                                , method="POST")