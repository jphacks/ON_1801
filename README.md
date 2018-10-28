# おかねかんりちゃん

[![Product Name](thumbnail.png)](https://youtu.be/Nqmd2o_2z3U)

## 製品概要
### Money  x Tech

### 背景（製品開発のきっかけ、課題等）
- お金管理アプリをもっと楽しく使えるようにしたい。

- 携帯（スマートフォン）でお金の管理をしてみたい方（又は現在使用している方）を対象に やってみたいけど、ただ使用履歴を記録するだけでは長く続かない・飽きやすいという問題を解決出来ないか考えた。


### 製品説明（具体的な製品の説明）
ClovaとZaimを連携させ、Zaimから取得した金額を元に Clova（おかねかんりちゃん）が様々な反応を見せてくれる。

### 特長

#### 1. お金を使いすぎると警告してくれる

#### 2. 口座の残高通知が出来る

#### 3. 今月の利用金額を通知

### 解決出来ること
お金の使いすぎによる破産の回避。  
記録が苦手な方でも楽しくお金の管理に取り組むことが出来る。 アプリの長期間の利用に繋がりやすい。
### 今後の展望
顔認証やセンサーによってClova自身が話しかけてくる。  
金銭的な余裕があるとamazon欲しいものリストから購入可能な商品をオススメする用にする。
## 開発内容・開発技術
### 活用した技術
#### API・データ

* [Clova Extensions Kit API](https://clova-developers.line.me/#/)
* [Zaim API](https://zaim.net)

#### フレームワーク・ライブラリ・モジュール
* [flask](http://flask.pocoo.org)
* [Amazon AWS](https://aws.amazon.com/jp/)

#### デバイス
* [Macbook Pro](https://www.apple.com/jp/macbook-pro/?afid=p238%7CsxLoA1Hns-dc_mtid_18707vxu38484_pcrid_284003974216_&cid=aos-jp-kwgo-mac--slid-)
* [Clova Friends [BROWN]](https://clova.line.me/clova-friends-mini/?gclid=CjwKCAjwmdDeBRA8EiwAXlarFvDKC0_sRzvsM8ZIc8xJyy67oq0ecu4AKxQgiZHg8z2C2sY4_jcMDRoCyFYQAvD_BwE)

### 独自開発技術（Hack Dayで開発したもの）
#### 2日間に開発した独自の機能・技術
* ClovaとZaimの連携
#### 使用上の注意
* direnvを使用して環境変数のパラメータを設定しているので、環境変数の設定を忘れずに。


```
export CLOVA_ID="clova_id"
export ZAIM_KEY="zaim_key"
export ZAIM_SECRET="zaim_secret"
export ACCESS_TOKEN_ZAIM="access_token_zaim"
export ACCESS_TOKEN_ZAIM_SECRET="access_token_zaim_secret"
```


#### 起動・使用方法
* Zaim の Developper モードで会員登録を行う( https://dev.zaim.net/ )
* Add a new application で Service tipe を Client Appで、Access Level に全てチェックを付けて作成。
* Consumer Key と Consumer Secret がもらえるので環境変数に設定。
* perl src_flask/zaim_access.pl で表示されるURLにブラウザからアクセスしてHTMLに隠れているVerifier を標準入力すると Access Token と Access Token Secret が得られるので、こちらも環境変数に設定。
##### ngrokを使用する際
* FLASK_APP=application.py flask runでclovaが動きます。
* FLASK runで動かす。
* (lineのdeveloperでurlを設定しないといけない)

##### 必要なモジュール
* perl
```
cpanm OAuth::Lite::Consumer
cpanm OAuth::Lite::Token
```

* python
```
pip install zaim
pip install line-bot-sdk
pip install clova-cek-sdk
pip install Flask
```