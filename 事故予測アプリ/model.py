import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import joblib
from tensorflow.keras.models import load_model



# データの読み込み
data = pd.read_csv('/content/drive/My Drive/ディープラーニングアプリ/事故予測アプリ2/accident_data.csv')

# 特徴量とターゲットの分割
X = data.drop('accident', axis=1)
y = data['accident']

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
model.save('accident_model.h5')
joblib.dump(scaler, 'scaler.pkl')

def predict_accident(input_data):
    # モデルとスケーラーの読み込み
    model = load_model('accident_model.h5')
    scaler = joblib.load('scaler.pkl')

    # 入力データの標準化
    input_data_scaled = scaler.transform(input_data)

    # 予測
    prediction = model.predict(input_data_scaled)
    return prediction
