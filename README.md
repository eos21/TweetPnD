# Tweet Pump-and-Dump
### Description
Performs trades on Bittrex based on tweets of a user. Searches tweets for any
mentions of currencies available on Bittrex. Optionally searches for a key
term/phrase first before searching for currencies.

### Configuration
A file named `config.json`, located in `/src/` (same directory as `bot.py`), is
used as the configuration of the bot. Below is the base configuration for the
bot:

```json
{
    "twitter": {
        "api": {
            "key": "",
            "secret": "",
            "access_token": "",
            "access_secret": ""
        },
        "user": "",
        "search_term": "",
        "search_text": true,
        "search_image": true,
        "ignore_retweets": true,
        "disconnect_on_first": true,
        "log_tweets": false
    },
    "exchanges": {
        "binance": {
            "priority": 0,
            "key": "",
            "secret": "",
            "use_multiplier": false,
            "recvWindow": 5000
        },
        "bittrex": {
            "priority": 1,
            "key": "",
            "secret": "",
            "use_multiplier": true,
        }
    },
    "order": {
        "quote_currencies": {
            "btc": 0,
            "eth": 0
        },
        "multiplier": 0
    },
    "search_currency_name": false,
    "tessdata_dir": "",
    "tesseract_cmd": "",
    "verbose": false
}
```

> **Note**: All strings, with the exceptions of authentication credentials,
`user`, `search_term`, and `tesseract_cmd`, must be completely lower case.

* `search_currency_name` - `true` to include currency names (in addition to
ticker symbols) in the regular expression used to search for a currency in the
OCR result text; `false` to only include currency ticker symbols.
* `tessdata_dir` - Path to Tesseract's tessdata folder. Set this if the bot
is on a different drive than Tesseract is installed to - particularly if using
Windows. This folder is typically located under the Tesseract install's root
directory.
* `tesseract_cmd` - Path to the Tesseract binary; ignored if empty. Unnecessary
if it is in the system's `PATH`. Backslashes must be escaped with another
backslash.
* `verbose` - `true` if the console logger should be more verbose i.e. show
debug-level messages; `false` otherwise.

#### Twitter
* `key` - Consumer key (API key)
* `secret` - Consumer secret (API secret)
* `access_token` - Access token; can be used to make API requests on your own
account's behalf.
* `access_secret` - Access secret
* `user` - The Twitter handle of the user whose tweets will be read.
* `search_term` - A search term to use to filter the user's tweets; ignored if
empty.
* `search_text` - `true` to search for currencies in the tweet's text; `false`
otherwise.
* `search_image` - `true` to search for currencies in the tweet's attached
image; `false` otherwise. The image will not be parsed if a currency has already
been found in the text.
* `ignore_retweets` - Does not parse tweets which are retweets.
* `disconnect_on_first` - `true` to disconnect the stream after the first found
tweet; `false` otherwise.
* `log_tweets` - `true` to log user's tweets to a file; `false` otherwise. A new
file is created every day at midnight. Old files have the date appended to their
name.

#### Exchanges
* `priority` - A positive integer representing the priority of the exchange.
Lower numbers have higher priority. Set to `0` to disable the exchange.
* `key` -  The exchange's API key.
* `secret` - The exchange's API secret.
* `use_multiplier` - `true` to use the `multiplier` for this exchange; `false`
otherwise.
* `recvWindow` - If the order request is not processed in this amount of
miliseconds, the request is cancelled. Only used with Binance.

#### Orders
* `quote_currencies` - A dictionary of currency ticker symbols for quote
currencies (currencies with which the tweeted currency can be bought) and the
amounts to spend on the order. The order determines the priority of the
currency; the first has the highest priority. It is safe to remove unwanted
currencies from this dictionary.
* `multiplier` - The price paid for the currency is multiplied by
`1 + multiplier` to account for any price increases between the request for the
price and request for placing the order.

### Requirements
#### Binaries
* [Python 3.6](https://www.python.org/downloads/) or higher
    * Make sure the python directory and python/Scripts directory are in your
    system's `PATH` environment variable.
    * For Windows users especially,
    [Anaconda](https://www.anaconda.com/download/) is recommended over the
    standard installer from python.org.
* [Google Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
    * See [this](https://github.com/tesseract-ocr/tesseract/wiki) page for more
    specific installation instructions.
    * Make sure it is set in your system's `PATH` environment variable or the
    * `tesseract_cmd` is configured accordingly.
#### Packages
> **Note** `pipenv` can install these automatically from the provided pipfiles.

* [tweepy](http://www.tweepy.org/)
* [pytesseract](https://github.com/madmaze/pytesseract)
* [coinmarketcap](https://github.com/mrsmn/coinmarketcap)
* `OPTIONAL` [python-binance](https://github.com/sammchardy/python-binance)
    * Only required if Binance's priority is > 0 i.e. it's enabled.
* `OPTIONAL` [python-bittrex](https://github.com/ericsomdahl/python-bittrex)
    * Only required if Bittrex's priority is > 0 i.e. it's enabled.
* `OPTIONAL` [pipenv](https://docs.pipenv.org/)

### Installation
[pipenv](https://docs.pipenv.org/) can be used to simply the installation
process. Once it is installed, `cd` into the root directory and install the
dependencies from the pipfile with

```bash
pipenv install
```

An error may occur while installing python-binance on Windows. More specifically

> Failed building wheel for Twisted

The error can be circumvented by downloading a pre-built wheel of Twisted from
[here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted). Download the
32-bit or 64-bit version depending on your OS and move the file into the root
directory of the program. To install Twisted and finish the installation of
python-binance run

```bash
pipenv install twisted-wheel-file-name.whl
pipenv install
```

### Running
Run `bot.py` to run the bot. If using pipenv:

```bash
pipenv shell
cd src
python bot.py
```

otherwise

```bash
python bot.py
```
