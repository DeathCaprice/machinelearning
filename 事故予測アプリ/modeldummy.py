import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import joblib
from tensorflow.keras.models import load_model

# ダミーデータの生成
np.random.seed(42)
data = {
    'feature1': np.random.rand(100) * 200,  # 車両の速度 (0 - 200 km/h)
    'feature2': np.random.rand(100) * 1000,  # 距離 (0 - 1000 km)
    'feature3': np.random.rand(100) * 50 - 10,  # 気温 (-10 - 40°C)
    'feature4': np.random.randint(0, 3, 100),  # 路面状況 (0: 良好, 1: 濡れている, 2: 凍結)
    'accident': np.random.randint(0, 2, 100)  # 事故 (0: なし, 1: あり)
}

df = pd.DataFrame(data)

# 特徴量とターゲットの分割
X = df.drop('accident', axis=1)
y = df['accident']

# データの標準化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 訓練データとテストデータに分割
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# モデルの構築
model = Sequential()
model.add(Dense(64, input_dim=X_train.shape[1], activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# モデルのコンパイル
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# モデルの訓練
model.fit(X_train, y_train, epochs=50, batch_size=10, validation_data=(X_test, y_test))

# モデルとスケーラーの保存
model.save('/content/drive/My Drive/ディープラーニングアプリ/事故予測アプリ2/accident_model.h5')
joblib.dump(scaler, '/content/drive/My Drive/ディープラーニングアプリ/事故予測アプリ2/scaler.pkl')

# モデルとスケーラーのロードとコンパイルを一度だけ行う
model = load_model('/content/drive/My Drive/ディープラーニングアプリ/事故予測アプリ2/accident_model.h5')
scaler = joblib.load('/content/drive/My Drive/ディープラーニングアプリ/事故予測アプリ2/scaler.pkl')
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

def predict_accident(input_data):
    # 入力データの標準化
    input_data_scaled = scaler.transform(input_data)

    # 予測
    prediction = model.predict(input_data_scaled)
    return prediction
