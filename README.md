# MyClassBot

Attends your classes, marks polls, and send greets the teacher as well.

## Prerequisites

[Python3](https://www.python.org/downloads/)

[Google Chrome](https://www.google.com/intl/en_in/chrome/)

Install Selenium
```bash
pip install -U selenium
```

## Configuration

Change the ID and PASSWORD field to your login ID and Password.
Make sure they are correct. 
Incorrect password is not handled by script right now.

Download chrome web driver according to your chrome version from [here](https://chromedriver.chromium.org/downloads).
PATH is the path to your downloaded web driver

I suggest putting webdriver in a safe place ;)

```python
ID = 1181XXXX 
PASSWORD = 'Something@123'
PATH = "/home/blackhawk/tools/webdriver/chrome/chromedriver"
```

## Usage

Run it using this command.

```bash
python3 test.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://github.com/mayankbist45/MyClassBot/blob/master/LICENSE.md)
