import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 仮想の試合データ
data = {
    'Player': ['Player A', 'Player B', 'Player C', 'Player D', 'Player E', 
               'Player F', 'Player G', 'Player H', 'Player I'],
    'Batting_Average': [0.320, 0.290, 0.310, 0.270, 0.280, 0.300, 0.260, 0.290, 0.280],
    'Home_Runs': [20, 15, 18, 12, 10, 22, 8, 11, 9],
    'Runs_Batted_In': [80, 70, 75, 60, 55, 85, 50, 65, 58],
    'Position': ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
    'Batting_Order': [1, 2, 3, 4, 5, 6, 7, 8, 9]
}

df = pd.DataFrame(data)

# 特徴量
X = df[['Batting_Average', 'Home_Runs', 'Runs_Batted_In']]

# ターゲット（打順）
y = df['Batting_Order']

# モデルの訓練
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# 訓練データでの精度
y_pred_train = model.predict(X)
accuracy_train = accuracy_score(y, y_pred_train)
print(f"Training Accuracy: {accuracy_train}")

def predict_batting_order():
    # 入力値の取得
    avg = float(entry_avg.get())
    hr = int(entry_hr.get())
    rbi = int(entry_rbi.get())
    
    # 予測するために入力値をデータフレームに変換し、カラム名を指定
    input_data = pd.DataFrame([[avg, hr, rbi]], columns=['Batting_Average', 'Home_Runs', 'Runs_Batted_In'])
    
    # 打順の予測
    predicted_order = model.predict(input_data)
    
    # 結果を表示
    result_label.config(text=f"Predicted Batting Order: {predicted_order[0]}")

# tkinterウィンドウの作成
root = tk.Tk()
root.title("Baseball Batting Order Predictor")

# 入力フレーム
input_frame = ttk.Frame(root, padding="20")
input_frame.grid(row=0, column=0)

# ラベルとエントリー
ttk.Label(input_frame, text="打率:").grid(row=0, column=0, padx=5, pady=5)
entry_avg = ttk.Entry(input_frame, width=10)
entry_avg.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="本塁打数:").grid(row=1, column=0, padx=5, pady=5)
entry_hr = ttk.Entry(input_frame, width=10)
entry_hr.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="打点:").grid(row=2, column=0, padx=5, pady=5)
entry_rbi = ttk.Entry(input_frame, width=10)
entry_rbi.grid(row=2, column=1, padx=5, pady=5)

# 予測ボタン
predict_button = ttk.Button(input_frame, text="予測する", command=predict_batting_order)
predict_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

# 結果ラベル
result_label = ttk.Label(input_frame, text="")
result_label.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

# tkinterウィンドウの実行
root.mainloop()
