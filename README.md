# Kdan Backend

## 目錄

- [Kdan Backend](#kdan-backend)
  - [目錄](#目錄)
  - [環境](#環境)
  - [安裝](#安裝)
  - [安裝依賴](#安裝依賴)
  - [啟動虛擬環境](#啟動虛擬環境)
  - [建立資料庫](#建立資料庫)
  - [啟動 FastAPI 開發伺服器](#啟動-fastapi-開發伺服器)
  - [openAPI 文件](#openapi-文件)

## 環境

- python > 3.8
- postgres > 16

## 安裝

安裝 Poetry：

```bash
# mac
brew install poetry

# windows
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

安裝完成後，確認版本：

```bash
poetry --version
```

## 安裝依賴

```bash
poetry install
```

## 啟動虛擬環境

```bash
poetry env activate // 複製此指令產出的路徑，並在終端機中輸入

# 以下輸出範例，複製並終端機輸入:
source /Users/your_username/Library/Caches/pypoetry/virtualenvs/kdan-backend-00000000000000000000000000000000/bin/activate

# 切換目錄
cd src/kdan_backend
```

## 建立資料庫

```bash
python3 etl.py
```

## 啟動 FastAPI 開發伺服器

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
## openAPI 文件

```bash
http://localhost:8000/docs
```


