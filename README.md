## Running:

1. Ping stanley for env variables;
2. Create **.env** file on root directory with following:

```
RIOT_API_KEY={APIKEY}
DISCORD_TOKEN={TOKEN}
```

3. Install required pip library:
   ` pip3 install -r requirements.txt`
4. Run `npx nodemon --exec python3 bot.py`
5. IF ^ fails, `python3 bot-main.py`

## Packages:

**Pydash**
https://pydash.readthedocs.io/en/latest/index.html

**riotwatcher**
https://riot-watcher.readthedocs.io/en/latest/
