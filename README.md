# Etherscan telegram bot

## Description
This bot alerts you via Telegram whenever any wallets you are interested in sell a token you are tracking. It does this by polling the Etherscan API, and parsing recent transactions for the token you are tracking.

## Prerequisites
1. Create a new Telegram bot using [@BotFather](https://t.me/BotFather) and get the bot token.
1. Create a new Telegram channel and add the bot as an administrator (or tweak its rights and invite it into a group
   chat ).
1. Create an Etherscan API key [here](https://etherscan.io/myapikey).

## Deploy
1. Clone this repository
1. Create a virtual env `python -m venv venv`
1. Activate venv `venv\Scripts\activate`
1. Install dependencies `pip install -r requirements.txt`
1. Copy .env.sample to .env and update the fields
1. Launch the app `python main.py`

## Usage
**/status** - Returns whether or not bot is alive
**/addresses** - Returns a list of addresses currently being tracked
**/add-address <name> <address>** - Adds an address to the list of addresses being tracked
**/remove-address <name>** - Removes an address from the list of addresses being tracked
**/tokens** - Returns the tokens being tracked
**/add-token <emoji> <token-address>**  - Adds a token to track
**/remove-token <address>** - Removes a token from the list of tokens being tracked
**/help** = Prints this info

# Outstanding questions
What are start block and end block?
Do you want me searching the from field?
What info do you want in the message?
What addresses do you want me to search?
Can we do a test?

# Todo
Exclude db from being tracked
get rid of global vars