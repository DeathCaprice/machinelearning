import tkinter as tk
from tkinter import messagebox
from sklearn.linear_model import LogisticRegression

# モデルの定義と訓練（サンプルデータを使用）
X = [
    [3, 1],   # チームAの得点: 3, チームBの得点: 1
    [2, 4],   # チームAの得点: 2, チームBの得点: 4
    [5, 3],   # ...
    [4, 2],
    [1, 1],
    [4, 5],
    [3, 3],
]

y = [1, 0, 1, 0, 1, 0, 0]

model = LogisticRegression()
model.fit(X, y)

# tkinterウィンドウの設定
root = tk.Tk()
root.title("野球試合勝敗予測アプリ")

# ラベルとエントリーの作成
tk.Label(root, text="チームAの得点").grid(row=0, column=0)
tk.Label(root, text="チームBの得点").grid(row=1, column=0)

entry_team_a_score = tk.Entry(root)
entry_team_a_score.grid(row=0, column=1)
entry_team_b_score = tk.Entry(root)
entry_team_b_score.grid(row=1, column=1)

# 勝敗予測ボタンのクリック時の処理
def predict_result():
    try:
        team_a_score = int(entry_team_a_score.get())
        team_b_score = int(entry_team_b_score.get())

        # 新しい試合のデータを作成
        new_data = [[team_a_score, team_b_score]]
        predicted_result = model.predict(new_data)

        # 予測結果をメッセージボックスで表示
        if predicted_result[0] == 1:
            messagebox.showinfo("勝敗予測", "チームAが勝利する確率が高いです。")
        else:
            messagebox.showinfo("勝敗予測", "チームBが勝利する確率が高いです。")

    except ValueError:
        messagebox.showerror("エラー", "数値を入力してください。")

# 予測ボタンの作成と配置
btn_predict = tk.Button(root, text="勝敗を予測する", command=predict_result)
btn_predict.grid(row=2, column=0, columnspan=2, pady=10)

# ウィンドウを開始
root.mainloop()
