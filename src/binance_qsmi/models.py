"""
# Name: models.py
# Description:
#   - This file contains the models for the Binance QSMI Module.
#   - These models are used to convert the data from the Binance API
#     into the data that is used by the core module.
"""

from typing import List
from pydantic import Field, BaseModel
from prettytable import PrettyTable


class UserAsset(BaseModel):
    """
    Binance Margin User Asset Base Model
    """

    asset: str = Field(
        ...,
        title="Asset",
        description="Asset",
        examples=["BTC"],
    )

    borrowed: float = Field(
        ...,
        title="Borrowed",
        description="Borrowed",
        examples=[0.00000000],
    )

    free: float = Field(
        ...,
        title="Free",
        description="Free amount",
        examples=[0.00000000],
    )

    interest: float = Field(
        ...,
        title="Interest",
        description="Interest",
        examples=[0.00000000],
    )

    locked: float = Field(
        ...,
        title="Locked",
        description="Locked amount",
        examples=[0.00000000],
    )

    net_asset: float = Field(
        ...,
        title="Net Asset",
        description="Net Asset",
        examples=[0.00000000],
        alias="netAsset",
    )

    def table(self) -> PrettyTable:
        """
        PrettyTable for UserAsset
        """

        table = PrettyTable()
        table.field_names = ["Asset", "Borrowed", "Free", "Interest", "Locked", "Net Asset"]
        table.add_row(
            [
                self.asset,
                self.borrowed,
                self.free,
                self.interest,
                self.locked,
                self.net_asset,
            ]
        )
        return table


class MarginAccountInfo(BaseModel):
    """
    Binance Margin Account Info Base Model
    """

    borrow_enabled: bool = Field(
        ...,
        title="Borrow Enabled",
        description="Borrow Enabled",
        examples=[True, False],
        alias="borrowEnabled",
    )

    margin_level: float = Field(
        ...,
        title="Margin Level",
        description="Margin Level",
        examples=[11.64405625, 0.91232],
        alias="marginLevel",
    )

    total_asset_of_btc: float = Field(
        ...,
        title="Total Asset of BTC",
        description="Total Asset of BTC",
        examples=[6.82728457, 0.00000000],
        alias="totalAssetOfBtc",
    )

    total_liability_of_btc: float = Field(
        ...,
        title="Total Liability of BTC",
        description="Total Liability of BTC",
        examples=[0.58633215, 0.00000000],
        alias="totalLiabilityOfBtc",
    )

    total_net_asset_of_btc: float = Field(
        ...,
        title="Total Net Asset of BTC",
        description="Total Net Asset of BTC",
        examples=[6.24095242, 0.00000000],
        alias="totalNetAssetOfBtc",
    )

    trade_enabled: bool = Field(
        ...,
        title="Trade Enabled",
        description="Trade Enabled",
        examples=[True, False],
        alias="tradeEnabled",
    )

    transfer_enabled: bool = Field(
        ...,
        title="Transfer Enabled",
        description="Transfer Enabled",
        examples=[True, False],
        alias="transferEnabled",
    )

    user_assets: List[UserAsset] = Field(
        ...,
        title="User Assets",
        description="User Assets",
        examples=[
            [
                {
                    "asset": "BTC",
                    "borrowed": "0.00000000",
                    "free": "0.00499500",
                    "interest": "0.00000000",
                    "locked": "0.00000000",
                    "netAsset": "0.00499500",
                },
                {
                    "asset": "BNB",
                    "borrowed": "201.66666672",
                    "free": "2346.50000000",
                    "interest": "0.00000000",
                    "locked": "0.00000000",
                    "netAsset": "2144.83333328",
                },
            ]
        ],
        alias="userAssets",
    )

    def table(self) -> PrettyTable:
        """
        PrettyTable for Balances.

        Returns:
            PrettyTable: PrettyTable for Balances.
        """

        table = PrettyTable()
        table.field_names = [
            "Borrow Enabled",
            "Margin Level",
            "Total Asset of BTC",
            "Total Liability of BTC",
            "Total Net Asset of BTC",
            "Trade Enabled",
            "Transfer Enabled",
            "User Assets",
        ]
        table.add_row(
            [
                self.borrow_enabled,
                self.margin_level,
                self.total_asset_of_btc,
                self.total_liability_of_btc,
                self.total_net_asset_of_btc,
                self.trade_enabled,
                self.transfer_enabled,
                self.user_assets,
            ]
        )
        return table

    def get_asset(self, asset: str) -> UserAsset:
        """
        Get UserAsset by asset.

        Args:
            asset (str): Asset.

        Returns:
            UserAsset: UserAsset.

        Raises:
            ValueError: If asset is not found.
        """

        for user_asset in self.user_assets:
            if user_asset.asset == asset:
                return user_asset

        raise ValueError(f"Asset {asset} not found")

    def user_assets_table(self, include_zero: bool = False) -> PrettyTable:
        """
        PrettyTable for UserAssets.

        Returns:
            PrettyTable: PrettyTable for UserAssets.
        """

        table = PrettyTable()
        table.field_names = self.user_assets[0].table().field_names
        for user_asset in self.user_assets:
            if user_asset.free > 0 or user_asset.borrowed > 0 or user_asset.locked > 0 or include_zero:
                table.add_row(user_asset.model_dump().values())
        return table


