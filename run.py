import logging
import os
import settings
import data_manager
from policy_learner_ant import PolicyLearner as PolicyLearnerAnt
from policy_learner_institude import PolicyLearner as PolicyLearnerInstitude
from multiprocessing import Process, Queue, Lock
from environment import Environment
import datetime
from multiprocessing.connection import Listener

init_time = datetime.datetime.now()

if __name__ == '__main__':
    stock_code = '005930'  # 삼성전자
    # stock_code = '005490'  # 포스코

    # 로그 기록
    log_dir = os.path.join(settings.BASE_DIR, 'logs/%s' % stock_code)
    timestr = settings.get_time_str()
    if not os.path.exists('logs/%s' % stock_code):
        os.makedirs('logs/%s' % stock_code)
    file_handler = logging.FileHandler(filename=os.path.join(
        log_dir, "%s_%s.log" % (stock_code, timestr)), encoding='utf-8')
    stream_handler = logging.StreamHandler()
    file_handler.setLevel(logging.DEBUG)
    stream_handler.setLevel(logging.INFO)
    logging.basicConfig(format="%(message)s",
                        handlers=[file_handler, stream_handler], level=logging.DEBUG)

    # 주식 데이터 준비
    chart_data = data_manager.load_chart_data(
        os.path.join(settings.BASE_DIR,
                     'data/chart_data/{}.csv'.format(stock_code)))
    prep_data = data_manager.preprocess(chart_data)
    training_data = data_manager.build_training_data(prep_data)

    # 기간 필터링
    training_data = training_data[(training_data['date'] >= '2017-01-01') &
                                  (training_data['date'] <= '2017-12-31')]
    training_data = training_data.dropna()

    # 차트 데이터 분리
    features_chart_data = ['date', 'open', 'high', 'low', 'close', 'volume']
    chart_data = training_data[features_chart_data]

    # 학습 데이터 분리
    features_training_data = [
        'open_lastclose_ratio', 'high_close_ratio', 'low_close_ratio',
        'close_lastclose_ratio', 'volume_lastvolume_ratio',
        'close_ma5_ratio', 'volume_ma5_ratio',
        'close_ma10_ratio', 'volume_ma10_ratio',
        'close_ma20_ratio', 'volume_ma20_ratio',
        'close_ma60_ratio', 'volume_ma60_ratio',
        'close_ma120_ratio', 'volume_ma120_ratio'
    ]
    training_data = training_data[features_training_data]

    environment = Environment(chart_data)  # singletone 환경 객체

    # 비 학습 투자 시뮬레이션 시작  # 기관
    policy_learner_institude = PolicyLearnerInstitude(stock_code=stock_code, chart_data=chart_data, environment=environment,
                                                      training_data=training_data,
                                                      min_trading_unit=1, max_trading_unit=50, delayed_reward_threshold=.05,
                                                      lr=.001)
    policy_learner_ant = PolicyLearnerAnt(stock_code=stock_code, chart_data=chart_data, environment=environment,
                                          training_data=chart_data[features_chart_data[1:]],
                                          min_trading_unit=1, max_trading_unit=10, delayed_reward_threshold=.02,
                                          lr=.0001)

    lock = Lock()
    model_ver = '20181217033712'  # institude 학습
    model_path=os.path.join(settings.BASE_DIR, 'models/{}/model_{}.h5'.format(stock_code, model_ver))
    Process(target=policy_learner_institude.trade, args=(1000000000,  # 십억
                                                         model_path))
    model_ver = '20181217032705'  # ant 학습
    model_path=os.path.join(settings.BASE_DIR, 'models/{}/model_{}.h5'.format(stock_code, model_ver))
    Process(target=policy_learner_ant.trade, args=(10000000,  # 천만
                                                   model_path))


finish_time = datetime.datetime.now()
print("start   : ", init_time.strftime("%Y-%m-%d-%Hh-%Mm"))
print("finish  : ", finish_time.strftime("%Y-%m-%d-%Hh-%Mm"))
print("Total Running Time : {}".format(finish_time - init_time))
"""
# 강화학습 시작 # 개미.
policy_learner = PolicyLearnerCustom(
    stock_code=stock_code, chart_data=chart_data, training_data=training_data,
    min_trading_unit=1, max_trading_unit=10, delayed_reward_threshold=.2, lr=.001)
policy_learner.fit(balance=10000000, num_epoches=10,
                   discount_factor=0, start_epsilon=.5)
"""
