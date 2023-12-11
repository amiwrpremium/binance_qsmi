"""
Main module for binance_qsmi.
"""

import os
import re
import typer
from binance import Client
import prettytable

from . import models


class BinanceQSMI:
    def __init__(self):
        self.client = None

    def _get_proxy(self):
        is_needed = typer.confirm("Do you need proxy?", default=True)

        if is_needed:
            proxy = typer.prompt('Enter proxy in format "http(s)://user:pass@host:port"', type=str)
            if "https" in proxy:
                kind = "https"
            elif "http" in proxy:
                kind = "http"
            elif "socks" in proxy:
                kind = "socks5"
            else:
                typer.echo("Invalid proxy", color=typer.colors.RED)
                raise typer.Exit()

            regex = "^(http|https|socks)://([^:@]+):([^:@]+)@((?:\d{1,3}\.){3}\d{1,3}|(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4})\:(\d+)$"

            if not re.match(regex, proxy):
                typer.echo("Invalid proxy", color=typer.colors.RED)
                raise typer.Exit()

            return {kind: proxy}

        else:
            confirmation = typer.confirm("Are you sure?", default=False)
            if confirmation:
                return None
            else:
                return self._get_proxy()

    def login(self):
        api_key: str = typer.prompt("Enter your API key", hide_input=True, type=str)
        api_secret: str = typer.prompt("Enter your API secret", hide_input=True, type=str)
        proxy = self._get_proxy()

        requests_params = None
        if proxy:
            requests_params = {"proxies": proxy}

        self.client = Client(api_key=api_key, api_secret=api_secret, requests_params=requests_params)

        return self.client

    def is_login(self):
        """
        Check if user is login or not

        Returns:
            bool: True if user is login, False otherwise.
        """

        return self.client is not None

    @property
    def menu_items(self) -> list:
        return [
            "Get margin account trades",
            "Get margin balances",
        ]

    @property
    def title(self) -> str:
        return ascii.BINANCE_QSMI

    @property
    def menu(self) -> str:
        menu = self.title
        menu += "Select an option:\n"
        for index, item in enumerate(self.menu_items):
            menu += f"{index + 1}. {item}\n"
        menu += "\n"
        menu += "0. Exit\n\n"
        return menu

    @staticmethod
    def divider(char: str = "*") -> None:
        try:
            width = os.get_terminal_size().columns
        except Exception:  # pylint: disable=broad-except
            width = 100

        typer.echo()
        typer.echo(char * width, color=typer.colors.CYAN)
        typer.echo()

    @property
    def table_menu(self) -> prettytable.PrettyTable:
        table = prettytable.PrettyTable()
        table.field_names = ["Option", "Description"]
        for index, item in enumerate(self.menu_items):
            table.add_row([index + 1, item])
        table.add_row([0, "Exit"])
        return table

    def get_option(self) -> int:
        typer.echo(self.table_menu)
        option = typer.prompt("Enter an option", type=int)
        typer.echo()
        return option

    def get_margin_trades(self):
        typer.clear()
        typer.echo(f"Margin trades:")
        symbol = typer.prompt("Enter symbol", type=str)
        full = typer.prompt("Return full data for each trade? [Y/n]", show_choices=True, default="n", type=bool)

        result = self.client.get_margin_trades(symbol=symbol)

        table = models.MarginTrades(trades=result).table(full=full)
        print(table)

    def get_margin_balances(self):
        typer.clear()
        typer.echo(f"Margin balance:")
        include_zero = typer.prompt("Include zero balances? [Y/n]", show_choices=True, default="n", type=bool)

        result = self.client.get_margin_account()

        table = models.MarginAccountInfo(**result).user_assets_table(include_zero)
        print(table)

    def process(self, option: int):
        if option == 1:
            typer.echo(self.get_margin_trades())
        elif option == 2:
            typer.echo(self.get_margin_balances())
        else:
            typer.echo("Invalid option")

    def main(self):
        option = self.get_option()

        while option != 0:
            try:
                self.process(option)
            except Exception as e:
                typer.echo(f"Error: {e}", color=typer.colors.RED)

            self.divider()

            option = self.get_option()

    def start(self):
        self.login()
        self.main()

    def run(self):
        try:
            typer.run(self.start)
        except KeyboardInterrupt:
            typer.echo("\nGoodbye!", color=typer.colors.RED)
            raise SystemExit()


if __name__ == "__main__":
    BinanceQSMI().run()
