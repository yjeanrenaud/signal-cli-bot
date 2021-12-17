# signal-cli-bot
A simple python3 script based bot for building your own signal channel using signal-cli.
It was built for [PocketPC.ch](https://www.pocketpc.ch).

It depend on [signal-cli](https://github.com/AsamK/signal-cli) and uses it as a dbus service. This project is linked to [signal-cli-newschannel](https://github.com/yjeanrenaud/signal-cli-newschannel) and serves the later with the list of subscribers.

## Installation and Usgae
1. First, install dependencies
``sudo apt-get update;sudo apt-get install python3 python3-pip``
``sudo pip install sqlite3 pprint arrow SystemBus GLib ``
2. and then signal-cli
`git clone https://github.com/AsamK/signal-cli`
and follow [the readme of signal-cli](https://github.com/AsamK/signal-cli)
or use directly [InstallSignalEN.py](https://gist.github.com/Vic3198/f0c9e17ef3d70e7b8c066bfd8cf4db2d)
3. Configure signal-cli with your phone number.
4. Customize the python script `yj_signalbot_regular.py` according to your needs
5. Optional: Install the truster script `yj_trustall_subscribers.py` in crontab
`(crontab -l 2>/dev/null; echo "4 */12 * * * screen -dRS trustall /absolute/path/to/yj_trustall_subscribers.py
") | crontab -`
This is done because some subscribers might change their secrets meanhile and then our bot runs into errors.
6. Run the script, e.g. in a `screen` session: `screen -dmS signal-bot python3 yj_signalbot_regular.py`

## Todos and Future Plans
* encrypt the SQlite and enable other db drivers
* clean the code, oop n stuff
* when [signal-cli](https://github.com/AsamK/signal-cli) enables TRUST command via dbus, change this from shell command in `yj_trustall_subscribers.py`
* parameterisation of the bot
* Use NLP for the chatbot to make it cooler
