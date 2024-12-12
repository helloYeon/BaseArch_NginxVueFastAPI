# peppol-receive-system😁

peppol receive system project for web

## architecture

Python 3.11.9

| no   | name              | version        | license | description                                                                                        |
| :--- | :---------------- | :------------- | :------ | :------------------------------------------------------------------------------------------------- |
| 1    | fastapi           | 0.111.0        | -       | Web framework for building APIs with Python                                                        |
| 2    | uvicorn           | 0.12.0,<0.31.0 | -       | ASGI server implementation for Python web apps                                                     |
| 3    | mysqlclient       | 2.2.4          | -       | MySQL database connector for Python                                                                |
| 4    | alembic           | 1.13.2         | -       | Database migration tool for SQLAlchemy                                                             |
| 5    | SQLAlchemy        | 2.0.23         | -       | SQL toolkit and Object-Relational Mapping (ORM) library                                            |
| 6    | sqlalchemy_utils  | 0.41.2         | -       | Utility functions and data types for SQLAlchemy                                                    |
| 7    | ppretty           | 1.3.0          | -       | Pretty print utility for complex data structures                                                   |
| 8    | boto3             | 1.35.0         | -       | AWS SDK for Python, allowing Python developers to write software that makes use of Amazon services |
| 9    | Faker             | 27.0.0         | -       | Library for generating fake data for testing                                                       |
| 10   | reportlab         | 4.2.2          | -       | Library for creating PDF documents using templates                                                 |
| 11   | starlette         | 0.37.2         | -       | Lightweight ASGI framework/toolkit for building async web applications                             |
| 12   | xhtml2pdf         | 0.2.16         | -       | Library for converting HTML/CSS to PDF                                                             |
| 13   | python-dotenv     | 1.0.1          | -       | Library for loading environment variables from a .env file                                         |
| 14   | Jinja2            | >=3.1.2        | BSD     | Template engine for Python                                                                         |
| 15   | pendulum[test]    | 3.0.0          | -       | Python library for working with dates and times, with better timezone handling                     |
| 16   | ruff              | 0.6.1          | -       | Fast Python linter and code formatter                                                              |
| 17   | pydantic-settings | 2.4.0          | -       | Settings management library for Pydantic-based applications                                        |
| 18   | xmltodict         | 0.13.0         | -       | XML to dictionary converter for Python                                                             |
| 19   | gunicorn          | 22.0.0         | -       | Python WSGI HTTP Server for running web applications                                               |
| 20   | pytest            | 8.3.1          | -       | Testing framework for Python                                                                       |
| 21   | pytest-mock       | 3.14.0         | -       | Pytest plugin for easier mocking in tests                                                          |
| 22   | factory-boy       | 3.3.1          | -       | Fixtures replacement library for Python, based on factory pattern                                  |
| 23   | selenium          | 4.23.1         | -       | Tool for automating web browsers interaction                                                       |
| 24   | webdriver-manager | 4.0.2          | -       | Manages WebDriver binaries for Selenium                                                            |

Vue.js 3.4.14

| no   | name            | ver      | license | description                                               |
| :--- | :-------------- | :------- | :------ | :-------------------------------------------------------- |
| 1    | Vuetify         | 3.4.10   | -       | Vue.js framework                                          |
| 2    | TypeScript      | 5.3.3    | -       | javaScript with syntax for types                          |
| 3    | Node.js         | 18.18.14 | -       | javaScript runtime environment                            |
| 4    | vue-router      | 4.0.0    | -       | <https://github.com/vuejs/router#readme>                  |
| 5    | pinia           | 2.0.23   | -       | <https://github.com/vuejs/pinia#readme>                   |
| 6    | vue3-cookies    | 18.18.14 | -       | <https://github.com/KanHarI/vue3-cookies#readme>          |
| 7    | vuedraggable    | 4.1.0    | -       | <https://github.com/SortableJS/vue.draggable.next#readme> |
| 8    | vee-validate    | 4.12.4   | -       | <https://vee-validate.logaretm.com/v4>                    |
| 9    | yup             | 1.3.3    | -       | <https://github.com/jquense/yup#readme>                   |
| 10   | html-to-pdfmake | 2.5.1    | -       | <https://github.com/Aymkdn/html-to-pdfmake#readme>        |
| 11   | pdfmake         | 0.2.8    | -       | <http://pdfmake.org>                                      |
| 12   | date-fns        | 3.2.0    | -       | <https://github.com/date-fns/date-fns#readme>             |

## 環境構築

1. 準備

   - Docker実行環境
   - Makeコマンド
     - MakeFileに各種コマンドを用意
   - vscode拡張機能
     - .vscode/extensions.jsonに記載

2. pythonの仮想環境を作成

    ```bash
    venvの仮想環境を作成
    python3.11 -m venv .venv

    仮想環境のアクティベート
    windowsの場合
    .venv\Scripts\activate
    Linux, Macの場合
    source .venv/bin/activate

    python --version
    ```

    ※python3.11がインストールされていない場合は環境に合わせてインストール後再度仮想環境を作成

3. コンテナ起動

    ```bash
    下記コマンドでコンテナイメージのビルド、各種packageインストール、マイグレーション
    make init
    下記コマンドでコンテナの起動
    make up
    下記コマンドでコンテナの停止、削除
    make down
    ```

