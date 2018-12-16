class Environment:

    PRICE_IDX = 4  # 종가의 위치

    def __init__(self, chart_data=None):
        self.chart_data = chart_data  # 모듈 자체가 차트 데이터를 관리(과거의 것만)
        self.observation = None  # 현재 관측치(시가 종가 거래량 등등)
        self.idx = -1  # 차트 데이터에서의 현재 위치.(최초니까 -1부터 해서 +1한 뒤 0으로 시작해 observe를 어딘가에서 루프 돌리는 것 같다.)
        self.demand = 0
        self.supply = 0

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

    def stock_matching(self, demand, ):
        self.demand = 0
        self.supply = 0