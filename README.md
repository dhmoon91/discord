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
6. We use `black` as auto formatter.

- Install `black`; pip3 install black
- Set `Python › Formatting: Provider` in vscode setting to be `black`.
- **If you have prettier setup, you have to override it**:
  - Open language specific setting in vscode for python(CMD + SHIFT + P)
  - Add this line in
  ```
  [python]:{
     ...
      "editor.defaultFormatter": "ms-python.python"
  }
  ```
- This will set up auto formatting upon saving a file.

7. To enable `pylint` on `pre-push`, please run following command:
```
pre-commit install --hook-type pre-push
```

8. We use `pylint` as base-linter
(Documentation available here: https://code.visualstudio.com/docs/python/linting)

- Install `pylint`; pip3 install pylint
- Open `Settings` in VS Code, search for `Terminal`, find `Terminal > Integrated > Env: Linux` and click `Edit in settings.json`
- Add this line in `settings.json`
```
{
    "python.linting.pylintEnabled": true,
    "python.linting.enabled": true,
    "python.linting.lintOnSave": true
}
```
- Now `pylint` will run when you save a file

9. To call the bot with the desired prefix locally, 

- Add `LOCAL_BOT_PREFIX= ""` to .env with desired prefix between the double quotes

## Packages:

**Pydash**
https://pydash.readthedocs.io/en/latest/index.html

**riotwatcher**
https://riot-watcher.readthedocs.io/en/latest/
