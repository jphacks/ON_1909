import os, sys, time
import tkinter
import detection_only

# clickイベント
def btn_click():
    detection_only.receiver(txt.get())


# GUI設計プログラム， 関数定義しないこと
root = tkinter.Tk()
root.title(u"指パッチン スクリーンショット")
root.geometry("400x300")

#ラベルを追加
label = tkinter.Label(root, text="startボタンを押してください！")
#表示
label.grid()

button = tkinter.Button(root, text="start", command=btn_click)
button.place(x=150, y=120)

# テキストラベル
lbl = tkinter.Label(text='スクショ制限時間')
lbl.place(x=30, y=70)

# テキストボックス
txt = tkinter.Entry(width=20)
txt.place(x=150, y=70)

root.mainloop()