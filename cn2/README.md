# CN2 代理筛选报告

- CSV 候选数：20
- 经百度前置测试数：20
- 可用数：16
- CN2 路由确认数：3

判断标准：经给定百度 HTTP CONNECT 前置可连接目标代理，且中国电信探针的回程 traceroute 出现 `59.43.0.0/16`。

| IP | 端口 | 地区 | ASN | 延迟 | CN2 证据 | 路由 |
|---|---:|---|---:|---:|---|---|
| `43.159.4.80` | 443 | SG/SIN | AS132203 | 3651 ms | Guangzhou: 59.43.130.110; Nanjing: 59.43.139.137, 59.43.22.6 | [查看](https://globalping.io?measurement=2jNu72nMcU25MBVKK00020w5D) |
| `202.55.27.177` | 443 | JP/NRT | AS4809 | 3730 ms | Guangzhou: 59.43.130.206, 59.43.141.146, 59.43.186.186; Beijing: 59.43.246.26, 59.43.46.82 | [查看](https://globalping.io?measurement=2ZbzJL8ve0SmI8ayN00020w5D) |
| `103.137.22.116` | 443 | TW/TPE | AS131151 | 4560 ms | Guangzhou: 59.43.187.178; Nanjing: 59.43.139.109, 59.43.248.202; Beijing: 59.43.19.94, 59.43.250.174 | [查看](https://globalping.io?measurement=2H1AP11II48dPFBF100020w5E) |
