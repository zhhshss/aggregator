# CN2 代理筛选报告

- CSV 地区候选数：3045
- 经百度前置测试数：3045
- 可用数：1729
- 已完成路由追踪：191
- 待路由追踪：1543
- CN2 路由确认数：58

判断标准：经给定百度 HTTP CONNECT 前置可连接目标代理，且中国电信探针的回程 traceroute 出现 `59.43.0.0/16`。

| IP | 端口 | 地区 | ASN | 延迟 | CN2 证据 | 路由 |
|---|---:|---|---:|---:|---|---|
| `202.55.27.177` | 443 | JP/NRT | AS4809 | 3149 ms | Guangzhou: 59.43.144.209, 59.43.246.26, 59.43.39.190; Nanjing: 59.43.139.133, 59.43.186.186; Beijing: 59.43.183.2, 59.43.39.98, 59.43.46.82 | [查看](https://globalping.io?measurement=21pqJP54vnfweuTe800020w5Y) |
| `216.38.170.102` | 443 | HK/SIN | AS4515 | 1237 ms | Guangzhou: 59.43.248.202; Nanjing: 59.43.187.182, 59.43.42.33 | [查看](https://globalping.io?measurement=2PXGIqYnkaHwNxcIk00020wF6) |
| `38.175.192.154` | 443 | HK/HKG | AS979 | 1475 ms | Nanjing: 59.43.123.89, 59.43.22.41, 59.43.248.246; Nanjing: 59.43.139.113, 59.43.16.166, 59.43.183.110 | [查看](https://globalping.io?measurement=2paAxP5Apm2uTj5kU00020w5c) |
| `64.90.24.236` | 443 | HK/HKG | AS979 | 1415 ms | Guangzhou: 59.43.130.154; Nanjing: 59.43.39.190, 59.43.46.97; Nanjing: 59.43.132.153, 59.43.39.178 | [查看](https://globalping.io?measurement=2LW64WJZw3Ho7TL9f00020w5l) |
| `82.158.230.241` | 443 | HK/HKG | AS401701 | 1090 ms | Nanjing: 59.43.139.109, 59.43.248.250 | [查看](https://globalping.io?measurement=2x7U9XjJoZtELZ34F00020wF6) |
| `82.158.91.93` | 443 | HK/HKG | AS401701 | 1224 ms | Xi'an: 59.43.183.110, 59.43.93.109 | [查看](https://globalping.io?measurement=2APU5OeQbZfEQslJa00020wEn) |
| `103.24.219.134` | 443 | HK/HKG | AS42960 | 1662 ms | Guangzhou: 59.43.16.166, 59.43.248.250; Nanjing: 59.43.139.117, 59.43.183.110, 59.43.22.33; Beijing: 59.43.182.110, 59.43.19.98, 59.43.246.226 | [查看](https://globalping.io?measurement=2LgBXxuyqqe2oceQT00020w5d) |
| `103.242.15.87` | 443 | HK/HKG | AS401696 | 2229 ms | Nanjing: 59.43.39.118, 59.43.46.101; Nanjing: 59.43.130.210, 59.43.139.137 | [查看](https://globalping.io?measurement=23haVCSxjawO0Gq4h00020w5g) |
| `149.104.2.56` | 443 | HK/HKG | AS932 | 1183 ms | Beijing: 59.43.138.58, 59.43.181.54, 59.43.46.86; Xi'an: 59.43.181.54, 59.43.46.157 | [查看](https://globalping.io?measurement=2P5OSxTtxelpqMLCh00020wES) |
| `149.104.31.208` | 443 | HK/HKG | AS139659 | 1687 ms | Guangzhou: 59.43.16.166, 59.43.183.110; Nanjing: 59.43.130.158, 59.43.139.113, 59.43.248.250 | [查看](https://globalping.io?measurement=2atDXEVXmL0F9BUpP00020wER) |
| `149.104.5.234` | 443 | HK/HKG | AS42960 | 1223 ms | Guangzhou: 59.43.130.118, 59.43.188.122, 59.43.250.170; Nanjing: 59.43.188.122, 59.43.42.33; Beijing: 59.43.132.30, 59.43.246.226, 59.43.38.118 | [查看](https://globalping.io?measurement=2NZx4FSJYmjxg0bAt00020wF6) |
| `149.104.6.15` | 443 | HK/HKG | AS42960 | 1239 ms | Guangzhou: 59.43.181.14; Nanjing: 59.43.138.46, 59.43.38.166, 59.43.46.101; Beijing: 59.43.46.82 | [查看](https://globalping.io?measurement=2ir6njNYFniL2myAr00020wF6) |
| `154.219.104.79` | 443 | HK/HKG | AS401701 | 1191 ms | Guangzhou: 59.43.248.250; Nanjing: 59.43.139.109, 59.43.188.122; Guangzhou: 59.43.248.250 | [查看](https://globalping.io?measurement=2aeN9ouECE4UrSX5s00020wF6) |
| `185.216.118.161` | 443 | HK/HKG | AS55933 | 1156 ms | Guangzhou: 59.43.183.110; Nanjing: 59.43.139.129, 59.43.188.122 | [查看](https://globalping.io?measurement=21wE5m4pwUrgfTLHk00020wF6) |
| `198.44.182.190` | 443 | HK/HKG | AS62468 | 1140 ms | Beijing: 59.43.46.82 | [查看](https://globalping.io?measurement=2LQdiR7UfeucmtKY900020wES) |
| `216.23.116.10` | 443 | HK/HKG | AS42960 | 1287 ms | Nanjing: 59.43.139.129, 59.43.22.33 | [查看](https://globalping.io?measurement=2awf7T9yTuSvWkSJb00020wEu) |
| `38.147.173.236` | 443 | HK/HKG | AS139659 | 1140 ms | Guangzhou: 59.43.183.110; Shenzhen: 59.43.248.246 | [查看](https://globalping.io?measurement=2aGa2IYetdjuMRsV600020wEm) |
| `38.207.133.44` | 443 | HK/HKG | AS6134 | 2093 ms | Guangzhou: 59.43.248.250, 59.43.250.170; Nanjing: 59.43.139.117, 59.43.248.250; Beijing: 59.43.246.226; Xi'an: 59.43.248.250, 59.43.93.109 | [查看](https://globalping.io?measurement=20sTzpgv7jAhGiGBW00020wEi) |
| `38.76.181.100` | 443 | HK/HKG | AS401701 | 1040 ms | Guangzhou: 59.43.183.110; Nanjing: 59.43.139.117, 59.43.183.110; Beijing: 59.43.181.210, 59.43.19.94, 59.43.246.226; Xi'an: 59.43.137.241, 59.43.188.122 | [查看](https://globalping.io?measurement=2tfTm9ejYMpiEi4Ku00020wEj) |
| `45.131.179.101` | 443 | HK/HKG | AS6134 | 2421 ms | Guangzhou: 59.43.130.126 | [查看](https://globalping.io?measurement=2HDF6XBtsj59bOqo500020wEn) |
| `68.64.182.121` | 443 | HK/HKG | AS139659 | 1364 ms | Guangzhou: 59.43.248.250; Nanjing: 59.43.139.113, 59.43.248.246; Xi'an: 59.43.188.122, 59.43.93.109 | [查看](https://globalping.io?measurement=2i5PdfyPYYRsgSUR100020wEj) |
| `68.64.182.205` | 443 | HK/HKG | AS139659 | 1192 ms | Guangzhou: 59.43.188.122; Nanjing: 59.43.139.113, 59.43.188.122 | [查看](https://globalping.io?measurement=2hKLJq2QZUIqO49JX00020wF6) |
| `43.159.4.80` | 443 | SG/SIN | AS132203 | 1705 ms | Nanjing: 59.43.132.153 | [查看](https://globalping.io?measurement=29AtQBn00L1V1R3C200020wEj) |
| `103.143.81.178` | 443 | HK/HKG | AS139659 | 1776 ms | Nanjing: 59.43.139.109, 59.43.248.250; Beijing: 59.43.246.226 | [查看](https://globalping.io?measurement=2Kn6eo2bcmlLzRYTD00020wEi) |
| `149.104.30.51` | 443 | HK/HKG | AS139659 | 1230 ms | Guangzhou: 59.43.248.250; Nanjing: 59.43.123.89, 59.43.130.162, 59.43.188.122; Beijing: 59.43.183.118, 59.43.19.98, 59.43.248.2 | [查看](https://globalping.io?measurement=2ZkBeGKCQPaa0Zl8a00020wF6) |
| `156.239.12.210` | 443 | HK/HKG | AS154321 | 3019 ms | Guangzhou: 59.43.183.110; Nanjing: 59.43.139.117, 59.43.248.250, 59.43.250.50 | [查看](https://globalping.io?measurement=2ETnrcuAQ5F2u06YD00020wEP) |
| `165.154.20.213` | 443 | HK/HKG | AS135377 | 1529 ms | Xi'an: 59.43.156.129 | [查看](https://globalping.io?measurement=2NwI4Ze38yVhBR39600020wEP) |
| `193.134.209.123` | 443 | HK/HKG | AS139659 | 1103 ms | Guangzhou: 59.43.248.246; Nanjing: 59.43.139.117, 59.43.248.250 | [查看](https://globalping.io?measurement=2NFwZUFDzH4BFXkEK00020wEK) |
| `38.207.164.126` | 443 | HK/HKG | AS967 | 3766 ms | Guangzhou: 59.43.188.122; Nanjing: 59.43.139.109, 59.43.248.246; Beijing: 59.43.181.222, 59.43.246.226 | [查看](https://globalping.io?measurement=2WZK2j3AZtkAnR32x00020wEi) |
| `38.55.192.142` | 443 | HK/HKG | AS139659 | 1177 ms | Guangzhou: 59.43.188.122; Nanjing: 59.43.139.109, 59.43.248.246 | [查看](https://globalping.io?measurement=2XbBrH5J4NlBEBp9J00020wF6) |
| `68.64.182.79` | 443 | HK/HKG | AS139659 | 1253 ms | Guangzhou: 59.43.248.246; Nanjing: 59.43.139.109, 59.43.248.246; Nanjing: 59.43.139.109, 59.43.183.110 | [查看](https://globalping.io?measurement=27qOEvbWcyQ0hRwyq00020w5b) |
| `165.154.21.142` | 443 | HK/HKG | AS135377 | 1239 ms | Guangzhou: 59.43.250.50; Nanjing: 59.43.139.137 | [查看](https://globalping.io?measurement=2EQh1zOqacEfIa8AB00020wF7) |
| `45.152.65.100` | 443 | HK/HKG | AS139659 | 1155 ms | Guangzhou: 59.43.183.110; Nanjing: 59.43.139.109, 59.43.183.110 | [查看](https://globalping.io?measurement=2M9l2WN9GGQ0KjE7o00020wF6) |
| `38.207.177.204` | 443 | HK/HKG | AS139659 | 1272 ms | Nanjing: 59.43.130.122, 59.43.139.117, 59.43.248.246; Nanjing: 59.43.123.89, 59.43.188.122 | [查看](https://globalping.io?measurement=2Nu40TJGXzkCPLi8000020w5c) |
| `43.160.254.163` | 443 | SG/SIN | AS132203 | 1154 ms | Nanjing: 59.43.139.117 | [查看](https://globalping.io?measurement=2Hg4PXQzKGJNyRjR700020wEP) |
| `82.158.88.94` | 443 | HK/HKG | AS401701 | 1612 ms | Guangzhou: 59.43.183.110; Nanjing: 59.43.139.129, 59.43.183.110; Beijing: 59.43.183.122, 59.43.248.2; Xi'an: 59.43.137.241, 59.43.188.122 | [查看](https://globalping.io?measurement=2MoUn7gsFJdC3BnLz00020wES) |
| `150.109.11.223` | 443 | SG/SIN | AS132203 | 2430 ms | Nanjing: 59.43.139.129; Beijing: 59.43.145.62, 59.43.22.41; Xi'an: 59.43.137.241 | [查看](https://globalping.io?measurement=26FEmuI702JMATYME00020wEO) |
| `43.160.209.30` | 443 | SG/SIN | AS132203 | 1765 ms | Nanjing: 59.43.139.109; Xi'an: 59.43.137.241 | [查看](https://globalping.io?measurement=2IIkBo0KB5IV0xrl500020wEO) |
| `43.160.240.180` | 443 | SG/SIN | AS132203 | 1337 ms | Nanjing: 59.43.130.126, 59.43.139.117 | [查看](https://globalping.io?measurement=2IABIyi079OhY0s0E00020wEt) |
| `45.194.18.109` | 443 | SG/SIN | AS137535 | 1107 ms | Nanjing: 59.43.139.129, 59.43.16.182 | [查看](https://globalping.io?measurement=2quu38VadGanRObfq00020wF6) |
| `43.156.142.191` | 443 | SG/SIN | AS132203 | 2235 ms | Nanjing: 59.43.139.113 | [查看](https://globalping.io?measurement=20h2UogvgwUaboyCo00020wEO) |
| `43.160.197.205` | 443 | SG/SIN | AS132203 | 1596 ms | Nanjing: 59.43.139.109 | [查看](https://globalping.io?measurement=2KT94gubBZQWEKhyF00020wEo) |
| `43.160.253.225` | 443 | SG/SIN | AS132203 | 1761 ms | Nanjing: 59.43.139.117 | [查看](https://globalping.io?measurement=2d5yRvREhWyGxkFzQ00020wEM) |
| `111.119.193.50` | 443 | SG/SIN | AS136907 | 2585 ms | Guangzhou: 59.43.130.102; Nanjing: 59.43.39.118, 59.43.46.101; Beijing: 59.43.159.18, 59.43.46.82 | [查看](https://globalping.io?measurement=2whzoXU1xDkzVQVJr00020w5c) |
| `43.156.23.85` | 443 | SG/SIN | AS132203 | 2346 ms | Guangzhou: 59.43.250.50; Nanjing: 59.43.139.109, 59.43.16.166 | [查看](https://globalping.io?measurement=2bPYUg7gIR76yVGed00020w5l) |
| `191.222.209.238` | 443 | JP/NRT | AS906 | 1100 ms | Guangzhou: 59.43.159.98; Nanjing: 59.43.132.149, 59.43.39.234 | [查看](https://globalping.io?measurement=2HvGPlVYGCbu4FfBF00020wF6) |
| `191.222.212.153` | 443 | JP/NRT | AS906 | 1113 ms | Guangzhou: 59.43.144.209; Nanjing: 59.43.139.133; Beijing: 59.43.138.54, 59.43.46.82 | [查看](https://globalping.io?measurement=2TlwLfz6LcPHMJNSB00020wF6) |
| `64.83.40.57` | 443 | JP/NRT | AS979 | 1103 ms | Guangzhou: 59.43.137.226; Nanjing: 59.43.139.133, 59.43.39.118; Guangzhou: 59.43.138.70, 59.43.144.209, 59.43.181.50 | [查看](https://globalping.io?measurement=2k2wswi3LgLh8gcBe00020wF6) |
| `191.222.212.77` | 443 | JP/NRT | AS906 | 1071 ms | Guangzhou: 59.43.130.194, 59.43.144.209; Nanjing: 59.43.139.133 | [查看](https://globalping.io?measurement=2EqHVS3p3juopEHaZ00020wEO) |
| `82.40.33.173` | 443 | JP/NRT | AS400618 | 1236 ms | Guangzhou: 59.43.141.146, 59.43.183.2, 59.43.247.186; Nanjing: 59.43.183.2; Beijing: 59.43.246.26, 59.43.46.82; Guangzhou: 59.43.138.46, 59.43.246.26, 59.43.46.77 | [查看](https://globalping.io?measurement=2WzPJmyeibciCZEJu00020wF6) |
| `82.40.33.62` | 443 | JP/NRT | AS400618 | 1332 ms | Guangzhou: 59.43.144.209, 59.43.246.26; Nanjing: 59.43.246.26; Beijing: 59.43.138.54, 59.43.183.2, 59.43.46.82 | [查看](https://globalping.io?measurement=2I9wMX37IiGgESj8300020wEs) |
| `142.248.139.25` | 443 | JP/NRT | AS140227 | 1039 ms | Guangzhou: 59.43.144.209, 59.43.183.2; Nanjing: 59.43.132.153, 59.43.246.26; Beijing: 59.43.246.26, 59.43.46.82 | [查看](https://globalping.io?measurement=2qw332P8VMNJilgtM00020wF6) |
| `207.56.227.33` | 443 | JP/NRT | AS140227 | 3192 ms | Guangzhou: 59.43.183.2, 59.43.22.6, 59.43.46.77; Nanjing: 59.43.139.137, 59.43.159.18, 59.43.183.2, 59.43.39.130 | [查看](https://globalping.io?measurement=26kHW3PfBvhTc09zp00020wER) |
| `38.47.198.28` | 443 | JP/NRT | AS140227 | 1076 ms | Guangzhou: 59.43.130.194, 59.43.246.26; Nanjing: 59.43.130.190, 59.43.132.153, 59.43.183.2 | [查看](https://globalping.io?measurement=2oZ73TJqD3bAwxaaH00020wF6) |
| `154.64.246.151` | 443 | HK/HKG | AS979 | 3489 ms | Nanjing: 59.43.139.109, 59.43.188.122; Shenzhen: 59.43.188.122 | [查看](https://globalping.io?measurement=2yzg8AxKvZs4cbX1L00020wEI) |
| `38.47.213.57` | 443 | HK/HKG | AS140227 | 983 ms | Nanjing: 59.43.132.153 | [查看](https://globalping.io?measurement=2Msh7cmr25nWGHlXo00020wF6) |
| `64.90.24.26` | 443 | HK/HKG | AS979 | 3249 ms | Nanjing: 59.43.132.149; Xi'an: 59.43.156.129 | [查看](https://globalping.io?measurement=27uSTgcGacpPHUc6M00020wER) |
| `64.90.28.28` | 443 | HK/HKG | AS61112 | 1190 ms | Guangzhou: 59.43.187.182; Nanjing: 59.43.139.129, 59.43.183.106 | [查看](https://globalping.io?measurement=2lAE0HrZAmtwuZZNy00020wF6) |