4. アクセス

   - API
     - <http://localhost:2000/api>
   - 画面
     - <http://localhost:2000/>
   - phpMyAdmin
     - <http://localhost:8080>
   - swagger-ui
     - <http://localhost:8002>
   - minio
     - <http://localhost:9000>

5. マスタデータ挿入

    ```bash
    make seed
    ```

6. ログイン

    ログイン可否はcookieで判断
    tools/starter_peppol.htmlをブラウザで表示してユーザー認証情報変更を2、ローカル環境選択で「一覧画面へ」を押下でログインユーザーで一覧画面に遷移

## frontendルール

### ディレクトリ構成

./frontend

```text
src
├── @types
├── assets
├── codegen
├── components
├── const
├── env
├── layouts
├── plugins
├── router
├── store
├── utils
└── views
```

- assets
  - 静的ファイル
- codegen
  - swaggerからtypescript-fetchで自動生成されたapi定義
- components
  - 単一ファイルコンポーネント
- const
  - 読み取り専用定数定義
- env
  - 環境変数
- layouts
  - 複数のrouteで共通的なレイアウト
- plugins
  - 外だし処理等
- router
  - SPAのrouter定義
  - layoutはここで指定する
- store
  - 状態管理(Pinia)
- views
  - routerで呼び出すファイル

### コンポーネント

- 自身の外側にmergeを持たないこと
- コンポーネントの呼び出しはアッパーキャメルケースで統一すること
- parts
  - 共通的な部品
  - 自身の位置は指定できない
  - mergeは持たないこと
- templates
  - 部品の集合
  - 部品の位置の指定や、部品間の余白を調整できる
  - 使用する{views}を接頭辞にすること
  - 共通的なものはCommonをつけること

### HTML&CSS

- 余分なタグは増やさない
- 極力レイアウトはフレックスボックスで指定する
- 要素と要素の幅はmergeで指定する
- 上下の余白はmerge-topで指定する
- 左右の余白は箇所で合わせ、mergeの相殺が起きないようにする
- scopedを各コンポーネントで指定する
- deepセレクターは見通しが悪くなるため極力使用せず、使用する際はコメントを残す
- !importantやIDでのスタイル指定は禁止

### vuetify

- スタイル調整は極力オプションを指定する
- 極力vuetifyのタグにcssでスタイルを指定するのは場所やフォント調整のみにする
- vuetifyのタグはコンポーネント規約のpartsの役割を持つ
- assets/styles/settings.scssでSASS変数を変更可能（全体への影響を考慮）
- 新規コンポーネントを使用する場合はplugins/vuetify.tsでimportする

## swaggerルール

### ディレクトリ構成_

./documents

```text
api
├── components
├── definitions
├── paths
└── schemas
```

- components/objects
  - 再利用可能なコンポーネントオブジェクト
- definitions
  - 最小単位の項目定義
- paths
  - エンドポイント以下
  - tagでフォルダを分割すること
- schemas
  - request | responseで分ける
  - pathsから呼び出し

### 各種ルール

api自動生成を行う上での必要ルール

- 下記プロパティは必須
| オプション  | 例      |
| :---------- | :------ |
| type        | integer |
| nullable    | false   |
| description | 説明    |
| example     | 例      |

### 自動生成

swagger定義を元にフロント側で呼び出すapiのメソッドを自動で生成
型情報を正確に扱うことができるかつswaggerの定義を正確に作成できるなどの目的

```bash
下記コマンドで自動生成かつフォーマット
make gen-fetch
```

※swaggerを変更した場合は毎回自動生成を実行すること

## backendルール

### ディレクトリ構成__

./backend

```text
src
├── api
│   ├── middlewares
│   └── v1
├── core
├── db
│   ├── factories
│   ├── fakers
│   ├── migrations
│   ├── seeders
│   └── versions
├── dependencies
├── enums
├── exceptions
├── handlers
├── helpers
├── models
├── repositories
├── services
├── storage
│   ├── for_test
│   ├── logs
│   └── templates
└── tests
    ├── api
    └── services
```

- api
  - v1: エンドポイントやルーティング、スキーマ定義
- core
  - 定数定義、設定
- db
  - alembicでのDB関連
- enums
  - enum定義
- exceptions
  - 例外クラス定義
- models
  - データベースモデル定義
- repositories
  - データベースと接続されデータの取得や保存を行うクラス定義
- services
  - ロジックやサービスクラス定義
- storage
  - 静的ファイルやログの保存場所
- tests
  - 自動テストコード

### DB関連

テーブルに変更があった場合
models/{テーブル名単数形}.pyを作成編集後下記コマンドでマイグレーションファイル生成

```bash
make exec-be
pythonコンテナ内で
cd db
alembic revision --autogenerate -m "マイグレーションのメッセージ"
```

※差分としてindex名を変更する記述が出る場合があるためdrop_index()とcreate_index()は削除する

```bash
下記のような記述の行は削除
op.drop_index('idx_esCompanyId', table_name='company_infos')
op.create_index(op.f('ix_company_infos_deletedAt'), 'company_infos', ['deletedAt'], unique=False)
```

マイグレーションファイル生成後

```bash
make migrate
```
