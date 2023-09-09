# MTG Card Bot

A Discord bot to provide information about Magic the Gathering cards.

## Description

This is a bot that can be added to a discord server.
It allows the user to query the mtgsdk for information about cards.

## Getting Started

### Dependencies

* [Python 3](https://www.python.org/)
* Dependencies are listed in the [requirements.txt](requirements.txt) file.
* Primary dependencies are the [mtgsdk](https://github.com/MagicTheGathering/mtg-sdk-python) and [discord.py](https://discordpy.readthedocs.io/en/stable/)

### Installing

* Clone the repository and start a python virtual environment:
  
```bash
python -m venv .
```

* Install the requirements:

```bash
pip -r requirements.txt
```

* In the root directory, create a file name `.env` and add a key value pair, `DISCORD_KEY=yourapikey`

### Executing program

```bash
python mtgb.py
```

## Help

A help menu can be accessed via Discord with the following command: `mtgb:help`
It will provide all of the commands and a brief description.
Passing a command to the help command will give a more in depth breakdown of usage.

## Authors

[Dennis Capone](https://github.com/dcap0)

## Version History

* v0.5.0
  * Initial/Beta release!
  * Implemented MTG Arena export file attachment parsing.
  * Implemented query command to allow user to find a cards and return specific information.

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details

## Acknowledgments

* [Wizards of the Coast](https://company.wizards.com/en) - Thanks for making a neato card game!

## TODO

* Allow user to save cards, then output an MTGA file to upload into the game.
  * Add database functionality? Mongo?
* Maybe something with card rulings.
* Containerize?
