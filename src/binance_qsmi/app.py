"""
Main module for binance_qsmi.
"""

import os
import re
from typing import Optional, Dict, Any

import typer
from binance import Client
import prettytable

from . import models


class BinanceQSMI:
    """
    Main class for binance_qsmi.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """

        self.client = self.login()

    def _get_proxy(self) -> Optional[Dict[str, Any]]:
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
                typer.echo("Invalid proxy")
                raise typer.Exit()

            regex = r"^(http|https|socks)://([^:@]+):([^:@]+)@((?:\d{1,3}\.){3}\d{1,3}|(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4})\:(\d+)$"

            if not re.match(regex, proxy):
                typer.echo("Invalid proxy")
                raise typer.Exit()

            return {kind: proxy}

        confirmation = typer.confirm("Are you sure?", default=False)
        if confirmation:
            return None
        return self._get_proxy()

    def login(self) -> Client:
        """
        Login.

        Returns:
            Client: Binance client.
        """

        api_key: str = typer.prompt("Enter your API key", hide_input=True, type=str)
        api_secret: str = typer.prompt("Enter your API secret", hide_input=True, type=str)
        proxy = self._get_proxy()

        requests_params = None
        if proxy:
            requests_params = {"proxies": proxy}

        return Client(api_key=api_key, api_secret=api_secret, requests_params=requests_params)

    def is_login(self) -> bool:
        """
        Check if user is login or not

        Returns:
            bool: True if user is login, False otherwise.
        """

        return self.client is not None

    @property
    def menu_items(self) -> list:
        """
        Menu items.

        Returns:
            list: Menu items.
        """

        return [
            "Get margin account trades",
            "Get margin balances",
        ]

    @staticmethod
    def divider(char: str = "*") -> None:
        """
        Print a divider.

        Args:
            char (str, optional): Character to use. Defaults to "*".

        Returns:
            None
        """

        try:
            width = os.get_terminal_size().columns
        except Exception:  # pylint: disable=broad-except
            width = 100

        typer.echo()
        typer.echo(char * width)
        typer.echo()

    @property
    def table_menu(self) -> prettytable.PrettyTable:
        """
        Table menu.

        Returns:
            prettytable.PrettyTable: Table menu.
        """

        table = prettytable.PrettyTable()
        table.field_names = ["Option", "Description"]
        for index, item in enumerate(self.menu_items):
            table.add_row([index + 1, item])
        table.add_row([0, "Exit"])
        return table

    def get_option(self) -> int:
        """
        Prompt the user for an option.

        Returns:
            int: Option.
        """

        typer.echo(self.table_menu)
        option = typer.prompt("Enter an option", type=int)
        typer.echo()
        return option

    def get_margin_trades(self) -> None:
        """
        Get margin trades.

        Returns:
            None
        """

        typer.clear()
        typer.echo("Margin trades:")
        symbol = typer.prompt("Enter symbol", type=str)
        full = typer.prompt("Return full data for each trade? [Y/n]", show_choices=True, default="n", type=bool)

        result = self.client.get_margin_trades(symbol=symbol)

        table = models.MarginTrades(trades=result).table(full=full)

        typer.echo(table)

    def get_margin_balances(self) -> None:
        """
        Get margin balances.

        Returns:
            None
        """

        typer.clear()
        typer.echo("Margin balance:")
        include_zero = typer.prompt("Include zero balances? [Y/n]", show_choices=True, default="n", type=bool)

        result = self.client.get_margin_account()

        table = models.MarginAccountInfo(**result).user_assets_table(include_zero)

        typer.echo(table)

    def process(self, option: int) -> None:
        """
        Process the option.

        Args:
            option (int): Option.

        Returns:
            None
        """

        if option == 1:
            self.get_margin_trades()
        elif option == 2:
            self.get_margin_balances()
        else:
            typer.echo("Invalid option")

    def main(self) -> None:
        """
        Main method.

        Returns:
            None
        """

        option = self.get_option()

        while option != 0:
            try:
                self.process(option)
            except Exception as e:  # pylint: disable=broad-except
                typer.echo(f"Error: {e}")

            self.divider()

            option = self.get_option()

    def start(self) -> None:
        """
        Start the application.

        Returns:
            None
        """

        self.main()

    def run(self) -> None:
        """
        Run the application.

        Returns:
            None

        Raises:
            SystemExit: If the user press Ctrl+C.
            KeyboardInterrupt: If the user press Ctrl+C.
        """

        try:
            typer.run(self.start)
        except (KeyboardInterrupt, SystemExit) as exc:
            typer.echo("\nGoodbye!")
            raise SystemExit() from exc


if __name__ == "__main__":
    BinanceQSMI().run()
