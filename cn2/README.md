# CN2 代理筛选报告

- CSV 地区候选数：3045
- 经百度前置测试数：3045
- 可用数：1738
- 已完成路由追踪：129
- 待路由追踪：1610
- CN2 路由确认数：38

判断标准：经给定百度 HTTP CONNECT 前置可连接目标代理，且中国电信探针的回程 traceroute 出现 `59.43.0.0/16`。

| IP | 端口 | 地区 | ASN | 延迟 | CN2 证据 | 路由 |
|---|---:|---|---:|---:|---|---|
| `202.55.27.177` | 443 | JP/NRT | AS4809 | 3117 ms | Guangzhou: 59.43.144.209, 59.43.246.26, 59.43.39.190; Nanjing: 59.43.139.133, 59.43.186.186; Beijing: 59.43.183.2, 59.43.39.98, 59.43.46.82 | [查看](https://globalping.io?measurement=21pqJP54vnfweuTe800020w5Y) |
| `38.175.192.154` | 443 | HK/HKG | AS979 | 2846 ms | Nanjing: 59.43.123.89, 59.43.22.41, 59.43.248.246; Nanjing: 59.43.139.113, 59.43.16.166, 59.43.183.110 | [查看](https://globalping.io?measurement=2paAxP5Apm2uTj5kU00020w5c) |
| `64.90.24.236` | 443 | HK/HKG | AS979 | 1690 ms | Guangzhou: 59.43.130.154; Nanjing: 59.43.39.190, 59.43.46.97; Nanjing: 59.43.132.153, 59.43.39.178 | [查看](https://globalping.io?measurement=2LW64WJZw3Ho7TL9f00020w5l) |
| `82.158.91.93` | 443 | HK/HKG | AS401701 | 1081 ms | Xi'an: 59.43.183.110, 59.43.93.109 | [查看](https://globalping.io?measurement=2APU5OeQbZfEQslJa00020wEn) |
| `103.24.219.134` | 443 | HK/HKG | AS42960 | 1105 ms | Guangzhou: 59.43.16.166, 59.43.248.250; Nanjing: 59.43.139.117, 59.43.183.110, 59.43.22.33; Beijing: 59.43.182.110, 59.43.19.98, 59.43.246.226 | [查看](https://globalping.io?measurement=2LgBXxuyqqe2oceQT00020w5d) |
| `103.242.15.87` | 443 | HK/HKG | AS401696 | 1092 ms | Nanjing: 59.43.39.118, 59.43.46.101; Nanjing: 59.43.130.210, 59.43.139.137 | [查看](https://globalping.io?measurement=23haVCSxjawO0Gq4h00020w5g) |
| `149.104.2.56` | 443 | HK/HKG | AS932 | 1611 ms | Beijing: 59.43.138.58, 59.43.181.54, 59.43.46.86; Xi'an: 59.43.181.54, 59.43.46.157 | [查看](https://globalping.io?measurement=2P5OSxTtxelpqMLCh00020wES) |
| `149.104.31.208` | 443 | HK/HKG | AS139659 | 1243 ms | Guangzhou: 59.43.16.166, 59.43.183.110; Nanjing: 59.43.130.158, 59.43.139.113, 59.43.248.250 | [查看](https://globalping.io?measurement=2atDXEVXmL0F9BUpP00020wER) |
| `198.44.182.190` | 443 | HK/HKG | AS62468 | 1295 ms | Beijing: 59.43.46.82 | [查看](https://globalping.io?measurement=2LQdiR7UfeucmtKY900020wES) |
| `216.23.116.10` | 443 | HK/HKG | AS42960 | 1158 ms | Nanjing: 59.43.139.129, 59.43.22.33 | [查看](https://globalping.io?measurement=2awf7T9yTuSvWkSJb00020wEu) |
| `38.147.173.236` | 443 | HK/HKG | AS139659 | 1075 ms | Guangzhou: 59.43.183.110; Shenzhen: 59.43.248.246 | [查看](https://globalping.io?measurement=2aGa2IYetdjuMRsV600020wEm) |
| `38.207.133.44` | 443 | HK/HKG | AS6134 | 989 ms | Guangzhou: 59.43.248.250, 59.43.250.170; Nanjing: 59.43.139.117, 59.43.248.250; Beijing: 59.43.246.226; Xi'an: 59.43.248.250, 59.43.93.109 | [查看](https://globalping.io?measurement=20sTzpgv7jAhGiGBW00020wEi) |
| `38.76.181.100` | 443 | HK/HKG | AS401701 | 1000 ms | Guangzhou: 59.43.183.110; Nanjing: 59.43.139.117, 59.43.183.110; Beijing: 59.43.181.210, 59.43.19.94, 59.43.246.226; Xi'an: 59.43.137.241, 59.43.188.122 | [查看](https://globalping.io?measurement=2tfTm9ejYMpiEi4Ku00020wEj) |
| `45.131.179.101` | 443 | HK/HKG | AS6134 | 1085 ms | Guangzhou: 59.43.130.126 | [查看](https://globalping.io?measurement=2HDF6XBtsj59bOqo500020wEn) |
| `68.64.182.121` | 443 | HK/HKG | AS139659 | 1008 ms | Guangzhou: 59.43.248.250; Nanjing: 59.43.139.113, 59.43.248.246; Xi'an: 59.43.188.122, 59.43.93.109 | [查看](https://globalping.io?measurement=2i5PdfyPYYRsgSUR100020wEj) |
| `43.159.4.80` | 443 | SG/SIN | AS132203 | 999 ms | Nanjing: 59.43.132.153 | [查看](https://globalping.io?measurement=29AtQBn00L1V1R3C200020wEj) |
| `103.143.81.178` | 443 | HK/HKG | AS139659 | 983 ms | Nanjing: 59.43.139.109, 59.43.248.250; Beijing: 59.43.246.226 | [查看](https://globalping.io?measurement=2Kn6eo2bcmlLzRYTD00020wEi) |
| `156.239.12.210` | 443 | HK/HKG | AS154321 | 1161 ms | Guangzhou: 59.43.183.110; Nanjing: 59.43.139.117, 59.43.248.250, 59.43.250.50 | [查看](https://globalping.io?measurement=2ETnrcuAQ5F2u06YD00020wEP) |
| `165.154.20.213` | 443 | HK/HKG | AS135377 | 3503 ms | Xi'an: 59.43.156.129 | [查看](https://globalping.io?measurement=2NwI4Ze38yVhBR39600020wEP) |
| `193.134.209.123` | 443 | HK/HKG | AS139659 | 1244 ms | Guangzhou: 59.43.248.246; Nanjing: 59.43.139.117, 59.43.248.250 | [查看](https://globalping.io?measurement=2NFwZUFDzH4BFXkEK00020wEK) |
| `38.207.164.126` | 443 | HK/HKG | AS967 | 995 ms | Guangzhou: 59.43.188.122; Nanjing: 59.43.139.109, 59.43.248.246; Beijing: 59.43.181.222, 59.43.246.226 | [查看](https://globalping.io?measurement=2WZK2j3AZtkAnR32x00020wEi) |
| `68.64.182.79` | 443 | HK/HKG | AS139659 | 1256 ms | Guangzhou: 59.43.248.246; Nanjing: 59.43.139.109, 59.43.248.246; Nanjing: 59.43.139.109, 59.43.183.110 | [查看](https://globalping.io?measurement=27qOEvbWcyQ0hRwyq00020w5b) |
| `38.207.177.204` | 443 | HK/HKG | AS139659 | 1216 ms | Nanjing: 59.43.130.122, 59.43.139.117, 59.43.248.246; Nanjing: 59.43.123.89, 59.43.188.122 | [查看](https://globalping.io?measurement=2Nu40TJGXzkCPLi8000020w5c) |
| `43.160.254.163` | 443 | SG/SIN | AS132203 | 2290 ms | Nanjing: 59.43.139.117 | [查看](https://globalping.io?measurement=2Hg4PXQzKGJNyRjR700020wEP) |
| `82.158.88.94` | 443 | HK/HKG | AS401701 | 1179 ms | Guangzhou: 59.43.183.110; Nanjing: 59.43.139.129, 59.43.183.110; Beijing: 59.43.183.122, 59.43.248.2; Xi'an: 59.43.137.241, 59.43.188.122 | [查看](https://globalping.io?measurement=2MoUn7gsFJdC3BnLz00020wES) |
| `150.109.11.223` | 443 | SG/SIN | AS132203 | 2669 ms | Nanjing: 59.43.139.129; Beijing: 59.43.145.62, 59.43.22.41; Xi'an: 59.43.137.241 | [查看](https://globalping.io?measurement=26FEmuI702JMATYME00020wEO) |
| `43.160.209.30` | 443 | SG/SIN | AS132203 | 2248 ms | Nanjing: 59.43.139.109; Xi'an: 59.43.137.241 | [查看](https://globalping.io?measurement=2IIkBo0KB5IV0xrl500020wEO) |
| `43.160.240.180` | 443 | SG/SIN | AS132203 | 1156 ms | Nanjing: 59.43.130.126, 59.43.139.117 | [查看](https://globalping.io?measurement=2IABIyi079OhY0s0E00020wEt) |
| `43.156.142.191` | 443 | SG/SIN | AS132203 | 1601 ms | Nanjing: 59.43.139.113 | [查看](https://globalping.io?measurement=20h2UogvgwUaboyCo00020wEO) |
| `43.160.197.205` | 443 | SG/SIN | AS132203 | 1098 ms | Nanjing: 59.43.139.109 | [查看](https://globalping.io?measurement=2KT94gubBZQWEKhyF00020wEo) |
| `43.160.253.225` | 443 | SG/SIN | AS132203 | 2296 ms | Nanjing: 59.43.139.117 | [查看](https://globalping.io?measurement=2d5yRvREhWyGxkFzQ00020wEM) |
| `111.119.193.50` | 443 | SG/SIN | AS136907 | 1879 ms | Guangzhou: 59.43.130.102; Nanjing: 59.43.39.118, 59.43.46.101; Beijing: 59.43.159.18, 59.43.46.82 | [查看](https://globalping.io?measurement=2whzoXU1xDkzVQVJr00020w5c) |
| `43.156.23.85` | 443 | SG/SIN | AS132203 | 2388 ms | Guangzhou: 59.43.250.50; Nanjing: 59.43.139.109, 59.43.16.166 | [查看](https://globalping.io?measurement=2bPYUg7gIR76yVGed00020w5l) |
| `191.222.212.77` | 443 | JP/NRT | AS906 | 1262 ms | Guangzhou: 59.43.130.194, 59.43.144.209; Nanjing: 59.43.139.133 | [查看](https://globalping.io?measurement=2EqHVS3p3juopEHaZ00020wEO) |
| `82.40.33.62` | 443 | JP/NRT | AS400618 | 1146 ms | Guangzhou: 59.43.144.209, 59.43.246.26; Nanjing: 59.43.246.26; Beijing: 59.43.138.54, 59.43.183.2, 59.43.46.82 | [查看](https://globalping.io?measurement=2I9wMX37IiGgESj8300020wEs) |
| `207.56.227.33` | 443 | JP/NRT | AS140227 | 1128 ms | Guangzhou: 59.43.183.2, 59.43.22.6, 59.43.46.77; Nanjing: 59.43.139.137, 59.43.159.18, 59.43.183.2, 59.43.39.130 | [查看](https://globalping.io?measurement=26kHW3PfBvhTc09zp00020wER) |
| `154.64.246.151` | 443 | HK/HKG | AS979 | 1334 ms | Nanjing: 59.43.139.109, 59.43.188.122; Shenzhen: 59.43.188.122 | [查看](https://globalping.io?measurement=2yzg8AxKvZs4cbX1L00020wEI) |
| `64.90.24.26` | 443 | HK/HKG | AS979 | 1867 ms | Nanjing: 59.43.132.149; Xi'an: 59.43.156.129 | [查看](https://globalping.io?measurement=27uSTgcGacpPHUc6M00020wER) |
