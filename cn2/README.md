# CN2 代理筛选报告

- CSV 地区候选数：3045
- 经百度前置测试数：3045
- 可用数：1739
- 已完成路由追踪：69
- 待路由追踪：1670
- CN2 路由确认数：25

判断标准：经给定百度 HTTP CONNECT 前置可连接目标代理，且中国电信探针的回程 traceroute 出现 `59.43.0.0/16`。

| IP | 端口 | 地区 | ASN | 延迟 | CN2 证据 | 路由 |
|---|---:|---|---:|---:|---|---|
| `202.55.27.177` | 443 | JP/NRT | AS4809 | 1665 ms | Guangzhou: 59.43.144.209, 59.43.246.26, 59.43.39.190; Nanjing: 59.43.139.133, 59.43.186.186; Beijing: 59.43.183.2, 59.43.39.98, 59.43.46.82 | [查看](https://globalping.io?measurement=21pqJP54vnfweuTe800020w5Y) |
| `38.175.192.154` | 443 | HK/HKG | AS979 | 2026 ms | Nanjing: 59.43.123.89, 59.43.22.41, 59.43.248.246; Nanjing: 59.43.139.113, 59.43.16.166, 59.43.183.110 | [查看](https://globalping.io?measurement=2paAxP5Apm2uTj5kU00020w5c) |
| `64.90.24.236` | 443 | HK/HKG | AS979 | 1478 ms | Guangzhou: 59.43.130.154; Nanjing: 59.43.39.190, 59.43.46.97; Nanjing: 59.43.132.153, 59.43.39.178 | [查看](https://globalping.io?measurement=2LW64WJZw3Ho7TL9f00020w5l) |
| `103.24.219.134` | 443 | HK/HKG | AS42960 | 1002 ms | Guangzhou: 59.43.16.166, 59.43.248.250; Nanjing: 59.43.139.117, 59.43.183.110, 59.43.22.33; Beijing: 59.43.182.110, 59.43.19.98, 59.43.246.226 | [查看](https://globalping.io?measurement=2LgBXxuyqqe2oceQT00020w5d) |
| `103.242.15.87` | 443 | HK/HKG | AS401696 | 1033 ms | Nanjing: 59.43.39.118, 59.43.46.101; Nanjing: 59.43.130.210, 59.43.139.137 | [查看](https://globalping.io?measurement=23haVCSxjawO0Gq4h00020w5g) |
| `149.104.2.56` | 443 | HK/HKG | AS932 | 1160 ms | Beijing: 59.43.138.58, 59.43.181.54, 59.43.46.86; Xi'an: 59.43.181.54, 59.43.46.157 | [查看](https://globalping.io?measurement=2P5OSxTtxelpqMLCh00020wES) |
| `149.104.31.208` | 443 | HK/HKG | AS139659 | 1155 ms | Guangzhou: 59.43.16.166, 59.43.183.110; Nanjing: 59.43.130.158, 59.43.139.113, 59.43.248.250 | [查看](https://globalping.io?measurement=2atDXEVXmL0F9BUpP00020wER) |
| `198.44.182.190` | 443 | HK/HKG | AS62468 | 1157 ms | Beijing: 59.43.46.82 | [查看](https://globalping.io?measurement=2LQdiR7UfeucmtKY900020wES) |
| `156.239.12.210` | 443 | HK/HKG | AS154321 | 1131 ms | Guangzhou: 59.43.183.110; Nanjing: 59.43.139.117, 59.43.248.250, 59.43.250.50 | [查看](https://globalping.io?measurement=2ETnrcuAQ5F2u06YD00020wEP) |
| `165.154.20.213` | 443 | HK/HKG | AS135377 | 1124 ms | Xi'an: 59.43.156.129 | [查看](https://globalping.io?measurement=2NwI4Ze38yVhBR39600020wEP) |
| `193.134.209.123` | 443 | HK/HKG | AS139659 | 1063 ms | Guangzhou: 59.43.248.246; Nanjing: 59.43.139.117, 59.43.248.250 | [查看](https://globalping.io?measurement=2NFwZUFDzH4BFXkEK00020wEK) |
| `68.64.182.79` | 443 | HK/HKG | AS139659 | 2749 ms | Guangzhou: 59.43.248.246; Nanjing: 59.43.139.109, 59.43.248.246; Nanjing: 59.43.139.109, 59.43.183.110 | [查看](https://globalping.io?measurement=27qOEvbWcyQ0hRwyq00020w5b) |
| `38.207.177.204` | 443 | HK/HKG | AS139659 | 948 ms | Nanjing: 59.43.130.122, 59.43.139.117, 59.43.248.246; Nanjing: 59.43.123.89, 59.43.188.122 | [查看](https://globalping.io?measurement=2Nu40TJGXzkCPLi8000020w5c) |
| `43.160.254.163` | 443 | SG/SIN | AS132203 | 1127 ms | Nanjing: 59.43.139.117 | [查看](https://globalping.io?measurement=2Hg4PXQzKGJNyRjR700020wEP) |
| `82.158.88.94` | 443 | HK/HKG | AS401701 | 1156 ms | Guangzhou: 59.43.183.110; Nanjing: 59.43.139.129, 59.43.183.110; Beijing: 59.43.183.122, 59.43.248.2; Xi'an: 59.43.137.241, 59.43.188.122 | [查看](https://globalping.io?measurement=2MoUn7gsFJdC3BnLz00020wES) |
| `150.109.11.223` | 443 | SG/SIN | AS132203 | 1113 ms | Nanjing: 59.43.139.129; Beijing: 59.43.145.62, 59.43.22.41; Xi'an: 59.43.137.241 | [查看](https://globalping.io?measurement=26FEmuI702JMATYME00020wEO) |
| `43.160.209.30` | 443 | SG/SIN | AS132203 | 1109 ms | Nanjing: 59.43.139.109; Xi'an: 59.43.137.241 | [查看](https://globalping.io?measurement=2IIkBo0KB5IV0xrl500020wEO) |
| `43.156.142.191` | 443 | SG/SIN | AS132203 | 1114 ms | Nanjing: 59.43.139.113 | [查看](https://globalping.io?measurement=20h2UogvgwUaboyCo00020wEO) |
| `43.160.253.225` | 443 | SG/SIN | AS132203 | 1089 ms | Nanjing: 59.43.139.117 | [查看](https://globalping.io?measurement=2d5yRvREhWyGxkFzQ00020wEM) |
| `111.119.193.50` | 443 | SG/SIN | AS136907 | 1616 ms | Guangzhou: 59.43.130.102; Nanjing: 59.43.39.118, 59.43.46.101; Beijing: 59.43.159.18, 59.43.46.82 | [查看](https://globalping.io?measurement=2whzoXU1xDkzVQVJr00020w5c) |
| `43.156.23.85` | 443 | SG/SIN | AS132203 | 3165 ms | Guangzhou: 59.43.250.50; Nanjing: 59.43.139.109, 59.43.16.166 | [查看](https://globalping.io?measurement=2bPYUg7gIR76yVGed00020w5l) |
| `191.222.212.77` | 443 | JP/NRT | AS906 | 1116 ms | Guangzhou: 59.43.130.194, 59.43.144.209; Nanjing: 59.43.139.133 | [查看](https://globalping.io?measurement=2EqHVS3p3juopEHaZ00020wEO) |
| `207.56.227.33` | 443 | JP/NRT | AS140227 | 1139 ms | Guangzhou: 59.43.183.2, 59.43.22.6, 59.43.46.77; Nanjing: 59.43.139.137, 59.43.159.18, 59.43.183.2, 59.43.39.130 | [查看](https://globalping.io?measurement=26kHW3PfBvhTc09zp00020wER) |
| `154.64.246.151` | 443 | HK/HKG | AS979 | 1031 ms | Nanjing: 59.43.139.109, 59.43.188.122; Shenzhen: 59.43.188.122 | [查看](https://globalping.io?measurement=2yzg8AxKvZs4cbX1L00020wEI) |
| `64.90.24.26` | 443 | HK/HKG | AS979 | 1137 ms | Nanjing: 59.43.132.149; Xi'an: 59.43.156.129 | [查看](https://globalping.io?measurement=27uSTgcGacpPHUc6M00020wER) |
