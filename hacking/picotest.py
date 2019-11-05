#!/usr/bin/env python3
import discord
import asyncio
import json
import os
from aiohttp import web
import aiohttp 

#
# key / channel neet to be put in the enviroment
#
discord_key = os.environ['DISCORD_KEY']
discord_channel = os.environ['DISCORD_CHANNEL']
ctf_team = os.environ['CTF_TEAM']

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

class pico():
    def __init__(self,client):
        self.client = client
        self.url = "https://2019game.picoctf.com/api/v1/scoreboards/e0d42bf04460419aafcf9b392a72868b/scoreboard?search=%s" % ctf_team
        self.score = 0
        self.rank = 0

    async def score_update(self):
        await self.client.wait_until_ready()
        while not self.client.is_closed():
            c = self.client.get_channel(int(discord_channel))
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as r:
                    if r.status == 200:
                        js = await r.json()
                        if js['scoreboard'] is not None:
                            try:
                                new_score = js['scoreboard'][0]['score']
                                new_rank =  js['scoreboard'][0]['rank']
                                print("%d, %d" % (new_score,new_rank))
                                if new_score != self.score and self.score != 0:
                                    await c.send("score update : %d (change %d)" % (new_score, new_score - self.score))
                                if new_rank < self.rank and self.rank != 0:
                                    await c.send("rank update : position is %d (change %d)" % (new_rank, new_rank - self.rank))
                                self.rank = new_rank
                                self.score = new_score
                            except IndexError:
                                print("Index error")
            await asyncio.sleep(600)



client = MyClient()
ws = gitolite_server(client)
pico = pico(client)
client.loop.create_task(ws.webserver())
client.loop.create_task(pico.score_update())
client.run(discord_key)
