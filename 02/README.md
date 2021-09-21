# 02

SQLAlchemy を利用してスクレイピングしたデータを DB に保存します

## pip で SQLAlchemy のインストール

pip で scrapy をインストールします。

```
pip3 install SQLAlchemy
```

最新は v1.4.xxx になっていると思います。  
今回は SQLite を利用しますが、MySQL に保存する場合は PyMySQL と mysqlclient もインストールする必要があります。

## scrapy のプロジェクト作成

とりあえず scrapy プロジェクト＆Spider の作成

```
scrapy startproject beauty
cd beauty
scrapy genspider beauty_spider beauty.rakuten.co.jp
```

## SQLAlchemy で DB 接続

今回はプロジェクト内に SQLAlchemy の接続設定を用意したいと思います。  
インストールした SQLAlchemy で DB 接続するには、接続設定と ORM で利用するモデルクラスが必要となります。今回これらは作成したプロジェクトの pipelines.py や items.py がある階層に作成します。  
接続設定を settings.py に設定できるようにして、models.py でモデルクラスを作成します。  
細々とした部分については、ソースコードを参照してください。

## クロールしたデータを SQLite に保存

保存処理は pipelines.py の Pipeline クラスで行います。  
Pipeline での保存処理を作成したあと、 scrapy crawl beauty_spider を実行すると SQLite の DB が作成されデータが保存されていることが確認できると思います。
