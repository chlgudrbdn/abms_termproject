import numpy as np
from keras.models import Sequential
from keras.layers import Activation, Dropout, CuDNNLSTM, LSTM, Dense, BatchNormalization
from keras.optimizers import sgd
# 케라스에선 만약 적절한 Nvidia GPU의 CuDNN지원 텐서플로우 상에서 돌아갈 경우엔 LSTM 대신에 CuDNNLSTM로 바꿔 쓰면 더 성능향상이 있다고 합니다.
# https://keras.io/layers/recurrent/#cudnnlstm 실제로도 GTX 1060 6GB로 돌려봤는데 그럭저럭 차이가 납니다. LSTM이 72분이라면 CuDNNLSTM은 62분정도인데,
# LSTM의 하이퍼 파라미터와 구조가 어떤 근거로 만들어 졌는지 몰라서 맞는 수정안인지 모르겠지만, LSTM의 Dropout을 별도로 빼서 레이어로 만든 것 외엔 별다른 구조가 차이가 없는데도 이정도입니다.
# 저자님 께서는 이 이슈를 확인해 git hub나 개정판 같은걸 낼 때 GPU 관련 파트에 적어두면 좋을 것 같습니다.

class PolicyNetwork:
    def __init__(self, input_dim=0, output_dim=0, lr=0.01):
        self.input_dim = input_dim
        self.lr = lr
        dropout_rate = 0.5
        # LSTM 신경망
        self.model = Sequential()
        """
        self.model.add(LSTM(256, input_shape=(1, input_dim),
                            return_sequences=True, stateful=False, dropout=0.5))
        self.model.add(BatchNormalization())
        self.model.add(LSTM(256, return_sequences=True, stateful=False, dropout=0.5))
        self.model.add(BatchNormalization())
        self.model.add(LSTM(256, return_sequences=False, stateful=False, dropout=0.5))
        self.model.add(BatchNormalization())
        self.model.add(Dense(output_dim))
        self.model.add(Activation('sigmoid'))
        """
        self.model.add(CuDNNLSTM(128, input_shape=(1, input_dim),
                            return_sequences=True, stateful=False))
        self.model.add(Dropout(dropout_rate))
        self.model.add(BatchNormalization())
        self.model.add(Dense(output_dim))
        self.model.add(Activation('sigmoid'))

        self.model.compile(optimizer=sgd(lr=lr), loss='mse')
        self.prob = None

    def reset(self):
        self.prob = None

    def predict(self, sample):
        self.prob = self.model.predict(np.array(sample).reshape((1, -1, self.input_dim)))[0]  # 학습데이터+에이전트상태=17차원 # 2차원으로 바꿔야케라스 입력형식에 맞기 때문.
        return self.prob

    def train_on_batch(self, x, y):
        return self.model.train_on_batch(x, y)  # 입력으로 들어온 학습 데이터 집합 x, 레이블 y로 정책 신경망을 학습시킨다.
# train_on_batch는 입력으로 들어온 학습 데이터의 집합(1개 배치)로 신경망을 한번 학습.
    def save_model(self, model_path):
        if model_path is not None and self.model is not None:
            self.model.save_weights(model_path, overwrite=True)  # hdf5로 저장.

    def load_model(self, model_path):
        if model_path is not None:
            self.model.load_weights(model_path)