# gitolite-discord

Send summaries of git commits to a discord channel.

The scipts here are nothing novel but it took me a few hours to figure out how do this in a way that currently suites my needs. 

## git hook script

It appears that git has a think called hooks on my ubuntu machine some examples can be found under /usr/share/git-core/contrib/hooks. I was happy to find the following more sane script in [simple-gitbot](https://github.com/ehamberg/simple-gitbot) 

I am using gitolite and it is possible to run hooks post-commit see the [cookbook](https://gitolite.com/gitolite/cookbook). For me the setup involved loggin into the git server and editing .gitolite.rc to have 'repo-specific-hooks' enable and also have LOCAL_CODE                =>  "$ENV{HOME}/local" define. after that I was able to create local/hooks/repo-specific and put the hooks/discord there.

```
repo demo
    RW+     = keesj
        option hook.post-receive = discord
```

testing the hooks was done by commiting multiple time 


```
md5sum test | tee test ; git add test ; git commit -m test ; git push

```

## git-hook -> discord python code

I decided to use http between the git hook and the discord python script that is running in the background. to send data I used json curl + jq to escape the data


## Discord integration

The discord integration is based on the discord python3 module. I followed [this tutorial on readpython.com](https://realpython.com/how-to-make-a-discord-bot-python/) 

```
pip3 install -U discord # the discord api
pip3 install -U aiohttp # for running a webserver accepting .. incomming requests
```
