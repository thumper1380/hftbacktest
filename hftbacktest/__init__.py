from .latencies import ConstantLatency, FeedLatency
from .backtest import COL_EVENT, COL_EXCH_TIMESTAMP, COL_LOCAL_TIMESTAMP, COL_SIDE, COL_PRICE, COL_QTY,\
    DEPTH_EVENT, DEPTH_SNAPSHOT_CLEAR_EVENT, TRADE_EVENT, BUY, SELL, NONE, NEW, EXPIRED, FILLED, CANCELED, GTC, GTX, Order, \
    HftBacktest as _HftBacktest, hbt_cls_spec
from numba.experimental import jitclass

__all__ = ('COL_EVENT', 'COL_EXCH_TIMESTAMP', 'COL_LOCAL_TIMESTAMP', 'COL_SIDE', 'COL_PRICE', 'COL_QTY',
           'DEPTH_EVENT', 'TRADE_EVENT', 'DEPTH_SNAPSHOT_CLEAR_EVENT', 'BUY', 'SELL',
           'NONE', 'NEW', 'EXPIRED', 'FILLED', 'CANCELED', 'GTC', 'GTX',
           'Order', 'HftBacktest', 'FeedLatency', 'ConstantLatency')


def HftBacktest(df, tick_size, lot_size, maker_fee, taker_fee, order_latency,
                start_row=0, start_position=0, start_balance=0, start_fee=0):
    assert (df.columns[:6] == ['event', 'exch_timestamp', 'local_timestamp', 'side', 'price', 'qty']).all()
    spec = hbt_cls_spec + [('order_latency', order_latency._numba_type_)]
    hbt = jitclass(spec=spec)(_HftBacktest)
    # hbt = _HftBacktest
    return hbt(df.values, tick_size, lot_size, maker_fee, taker_fee, order_latency,
               start_row, start_position, start_balance, start_fee)
