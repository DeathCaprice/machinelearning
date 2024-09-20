import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import tkinter as tk
from tkinter import messagebox, StringVar

# ダミーデータの作成
# バッターのデータ
X_batting_team1 = np.array([
    [0.298,  8, 0.320],
    [0.278,  6, 0.314],
    [0.310, 12, 0.322],
    [0.325, 25, 0.333],
    [0.302, 18, 0.317],
    [0.279, 13, 0.297],
    [0.260,  9, 0.279],
    [0.229,  6, 0.285],
    [0.025,  0, 0.115],
])

X_batting_team2 = np.array([
    [0.320,  4, 0.340],
    [0.273,  3, 0.329],
    [0.345,  8, 0.362],
    [0.327, 18, 0.355],
    [0.322, 19, 0.395],
    [0.289,  9, 0.297],
    [0.263,  7, 0.299],
    [0.239,  3, 0.285],
    [0.021,  0, 0.129],
])

# ピッチャーのデータ
X_pitching_team1 = np.array([
    [2.90, 170],
])

X_pitching_team2 = np.array([
    [2.56, 80],
])

# チームのデータを結合
X_team1 = np.hstack((X_batting_team1, np.repeat(X_pitching_team1, X_batting_team1.shape[0], axis=0)))
X_team2 = np.hstack((X_batting_team2, np.repeat(X_pitching_team2, X_batting_team2.shape[0], axis=0)))

# ラベルの作成 (勝ち: 1, 負け: 0)
# ここではチーム1を勝ち、チーム2を負けと仮定
y_team1 = np.ones(X_team1.shape[0])
y_team2 = np.zeros(X_team2.shape[0])

# データの結合
X = np.vstack((X_team1, X_team2))
y = np.hstack((y_team1, y_team2))

# データの分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# モデルの訓練
model = RandomForestClassifier()
model.fit(X_train, y_train)

def predict():
    try:
        
        # 対戦チーム名のチェック
        opponent_team_name = entry2.get()
        if not opponent_team_name:
            messagebox.showerror("入力エラー", "対戦チーム名を入力してください")
            return
        # 入力されたデータを取得
        batting_team1 = []
        for row_entries in entries_team1:
            batting_team1.append([float(entry.get()) for entry in row_entries[-3:]])

        batting_team2 = []
        for row_entries in entries_team2:
            batting_team2.append([float(entry.get()) for entry in row_entries[-3:]])

        # バッティング成績の平均を計算
        X_batting_avg_team1 = np.mean(batting_team1, axis=0)
        X_batting_avg_team2 = np.mean(batting_team2, axis=0)

        # ピッチャーのデータを取得
        pitching_team1 = [
            float(pitcher_entries[1].get()),
            int(pitcher_entries[2].get())
        ]
        pitching_team2 = [
            float(pitcher_entries[4].get()),
            int(pitcher_entries[5].get())
        ]

        # チームのデータを結合
        X_team1 = np.hstack((X_batting_avg_team1, pitching_team1))
        X_team2 = np.hstack((X_batting_avg_team2, pitching_team2))

        # 予測
        prediction_team1 = model.predict([X_team1])[0]
        prediction_team2 = model.predict([X_team2])[0]

        # 対戦チーム名を取得
        opponent_team_name = entry2.get()

        # 結果表示
        if prediction_team1 == prediction_team2:
            result = "引き分け"
        else:
            result_team1 = "勝ち" if prediction_team1 == 1 else "負け"
            result_team2 = "勝ち" if prediction_team2 == 1 else "負け"
            result = f"群馬ニューフェニックスは{result_team1}\n{opponent_team_name}は{result_team2}"

        messagebox.showinfo("予測結果", result)

    except ValueError as e:
        messagebox.showerror("入力エラー", f"全てのフィールドに正しい数値を入力してください。\nエラー: {str(e)}")


# GUIの設定
root = tk.Tk()
root.title("野球試合推測アプリ")
root.minsize(920, 800)


# ホームチーム情報
# チーム名(ホームチームテキスト表示)
label_team1 = tk.Label(text="チーム名　群馬ニューフェニックス")
label_team1.place(x=10, y=20)

# 打撃成績入力(ホームチーム用テキスト)
label_batting1 = tk.Label(text="打撃成績を入力してください")
label_batting1.place(x=10, y=50)

# 打撃項目と選手名(テキスト)
label_headers = ["打順", "守備", "選手名", "背番号", "打率", "本塁打", "出塁率"]
header_positions = [10, 48, 118, 206, 277, 334, 396]

for i, text in enumerate(label_headers):
    label = tk.Label(text=text)
    label.place(x=header_positions[i], y=75)
    
# 守備の選択肢
positions = ["投", "捕", "一", "二", "三", "遊", "左", "中", "右"]

#選手名の選択肢
player_name=["白鳥","国田","岡元","金田","藤本大","岡島","余田","新家","高橋駿","高橋博"]

#背番号の選択肢
uniform_number = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]

# 各打順の入力欄を表示
entries_team1 = []

