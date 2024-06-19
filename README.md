# soft
 This repository has been created for a homework task.

## 概要
　投票システムを作る。

## 実行方法
### release code
```
git clone git@github.com:hello30190f/soft.git
cd soft/release
python main.py
```
or
```
git clone https://github.com/hello30190f/soft.git
cd soft/release
python main.py
```

### debug code
```
git clone git@github.com:hello30190f/soft.git
cd soft/debug
python main.py
```
or
```
git clone https://github.com/hello30190f/soft.git
cd soft/debug
python main.py
```

これで動かなかったら、lineかdiscordで連絡してください。何回か試してからの方が幸せになれるかもです。

## フォルダ構成
```
├─debug
├─old
├─release
├─testCaseData
└─tools
```
### release
　いったん切りのいいところを完成として、ちゃんと動くだろうと思ったコードがおいてあります。レポートの提出では、このコードを完成しています。

### debug
　開発中のコードが置いてあります。

### old
　新たにrelease code を更新したときに、一応一つ前のコードを置いています。

### testCaseData
　テストに使うデータがおいてあります。

### tools
　データを生成するツールなどがおいてあります。


## ファイル構成
### mainForGui.py
　main.py の処理にGUIを付けたものである。初めに実行される処理が記述されている。C言語でいうmain関数に相当する機能を持つ。

### data.py
　立候補者、投票のデータを管理するクラスが宣言されている。

### err.py
　ファイルのフォーマットに問題がないかなどを調べる関数群がある。

### process.py
　実際に当選者を見つける処理を行う。

### statusPanel.py
　GUIを表示するためのclass等が宣言され、メンバ変数、メンバ関数を持っている。