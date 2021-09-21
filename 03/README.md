# 03

作成した Scrapy クローラを Zyte というサービスを使ってクロールさせます。　　
https://www.zyte.com/  
やる場合は、アカウントを作成してくださいね

## shub のインストール

zyte にクローラをデプロイするために利用する shub というライブラリをインストールします。

```
pip3 install shub
```

インストールすると shub コマンドが利用できるようになります。

## scrapy のプロジェクト作成

プロジェクト作成して適当なクローラを作成

```
scrapy startproject kaigo
cd kaigo
scrapy genspider kaigo_spider www.kaigo-kyuujin.com
```

## zyte でクローラ用のプロジェクトを作成する

zyte にログインしてプロジェクトを作成して。cd kaigo でプロジェクトディレクトリに移動して shub コマンドでログイン＆デプロイしてください。

```
shub login
# APIキーを入力
shub deploy xxx
# xxxにプロジェクトIDを入力
```

デプロイが完了したら、zyte のダッシュボード上で追加したプロジェクトのクローラが表示されているのでクロールを開始！

デプロイがうまくいかないなーと思ったら、デプロイで生成される build ディレクトリーを確認して、クロールに必要なものがデプロイされているかを一度確認した方がいい。

### 生成される設定ファイルに関して

shub deploy を実行すると色々な設定ファイルが生成されますが、設定ファイルをカスタマイズすることでデプロイした後の環境をある程度コントロールすることができます。  
・scrapinghub.yml プロジェクトの requirements.txt などを変更可能  
・setup.py プロジェクトのデプロイに含めるファイルや settings.py などの設定変更が可能

## デプロイに関して

以下 URL 見た方が早いっす  
https://data.gunosy.io/entry/python-scrapy-scraping
