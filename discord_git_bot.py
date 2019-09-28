#!/usr/bin/env python3
import discord
import asyncio
import json
import os
from aiohttp import web

#
# key / channel neet to be put in the enviroment
#
discord_key = os.environ['DISCORD_KEY']
discord_channel = os.environ['DISCORD_CHANNEL']

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

class gitolite_server():
    def __init__(self,client):
        self.client = client

    async def webserver(self):

        async def handle(request):
            print("Incomming request")
            text = "Hello\n"
            c = self.client.get_channel(int(discord_channel))
            a = await request.json()
            print(a)
            message = "{summary}".format(summary=a['summary'])
            await c.send(message)
            message = "{log}".format(log=a['log'])
            await c.send(message)
            return web.Response(text=text)

        app = web.Application()
        app.add_routes([web.post('/gitolite', handle)])
        runner =web.AppRunner(app)
        await runner.setup()
        self.site = web.TCPSite(runner,'127.0.0.1',1337) # make sure it is really only bindin to localhost..
        await self.site.start()

    def _unload(self):
        asyncio.ensure_future(self.site.stop)


client = MyClient()
ws = gitolite_server(client)
client.loop.create_task(ws.webserver())
client.run(discord_key)
