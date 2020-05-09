# The "Do All Stuff" (DAS) Telegram Bot #

The DAS bot is a webhook-based Telegram bot that is written in Python 3.7 and deployed on AWS Lambda. It is capable of telling jokes, sharing fun facts, hosting trivia sessions, and fetching insights from Google Trends.

## Usage ##
Interact with the bot **[@thedasbot](https://t.me/thedasbot)** on Telegram. It supports both private and group chats.

## Commands ##
### Help ###
Pulls up the list of available commands.

**Syntax:** `/help`


### Trivia ###
Gets a random, interactable multiple choice question from [Open Trivia Database](https://opentdb.com/). 

**Syntax:** `/trivia [ <category> | any | help ] [ <difficulty> | any ]`

- `/trivia help` brings up the list of available categories and difficulties. Categories do not need to exactly match what's listed, as long it's enough to uniquely identify it. Leaving any arguments blank will default to `any`, which selects a random category/difficulty.

**Examples**

* `/trivia` - Question from random category and difficulty

* `/trivia history` - Question from the "History" category at random difficulty

* `/trivia anime easy` - Easy question from the "Entertainment: Japanese Anime & Manga" category

* `/trivia any hard` - Hard question from a random category

### Trends ###
Gets insights from Google Trends; capble graphing trends, pulling top trends, and realtime trending searches. It uses the [pytrends](https://github.com/GeneralMills/pytrends) library.

**Syntax:** `/trends <mode> [arguments]`
* `mode` is one of `{ help, graph, top, trending }`
    * `help` - Brings up the syntax help text
    * `graph` - Plots the trends of the given search terms for a specified time period and generates a graph. `arguments` is a list of up to 5 search terms to compare, followed by the optional argument [ `--time <time> `] or [`-t <time>`] to specify a time range. `time` is in the format `<number>< d | w | m | y >` (See examples)
    * `top` - Gets the top searches for a given year. `arguments` is an optional argument to indicate the year. (Default previous year)
    * `trending` - Gets the current trending searches for a specific country. (Default US)

**Examples**
* `/trends graph BMO "Bank of America" RBC` - Graphs the search trends of "BMO", "Bank of America" and "RBC" on the same plot for the past year.
* `/trends graph Honda Toyota --time 6w` - Graphs the search trends of "Honda" and "Toyota" on the same plot in the past 6 weeks.
* `/trends graph GitHub -t 4m` - Graphs the search trends of "GitHub" in the past 4 months.
* `/trends top` - If we're in year 2020, it gets the top searches for year 2019
* `/trends top 2012` - Gets the top searches for 2012
* `/trends trending` - Gets the realtime trending searches in the USA (default region)
* `/trends trending canada` - Gets the realtime trending searches in the Canada
* `/trends trending "new zealand"` - Gets the realtime trending searches in New Zealand

### Joke ###
Fetches a random joke from [icanhazdadjoke](https://icanhazdadjoke.com/).

**Syntax:** `/joke`


### Fact ###
Fetches a random fun fact from [Mental Floss](https://www.mentalfloss.comamazingfactgenerator).

**Syntax:** `/fact`
    
## Contributing ##
Got an feature idea? Make a pull request! New features and improvements are always welcome! New commands should inherit the `BotCommand` class, override at least the `execute` method, and placed inside the `commands/` directory. Also, the command must be added to the `AVAILABLE_COMMANDS` dictionary in `command_parser.py` to be recognized by the parser.

### Local Testing ###
My local webhook setup uses [bottle](https://pypi.org/project/bottle/) and [ngrok](https://ngrok.com/download). This [guide](https://hackernoon.com/serverless-telegram-bot-on-aws-lambda-851204d4236c) is what I used to setup my local environment. If you want to use the same setup, run `install_local`, then `python3 local.py` after you have ngrok running and webhook set.
