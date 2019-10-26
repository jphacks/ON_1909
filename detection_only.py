# -*- coding: utf-8 -*-

"""
実際に指パッチンを検出するファイル
基本はdetection.pyと同じだが、テスト用として使う
以下で実行
python detection_only.py (実行する秒数)
"""
from datetime import datetime
import pyaudio
import sys
import numpy as np
import tensorflow as tf
import os
import pyautogui
import argparse
import requests
from dotenv import load_dotenv
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
load_dotenv()
project_dir = os.getcwd() + "/"
# 自作モジュールのimport
sys.path.append(project_dir + "./my_modules/")
import learning
import const

"""
定数
"""
# 実行時に引数に時間を指定していたらその時間分実行し、指定していなかったらデフォルトで100秒
if len(sys.argv) == 2:
    RECORD_SECONDS = int(sys.argv[1]) 
else:
    RECORD_SECONDS = 100

"""
tensorflowに関する処理
"""
def set_tensorflow():
    
    # tensorflowで必要な変数を取得
    x, p, t, loss, train_step, correct_prediction, accuracy, y = learning.learning_algorithm(tf, const.FOR_TENSORFLOW.DATA_LEN)
    
    # tfのセッション初期化
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())
    
    # `do_learning.py`で学習させたデータを取得
    saver = tf.train.Saver()
    if const.FOR_PYAUDIO.RATE == 44100:
        saver.restore(sess, project_dir + "./model_data_44100/model.ckpt")
    elif const.FOR_PYAUDIO.RATE == 16000:
        saver.restore(sess, project_dir + "./model_data_16000/model.ckpt")

    return p, x, sess

"""
pyaudioに関する処理
"""
def set_pyaudio():
    
    pa = pyaudio.PyAudio()
    
    stream = pa.open(
        format = const.FOR_PYAUDIO.FORMAT,
        channels = const.FOR_PYAUDIO.CHANNELS,
        rate = const.FOR_PYAUDIO.RATE,
        input = True,
        frames_per_buffer = const.FOR_PYAUDIO.chunk
    )

    return pa, stream

class Screen_shot:
  def __init__(self):
    self.count = 0
    self.path = "./image"
        
  def main(self):
    if not os.path.exists(self.path):
      os.makedirs(self.path)
    s = pyautogui.screenshot()
    s.save('{0}/screenshot{1}.png'.format(self.path,self.count))
    line_notify_api = 'https://notify-api.line.me/api/notify'
    line_notify_token = os.environ["LINE_NOTIFY_TOKEN"]
    headers = {'Authorization': 'Bearer ' + line_notify_token}
    payload = {'message': "おはあやさ"}
    files = {"imageFile": open('{0}/screenshot{1}.png'.format(self.path,self.count), "rb")}
    requests.post(line_notify_api, data=payload, headers=headers, files=files)
    self.count += 1

def main():
    p, x, sess = set_tensorflow()
    pa, stream = set_pyaudio()
    sc_shot = Screen_shot()
    # データを入れていく
    # allの長さは20以上にならない
    all = []
    
    # tmpは常に同じ長さ
    tmp = [False for k in range(0, 20)]
    
    print('指パッチンの検出を始めます')
    for i in range(0, int(const.FOR_PYAUDIO.RATE / const.FOR_PYAUDIO.chunk * RECORD_SECONDS)):
    
        data = stream.read(const.FOR_PYAUDIO.chunk, exception_on_overflow = False)
        npData = np.frombuffer(data, dtype="int16") / 32768.0
    
        # npDataの中にthresoldより大きい数字があるかどうか
        threshold = 0.3
        isThresholdOver = False
        if max(npData) > threshold:
            isThresholdOver = True
    
        tmp.append(isThresholdOver)
        tmp.pop(0)
    
        # 9,10, 11がのどれかがtrueで他がfalseだけなら反応
        # iが11まではallの長さが足りないためエラーになる。
        if sum(tmp[9: 11]) >= 1 and sum(tmp) <= 3 and i >= 12:
    
            # 単発音の部分を取得する
            big_point_data = all[-10:-8] 
    
            big_point_data = np.frombuffer(b''.join(big_point_data), dtype="int16") / 32768.0
            X = np.fft.fft(big_point_data)
            amplitudeSpectrum = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in X]
    
            # 指パッチンである確率を算出
            result = sess.run(p, feed_dict={x: np.array([amplitudeSpectrum])})

            if(result[0] >= 0.5):
                print('これは指パッチンです\n')
                sc_shot.main()
            else:
                print('これは指パッチンではないです\n')
    
    
            tmp = [False for k in range(0, 20)]
    
        all.append(data)
    
        # allに入れっぱなしだとメモリを食う気がしたので、20以上なら0番目を削除
        if len(all) >= 20:
            all.pop(0)
    
    stream.close()
    pa.terminate()
    print('指パッチン検出を終了します。')

if __name__ == "__main__":
    main()
