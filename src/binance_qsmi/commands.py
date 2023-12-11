"""
# Commands
"""

import typer
from .app import BinanceQSMI

app = typer.Typer(
    name="binance-qsmi",
    add_completion=False,
    help="Binance QSMI",
)


@app.command()
def qsmi():
    """
    Start.
    """

    BinanceQSMI().run()
