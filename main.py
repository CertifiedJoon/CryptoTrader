# 일부러 영어로 다큐멘테이션 작성했습니다.

# Think about what are the initializers.
# We are creating a trading algorithm that does:
#   1. Trade A stock given its ticker, stoploss, profit taking level
#   2. Dynamically add strategies
#   3. Trade using one strategy or composition of two or more strategies.
#   4. 요약: 주식 거래를 프로그램이 자동으로 and 실시간으로 전략을 바꿔가면서 자동거래하는 프로그램.
#   5. Strategy files are grouped in Strategy folder
#   6. User Notification is done in Notifier folder
#   7. Fetching information from stock API is done in Trader folder
#   8. Trading is done in Trade.py\\

import Trade as trd
client = trd.Trade()
client.trade()