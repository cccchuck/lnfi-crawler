import requests, time
import pandas as pd
import bech32


def get_token_id(token: str) -> str:
  token = token.upper()

  token_map = {
    'TREAT': '0f8b9bb57522a824746b2ce364ae606ad433bc36db66ab86756e0e156a1ed34d',
    'TRICK': 'e24574fd22b81230af6764617d37a2ec588679929516c4231292319e725d9d5c',
    'NOSTR': '475a642ed13bc44af6490c8571404988d7b514386cf8f3a603d04a0d2fa9f8f5',
    'BURGET': 'a9b7c7367b9ad647651ff710a6b2ff9fa5c0d186b6eb2ff541eb4a98f6bbdd4b',
    'TNA': '338563d188a4b4b99be8fe3112bd0fed956f197633bb701a826e3f9db9edaa64',
    'NODE1': 'f47918a476561d81413680b7c0cf979bf0ac775cc7955a34d4a8db26b2986aaf',
    'USDT': '0f929c417705fd4ad6fda742e107809367c7f5f10135cc6c5302bde3cb5982f1'
  }

  return token_map.get(token, None)


def get_order_history_v1(token: str, page: int, count: int) -> dict:
  token = token.upper()

  if page < 0:
    print('invalid ')

  if count > 100:
    print('invalid count')
    return

  try:
    ['TREAT', 'TRICK', 'NOSTR', 'TNA', 'BURGER'].index(token)
  except ValueError:
    print('invalid token')
    return

  url = 'https://market-api.lnfi.network/market/api/orderHistoryV1'
  payload = {
    'type': '',
    'address': '',
    'eventId': '',
    'status': 'SUCCESS',
    'token': token,
    'count': count,
    'page': page
  }

  try:
    res = requests.post(url=url, json=payload)
    if res.status_code == 200:
      return res.json()
    else:
      print('request error: ', res.status_code)
  except Exception as e:
    print('unknown error: ', e)


def get_holder_summary(token: str) -> dict:
  token = token.upper()
  token_id = get_token_id(token)

  if not token_id:
    print('invalid token')
    return

  url = 'https://market-api.lnfi.network/assets/api/getHolderSummary'
  payload = {
    'assetId': token_id
  }

  try:
    res = requests.post(url=url, json=payload)
    if res.status_code == 200:
      return res.json()
    else:
      print('request error: ', res.status_code)
  except Exception as e:
    print('unknown error: ', e)


def get_holder(token: str, page: int, count: int) -> dict:
  token = token.upper()
  token_id = get_token_id(token)

  if not token_id:
    print('invalid token')
    return

  if page < 0:
    print('invalid page')
    return

  url = 'https://market-api.lnfi.network/assets/api/getHolders'
  payload = {
    'page': page,
    'count': count,
    'owner': '',
    'assetId': token_id
  }

  try:
    res = requests.post(url=url, json=payload)
    if res.status_code == 200:
      return res.json()
    else:
      print('request error: ', res.status_code)
  except Exception as e:
    print('unknown error: ', e)


def encode_npub(hex_key):
  if hex_key.startswith('npub'):
    return hex_key
  try:
    data = bytes.fromhex(hex_key)
    converted = bech32.convertbits(data, 8, 5)
    return bech32.bech32_encode('npub', converted)
  except Exception:
    return hex_key

if __name__ == '__main__':
  token = 'usdt'
  page = 1
  size = 100

  # 获取历史订单
  # count = 0
  # orders = []
  # orders_file_path = f'./{token}_orders_history.csv'

  # while True:
  #   print(f'fetching {(page - 1) * size} ~ {page * size} orders')
  #   order_history = get_order_history_v1(token, page, size)
  #   if order_history.get('code', -1) == 0:
  #     print(f'fetching {(page - 1) * size} ~ {page * size} orders success')
  #     _orders = order_history.get('data', {}).get('orderPOS', [])
  #     _count = order_history.get('data', {}).get('sumCount', 0)
  #     print(f'total {_count} orders; current get {len(orders)} orders\n')

  #     orders.extend(_orders)

  #     if len(orders) >= _count:
  #       df = pd.DataFrame(orders)
  #       df.to_csv(orders_file_path, index=False)
  #       break

  #     page += 1
  #     time.sleep(0.5)
  #   else:
  #     print(f'fetching failed, reason: {order_history.get('data', '')}')

  # 获取持有者
  count = 0
  holders = []
  holders_file_path = f'./{token}_holders.csv'

  # 获取持有者总数
  print('fetching holders summary')
  holder_summary = get_holder_summary(token)
  if holder_summary.get('code', -1) == 0:
    count = holder_summary.get('data', {}).get('data', {}).get('holderCount', 0)
    if count == 0:
      print('no holders')
      exit(0)
    else:
      print(f'total {count} holders\n')
  else:
    print(f'fetching holders summary failed, reason: {holder_summary.get('data', '')}')
    exit(1)

  while True:
    print(f'fetching {(page - 1) * size} ~ {page * size} holders')
    holder_res = get_holder(token, page, size)
    if holder_res.get('code', -1) == 0:
      print(f'fetching {(page - 1) * size} ~ {page * size} holders success')
      holders.extend(holder_res.get('data', {}).get('data', []))
      print(f'total {count} holders; current get {len(holders)} holders\n')

      if len(holders) >= count:
        df = pd.DataFrame(holders)
        df['owner'] = df['owner'].apply(encode_npub)
        df.to_csv(holders_file_path, index=False)
        break

      page += 1
      time.sleep(0.5)
    else:
      print(f'fetching holders failed, reason: {holder_res.get('data', '')}')
      exit(1)