class MarginTrade(BaseModel):
    """
    Binance Margin Trade Base Model
    """

    symbol: str = Field(
        ...,
        title="Symbol",
        description="Symbol",
        examples=["BTCUSDT", "ETHUSDT"],
    )

    id: int = Field(
        ...,
        title="Id",
        description="Id",
        examples=[3307212199, 3307212199],
    )

    order_id: int = Field(
        ...,
        title="Order Id",
        description="Order Id",
        examples=[23573313851, 23573313851],
        alias="orderId",
    )

    price: float = Field(
        ...,
        title="Price",
        description="Price",
        examples=[41830, 41830],
    )

    quantity: float = Field(
        ...,
        title="Quantity",
        description="Quantity",
        examples=[0.00041, 0.00041],
        alias="qty",
    )

    quote_quantity: float = Field(
        ...,
        title="Quote Quantity",
        description="Quote Quantity",
        examples=[17.1503, 17.1503],
        alias="quoteQty",
    )

    commission: float = Field(
        ...,
        title="Commission",
        description="Commission",
        examples=[0.0171503, 0.0171503],
    )

    commission_asset: str = Field(
        ...,
        title="Commission Asset",
        description="Commission Asset",
        examples=["USDT", "USDT"],
        alias="commissionAsset",
    )

    time: int = Field(
        ...,
        title="Time",
        description="Time",
        examples=[1701779991682, 1701779991682],
    )

    is_buyer: bool = Field(
        ...,
        title="Is Buyer",
        description="Is Buyer",
        examples=[False, False],
        alias="isBuyer",
    )

    is_maker: bool = Field(
        ...,
        title="Is Maker",
        description="Is Maker",
        examples=[False, False],
        alias="isMaker",
    )

    is_best_match: bool = Field(
        ...,
        title="Is Best Match",
        description="Is Best Match",
        examples=[True, True],
        alias="isBestMatch",
    )

    is_isolated: bool = Field(
        ...,
        title="Is Isolated",
        description="Is Isolated",
        examples=[False, False],
        alias="isIsolated",
    )

    def table(self, full: bool = False) -> PrettyTable:
        """
        PrettyTable for MarginTrade.

        Returns:
            PrettyTable: PrettyTable for MarginTrade.
        """

        table = PrettyTable()

        fields = [
            "Symbol",
            "Id",
            "Order Id",
            "Price",
            "Quantity",
            "Quote Quantity",
            "Commission",
            "Commission Asset",
            "Time",
        ]
        data = [
                self.symbol,
                self.id,
                self.order_id,
                self.price,
                self.quantity,
                self.quote_quantity,
                self.commission,
                self.commission_asset,
                self.time,
            ]

        if full:
            fields.extend(
                [
                    "Is Buyer",
                    "Is Maker",
                    "Is Best Match",
                    "Is Isolated",
                ]
            )
            data.extend(
                [
                    self.is_buyer,
                    self.is_maker,
                    self.is_best_match,
                    self.is_isolated,
                ]
            )

        table.field_names = fields
        table.add_row(data)
        return table


class MarginTrades(BaseModel):
    """
    Binance Margin Trades Base Model
    """

    trades: List[MarginTrade] = Field(
        ...,
        title="Trades",
        description="Trades",
    )

    def table(self, full: bool = False) -> PrettyTable:
        """
        PrettyTable for MarginTrades.

        Returns:
            PrettyTable: PrettyTable for MarginTrades.
        """

        print(f"FULL: {full}")

        table = PrettyTable()
        table.field_names = self.trades[0].table(full).field_names
        for trade in self.trades:
            table.add_row(trade.model_dump().values())
        return table
