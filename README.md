# macOS 上使用 Poetry 的指南

在 macOS 上使用 Poetry 建立 Python 專案環境的完整指南。

## 安裝

使用 Homebrew 安裝 Poetry：

```bash
brew install poetry
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
```

## 啟動 FastAPI 開發伺服器

```bash
cd src/kdan_backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
## openAPI 文件

```bash
http://localhost:8000/docs
```

