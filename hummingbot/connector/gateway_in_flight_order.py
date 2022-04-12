from decimal import Decimal
from typing import Optional

from hummingbot.core.data_type.common import OrderType, TradeType
from hummingbot.core.data_type.in_flight_order import InFlightOrder, OrderState


class GatewayInFlightOrder(InFlightOrder):
    def __init__(self,
                 client_order_id: str,
                 exchange_order_id: Optional[str],
                 trading_pair: str,
                 order_type: OrderType,
                 trade_type: TradeType,
                 price: Decimal,
                 amount: Decimal,
                 creation_timestamp: float,
                 gas_price: Optional[Decimal] = Decimal("0"),
                 initial_state: str = OrderState.PENDING_CREATE,
                 is_approval: bool = False):
        super().__init__(
            client_order_id=client_order_id,
            exchange_order_id=exchange_order_id,
            trading_pair=trading_pair,
            order_type=order_type,
            trade_type=trade_type,
            price=price,
            amount=amount,
            creation_timestamp=creation_timestamp,
            initial_state=initial_state if not is_approval else OrderState.PENDING_APPROVAL,
        )
        self._gas_price = gas_price
        self._nonce: int = 0
        self._cancel_tx_hash: Optional[str] = None

    @property
    def is_pending_approval(self) -> bool:
        return self.current_state in {OrderState.PENDING_APPROVAL}

    @property
    def is_approval_request(self) -> bool:
        return self.current_state in {OrderState.PENDING_APPROVAL, OrderState.APPROVED}

    @property
    def gas_price(self) -> Decimal:
        return self._gas_price

    @gas_price.setter
    def gas_price(self, gas_price: Decimal):
        self._gas_price = gas_price

    @property
    def nonce(self) -> int:
        return self._nonce

    @nonce.setter
    def nonce(self, nonce):
        self._nonce = nonce

    @property
    def cancel_tx_hash(self) -> Optional[str]:
        return self._cancel_tx_hash

    @cancel_tx_hash.setter
    def cancel_tx_hash(self, cancel_tx_hash):
        self._cancel_tx_hash = cancel_tx_hash
