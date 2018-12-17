from multiprocessing.connection import Listener


class Environment:

    PRICE_IDX = 4  # 종가의 위치

    def __init__(self, chart_data=None):
        self.chart_data = chart_data  # 모듈 자체가 차트 데이터를 관리(과거의 것만)
        self.observation = None  # 현재 관측치(시가 종가 거래량 등등)
        self.idx = -1  # 차트 데이터에서의 현재 위치.(최초니까 -1부터 해서 +1한 뒤 0으로 시작해 observe를 어딘가에서 루프 돌리는 것 같다.)
        self.stock_remain = 100
        self.sell_queue = []
        self.buy_queue = []
        self.order_log = []

        address = ('localhost', 6000)  # family is deduced to be 'AF_INET'
        listener = Listener(address, authkey=b'password')
        conn = listener.accept()

        print('connection accepted from', listener.last_accepted)
        while True:
            message = conn.recv()
            # do something with msg
            self.order_log.append(msg)
            msg = msg.split()

            if msg[0] == self.observe()[0]:  # 일단 같은 날짜만 취급.
                if msg[1] == 'sell':  # 파는건 무한정 팔 수 있다고 가정.
                    self.stock_remain += int(msg[2])
                    conn.send('sell done!')
                    continue

                if msg[1] == 'buy':
                    ready = self.check_remain_stock(int(msg[2]))
                    if ready == 'wait':
                        self.buy_queue.append(message)
                        continue
                    elif len(self.queue) > 0:
                        conn.send(self.check_remain_stock(int(msg[2])))
                        del self.queue[0]
                        continue
            elif msg[0] == self.observe()[0]:
                self.observe()
            elif self.idx == chart_data.shape[0]:
                conn.close()
                break
        listener.close()

    def reset(self):
        self.observation = None
        self.idx = -1

    def observe(self):  # idx를 다음위치로 이동하고 observation을 업데이트.
        if len(self.chart_data) > self.idx + 1:
            self.idx += 1
            self.observation = self.chart_data.iloc[self.idx]
            return self.observation
        return None

    def get_price(self):  # 현 observation에서 종가를 획득
        if self.observation is not None:
            return self.observation[self.PRICE_IDX]
        return None

    def set_chart_data(self, chart_data):
        self.chart_data = chart_data
    """
    def stock_matching(self, buy, sell):
        self.buy = buy
        self.sell = sell
    """
    def check_remain_stock(self, buy_order_qauntity):
        if self.stock_remain >= buy_order_qauntity:
            return buy_order_qauntity
        # elif self.stock_remain < buy_order_qauntity and len(self.queue) == 0:
        #     return 'wait'
        elif self.stock_remain < buy_order_qauntity:
            return self.stock_remain
