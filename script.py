from abc import ABC, abstractmethod
from typing import Any

from google_play_scraper import search
from google_play_scraper import app as app_details


class AbstractFunc(ABC):
    """ Abstract class for features """

    @staticmethod
    @abstractmethod
    def get_name() -> str:
        """ Returns name of the feature """
        pass

    @staticmethod
    @abstractmethod
    def exec() -> Any:
        """ Executes further commands"""
        pass


class RankCheckerFunc(AbstractFunc):

    @staticmethod
    def get_name() -> str:
        return 'Rank Checker'

    @staticmethod
    def exec() -> Any:
        """ Shows application position. """

        search_query = input('Enter search query: ')
        target_app_id = input('Your app package name: ')
        print('Enter country code. For example: us')

        country = input('Country code: ')

        result: dict = search(
            query=search_query,
            lang="en",
            country=country,
            n_hits=30
        )

        count = 0
        for app in result:
            count += 1

            app_id = app['appId']

            if app_id == target_app_id:
                print(f'Your app is ranked in {count} position in {country.upper()}')
                return

        print(f'Not ranked in {country} in top 30')


class AppDetailsFunc(AbstractFunc):
    @staticmethod
    def get_name() -> str:
        return 'App details'

    @staticmethod
    def exec() -> Any:
        """ Shows app details. Package name is required. """

        target_app_id = input('Your app package name: ')

        result = app_details(
            app_id=target_app_id,
            lang='en',
            country='us'
        )

        for key, value in result.items():
            print(f'{key}:', value)


class FeaturesFunc:
    @staticmethod
    def get_features() -> dict:
        """ Returns all available commands """

        cmd_options = {
            '1': RankCheckerFunc,
            '2': AppDetailsFunc
        }

        return cmd_options


def input_command():
    """ Listen for new command """

    print("Please choose any of the option")

    for option, func in FeaturesFunc.get_features().items():
        print(option, func.get_name())

    cmd = input("\nSelect: ")

    try:
        # Get class of currently selcted feature
        selected: AbstractFunc = FeaturesFunc.get_features()[cmd]
        print(f'{selected.get_name()} is selected\n')

        # Remaining new task will be handled by selcted class
        selected.exec()

    except KeyError:
        print('Invalid command')


# ask user for command
input_command()