for i in range(9):  # 入力欄を9行に増やす
    y_position = 95 + (i * 30)
    # ホームチームの打撃成績入力欄
    row_entries_team1 = []

    #打順
    label = tk.Label(text=str(i + 1))
    label.place(x=15, y=y_position)
    #守備
    var_team1 = StringVar(root)
    var_team1.set(positions[0])
    dropdown_team1 = tk.OptionMenu(root, var_team1, *positions)
    dropdown_team1.place(x=48, y=y_position)
    row_entries_team1.append(var_team1)
    #選手名
    var_team1 = StringVar(root)
    var_team1.set(player_name[0])
    dropdown_team1 = tk.OptionMenu(root, var_team1, *player_name)
    dropdown_team1.place(x=120, y=y_position)
    row_entries_team1.append(var_team1)

    #背番号
    var_team1 = StringVar(root)
    var_team1.set(uniform_number[0])
    dropdown_team1 = tk.OptionMenu(root, var_team1, *uniform_number)
    dropdown_team1.place(x=206, y=y_position)
    row_entries_team1.append(var_team1)

    #打率
    entry = tk.Entry(width=6)
    entry.place(x=277, y=y_position)
    row_entries_team1.append(entry)

    #本塁打
    entry = tk.Entry(width=6)
    entry.place(x=334, y=y_position)
    row_entries_team1.append(entry)
    #出塁率
    entry = tk.Entry(width=6)
    entry.place(x=396, y=y_position)
    row_entries_team1.append(entry)
    entries_team1.append(row_entries_team1)


# ホームチームの投手成績
label_team1_pitcher = tk.Label(text="投手成績を入力してください")
label_team1_pitcher.place(x=10, y=400)


pitcher_entries = []

# ホームチームの投手の入力欄
label = tk.Label(text="先発投手名")
label.place(x=10, y=430)
entry_defense_team1 = tk.Entry(width=10)
entry_defense_team1.place(x=81, y=430)
pitcher_entries.append(entry_defense_team1)

label = tk.Label(text="防御率")
label.place(x=190, y=430)
entry_strikeouts_team1 = tk.Entry(width=6)
entry_strikeouts_team1.place(x=232, y=430)
pitcher_entries.append(entry_strikeouts_team1)

label = tk.Label(text="奪三振数")
label.place(x=287, y=430)
entry_strikeouts_team1 = tk.Entry(width=6)
entry_strikeouts_team1.place(x=348, y=430)
pitcher_entries.append(entry_strikeouts_team1)




    
# 対戦チーム情報
# チーム名(対戦チーム名入力ボックス)
label_team2 = tk.Label(text="対戦チーム名")
label_team2.place(x=460, y=20)
# 対戦チーム名入力テキストボックス表示
entry2 = tk.Entry(width=25)
entry2.place(x=535, y=20)

# 打撃成績入力(対戦ホームチーム用テキスト)
label_batting2 = tk.Label(text="打撃成績を入力してください")
label_batting2.place(x=460, y=50)


# 打撃項目と選手名(対戦チーム　テキスト)
label_headers = ["打順", "守備", "選手名", "背番号", "打率", "本塁打", "出塁率"]
header_positions_2 = [x + 450 for x in header_positions]

for i, text in enumerate(label_headers):
    label = tk.Label(text=text)
    label.place(x=header_positions_2[i], y=75)


# 守備の選択肢
positions = ["投", "捕", "一", "二", "三", "遊", "左", "中", "右"]


#背番号の選択肢
uniform_number = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]

# 各打順の入力欄を表示
entries_team2 = []

for i in range(9):  # 入力欄を9行に増やす
    y_position = 95 + (i * 30)
    # 対戦チームの打撃成績入力欄
    row_entries_team2 = []


    #打順
    label = tk.Label(text=str(i + 1))
    label.place(x=70 + 400, y=y_position)
    #守備欄   
    var_team2 = StringVar(root)
    var_team2.set(positions[0])
    dropdown_team2 = tk.OptionMenu(root, var_team2, *positions)
    dropdown_team2.place(x=98 + 400, y=y_position)
    row_entries_team2.append(var_team2)

    #選手名 
    entry = tk.Entry(width=10)
    entry.place(x=170 + 400, y=y_position)
    row_entries_team2.append(entry)

    #背番号
    var_team2 = StringVar(root)
    var_team2.set(uniform_number[0])
    dropdown_team2 = tk.OptionMenu(root, var_team1, *uniform_number)
    dropdown_team2.place(x=256 + 400, y=y_position)
    row_entries_team2.append(var_team2)
    
    #打率
    entry = tk.Entry(width=6)
    entry.place(x=330 + 400, y=y_position)
    row_entries_team2.append(entry)
    #本塁打
    entry = tk.Entry(width=6)
    entry.place(x=390 + 400, y=y_position)
    row_entries_team2.append(entry)
    #出塁率    
    entry = tk.Entry(width=6)
    entry.place(x=450 + 400, y=y_position)
    row_entries_team2.append(entry)
    entries_team2.append(row_entries_team2)


# 相手チームの投手成績
label_team2_pitcher = tk.Label(text="投手成績を入力してください")
label_team2_pitcher.place(x=460, y=400)

    
# 相手チームの投手の入力欄
label = tk.Label(text="先発投手名")
label.place(x=460, y=430)
entry_defense_team2 = tk.Entry(width=10)
entry_defense_team2.place(x=531, y=430)
pitcher_entries.append(entry_defense_team2)

label = tk.Label(text="防御率")
label.place(x=640, y=430)
entry_strikeouts_team2 = tk.Entry(width=6)
entry_strikeouts_team2.place(x=682, y=430)
pitcher_entries.append(entry_strikeouts_team2)

label = tk.Label(text="奪三振数")
label.place(x=727, y=430)
entry_strikeouts_team2 = tk.Entry(width=6)
entry_strikeouts_team2.place(x=798, y=430)
pitcher_entries.append(entry_strikeouts_team2)

# 予測ボタン
button = tk.Button(root, text="予測する", command=predict)
button.place(x=400, y=500)

root.mainloop()
