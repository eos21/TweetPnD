import logging

import tweepy
from bittrex import Bittrex

class StreamListener(tweepy.StreamListener):
    config: dict = {}
    bittrex: Bittrex = None
    log: logging.Logger = None

    def __init__(self, cfg, logger, user, callback = None):
        global config
        global bittrex
        global log
        config = cfg
        bittrex = Bittrex(config["bittrex"]["key"],
                          config["bittrex"]["secret"],
                          api_version = "v2.0")
        log = logger

        super(StreamListener, self).__init__()

        self.user = user
        self.currencies = bittrex.get_currencies()
        self.callback = callback

        if not self.currencies["success"]:
            raise RuntimeError("The currencies could not be retrieved from "
                               "Bittrex.")

        self.currencies = self.currencies["result"]

    def on_status(self, status):
        # log.info(f"{status.author.screen_name} tweeted | {status.text}")

        # Only parses statuses by the author; ignores retweets, replies, etc.
        if status.author.id == self.user:
            log.info(f"User tweeted | {status.text}")

            # Finds the first currency whose long name is found in the text of
            # the status. None if no match is found.
            currency = next((currency for currency in self.currencies
                             if currency["CurrencyLong"] in status.text or
                             currency["Currency"] in status.text),
                            None)

            # Prints the name of currency market if one was found.
            if currency:
                self.callback(currency)

    def on_error(self, status_code):
        if status_code == 420:
            # TODO: Handle rate limiting properly instead of closing the stream.
            log.error("The stream has closed due to rate limiting.")
            return False

        log.error(f"The stream encountered an error with code {status_code}")
        return True

    def on_timeout(self):
        print("Stream timed out.")
        log.warning("The stream timed out.")
        return True
