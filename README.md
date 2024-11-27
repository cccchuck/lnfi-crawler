# Lnfi Crawler

## 运行要求

- python 3.10+

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行

- 获取持有者

  ```bash
  python main.py get-holders xxx
  ```

- 获取订单
  ```bash
  python main.py get-orders xxx
  ```

## 参数

- action: 支持的 action 列表见 `main.py` 文件中的 `parser` 变量

- token: 支持的代币列表见 `main.py` 文件中的 `SUPPORTED_TOKENS` 变量
