# CN2 代理筛选报告

- CSV 地区候选数：3045
- 经百度前置测试数：3045
- 可用数：1718
- 已完成路由追踪：377
- 待路由追踪：1356
- CN2 路由确认数：103

判断标准：经给定百度 HTTP CONNECT 前置可连接目标代理，且中国电信探针的回程 traceroute 出现 `59.43.0.0/16`。

| IP | 端口 | 地区 | ASN | 延迟 | CN2 证据 | 路由 |
|---|---:|---|---:|---:|---|---|
| `202.55.27.177` | 443 | JP/NRT | AS4809 | 2721 ms | Guangzhou: 59.43.144.209, 59.43.246.26, 59.43.39.190; Nanjing: 59.43.139.133, 59.43.186.186; Beijing: 59.43.183.2, 59.43.39.98, 59.43.46.82 | [查看](https://globalping.io?measurement=21pqJP54vnfweuTe800020w5Y) |
| `191.222.216.163` | 443 | HK/HKG | AS906 | 3070 ms | Shenzhen: 59.43.250.54 | [查看](https://globalping.io?measurement=2Zt8Z91aP5UrDYD5L00020wFc) |
| `216.38.170.102` | 443 | HK/SIN | AS4515 | 2321 ms | Guangzhou: 59.43.248.202; Nanjing: 59.43.187.182, 59.43.42.33 | [查看](https://globalping.io?measurement=2PXGIqYnkaHwNxcIk00020wF6) |
| `23.26.201.245` | 443 | HK/HKG | AS149440 | 1266 ms | Nanjing: 59.43.123.89, 59.43.22.41; Beijing: 59.43.145.62, 59.43.22.41 | [查看](https://globalping.io?measurement=2G5gN5x8LiSZOTYe500020wFk) |
| `38.175.192.154` | 443 | HK/HKG | AS979 | 3561 ms | Nanjing: 59.43.123.89, 59.43.22.41, 59.43.248.246; Nanjing: 59.43.139.113, 59.43.16.166, 59.43.183.110 | [查看](https://globalping.io?measurement=2paAxP5Apm2uTj5kU00020w5c) |
| `50.114.59.134` | 443 | HK/HKG | AS149440 | 3063 ms | Nanjing: 59.43.139.117 | [查看](https://globalping.io?measurement=25hrLoaiMkVyceII300020wFF) |
| `64.90.24.236` | 443 | HK/HKG | AS979 | 1532 ms | Guangzhou: 59.43.130.154; Nanjing: 59.43.39.190, 59.43.46.97; Nanjing: 59.43.132.153, 59.43.39.178 | [查看](https://globalping.io?measurement=2LW64WJZw3Ho7TL9f00020w5l) |
| `82.158.230.241` | 443 | HK/HKG | AS401701 | 2377 ms | Nanjing: 59.43.139.109, 59.43.248.250 | [查看](https://globalping.io?measurement=2x7U9XjJoZtELZ34F00020wF6) |
| `82.158.91.93` | 443 | HK/HKG | AS401701 | 1620 ms | Xi'an: 59.43.183.110, 59.43.93.109 | [查看](https://globalping.io?measurement=2APU5OeQbZfEQslJa00020wEn) |
| `103.24.219.134` | 443 | HK/HKG | AS42960 | 2522 ms | Guangzhou: 59.43.16.166, 59.43.248.250; Nanjing: 59.43.139.117, 59.43.183.110, 59.43.22.33; Beijing: 59.43.182.110, 59.43.19.98, 59.43.246.226 | [查看](https://globalping.io?measurement=2LgBXxuyqqe2oceQT00020w5d) |
| `103.242.15.87` | 443 | HK/HKG | AS401696 | 1837 ms | Nanjing: 59.43.39.118, 59.43.46.101; Nanjing: 59.43.130.210, 59.43.139.137 | [查看](https://globalping.io?measurement=23haVCSxjawO0Gq4h00020w5g) |
| `149.104.2.56` | 443 | HK/HKG | AS932 | 2659 ms | Beijing: 59.43.138.58, 59.43.181.54, 59.43.46.86; Xi'an: 59.43.181.54, 59.43.46.157 | [查看](https://globalping.io?measurement=2P5OSxTtxelpqMLCh00020wES) |
| `149.104.3.16` | 443 | HK/HKG | AS42960 | 2363 ms | Guangzhou: 59.43.183.110; Beijing: 59.43.132.26, 59.43.248.2, 59.43.38.130 | [查看](https://globalping.io?measurement=2ZXpmVrHgq6HFqHna00020wFF) |
| `149.104.3.97` | 443 | HK/HKG | AS42960 | 1268 ms | Beijing: 59.43.19.98, 59.43.246.226 | [查看](https://globalping.io?measurement=2aOiuYWLp5GQcnK8U00020wFc) |
| `149.104.31.208` | 443 | HK/HKG | AS139659 | 1820 ms | Guangzhou: 59.43.16.166, 59.43.183.110; Nanjing: 59.43.130.158, 59.43.139.113, 59.43.248.250 | [查看](https://globalping.io?measurement=2atDXEVXmL0F9BUpP00020wER) |
| `149.104.5.234` | 443 | HK/HKG | AS42960 | 2213 ms | Guangzhou: 59.43.130.118, 59.43.188.122, 59.43.250.170; Nanjing: 59.43.188.122, 59.43.42.33; Beijing: 59.43.132.30, 59.43.246.226, 59.43.38.118 | [查看](https://globalping.io?measurement=2NZx4FSJYmjxg0bAt00020wF6) |
| `149.104.6.130` | 443 | HK/HKG | AS42960 | 1265 ms | Nanjing: 59.43.159.18, 59.43.46.101; Shenzhen: 59.43.130.110 | [查看](https://globalping.io?measurement=2mkcN3bgOuwq2wLe400020wFF) |
| `149.104.6.15` | 443 | HK/HKG | AS42960 | 4392 ms | Guangzhou: 59.43.181.14; Nanjing: 59.43.138.46, 59.43.38.166, 59.43.46.101; Beijing: 59.43.46.82 | [查看](https://globalping.io?measurement=2ir6njNYFniL2myAr00020wF6) |
| `154.219.104.79` | 443 | HK/HKG | AS401701 | 1200 ms | Guangzhou: 59.43.248.250; Nanjing: 59.43.139.109, 59.43.188.122; Guangzhou: 59.43.248.250 | [查看](https://globalping.io?measurement=2aeN9ouECE4UrSX5s00020wF6) |
| `185.216.118.161` | 443 | HK/HKG | AS55933 | 8206 ms | Guangzhou: 59.43.183.110; Nanjing: 59.43.139.129, 59.43.188.122 | [查看](https://globalping.io?measurement=21wE5m4pwUrgfTLHk00020wF6) |
| `193.134.209.165` | 443 | HK/HKG | AS139659 | 1379 ms | Guangzhou: 59.43.248.246; Beijing: 59.43.183.118, 59.43.248.2 | [查看](https://globalping.io?measurement=25PJ2JNtuTityu0X100020wFc) |
| `198.44.182.190` | 443 | HK/HKG | AS62468 | 1689 ms | Beijing: 59.43.46.82 | [查看](https://globalping.io?measurement=2LQdiR7UfeucmtKY900020wES) |
| `216.23.116.10` | 443 | HK/HKG | AS42960 | 2187 ms | Nanjing: 59.43.139.129, 59.43.22.33 | [查看](https://globalping.io?measurement=2awf7T9yTuSvWkSJb00020wEu) |
| `38.147.173.136` | 443 | HK/HKG | AS139659 | 1233 ms | Guangzhou: 59.43.130.114, 59.43.248.250; Nanjing: 59.43.139.109, 59.43.248.246 | [查看](https://globalping.io?measurement=2tAqVWl7GOXWHrtl500020wFk) |
| `38.147.173.236` | 443 | HK/HKG | AS139659 | 1364 ms | Guangzhou: 59.43.183.110; Shenzhen: 59.43.248.246 | [查看](https://globalping.io?measurement=2aGa2IYetdjuMRsV600020wEm) |
| `38.207.133.44` | 443 | HK/HKG | AS6134 | 2618 ms | Guangzhou: 59.43.248.250, 59.43.250.170; Nanjing: 59.43.139.117, 59.43.248.250; Beijing: 59.43.246.226; Xi'an: 59.43.248.250, 59.43.93.109 | [查看](https://globalping.io?measurement=20sTzpgv7jAhGiGBW00020wEi) |
| `38.55.107.239` | 443 | HK/HKG | AS967 | 1264 ms | Guangzhou: 59.43.183.110; Nanjing: 59.43.139.129, 59.43.183.110; Beijing: 59.43.132.26, 59.43.248.2, 59.43.38.130 | [查看](https://globalping.io?measurement=24K1SxKAFUCCtsQU800020wFE) |
| `38.55.97.172` | 443 | HK/HKG | AS42960 | 1293 ms | Nanjing: 59.43.132.149; Beijing: 59.43.247.226 | [查看](https://globalping.io?measurement=2TPLZqu1XOoXSqdoX00020wFF) |
| `38.76.181.100` | 443 | HK/HKG | AS401701 | 2090 ms | Guangzhou: 59.43.183.110; Nanjing: 59.43.139.117, 59.43.183.110; Beijing: 59.43.181.210, 59.43.19.94, 59.43.246.226; Xi'an: 59.43.137.241, 59.43.188.122 | [查看](https://globalping.io?measurement=2tfTm9ejYMpiEi4Ku00020wEj) |
| `45.131.179.101` | 443 | HK/HKG | AS6134 | 1244 ms | Guangzhou: 59.43.130.126 | [查看](https://globalping.io?measurement=2HDF6XBtsj59bOqo500020wEn) |
| `45.145.229.223` | 443 | HK/HKG | AS139659 | 1185 ms | Guangzhou: 59.43.16.166, 59.43.181.14, 59.43.183.110; Nanjing: 59.43.139.117, 59.43.248.250; Beijing: 59.43.19.94, 59.43.248.2; Nanjing: 59.43.139.109 | [查看](https://globalping.io?measurement=2QbOKhdYHoO67MNhJ00020wFF) |
| `68.64.179.129` | 443 | HK/HKG | AS139659 | 2152 ms | Guangzhou: 59.43.188.122, 59.43.250.110; Beijing: 59.43.181.222, 59.43.246.226; Shenzhen: 59.43.183.110 | [查看](https://globalping.io?measurement=2BP1oPeBmSDFB2wE300020wFF) |
| `68.64.182.121` | 443 | HK/HKG | AS139659 | 1666 ms | Guangzhou: 59.43.248.250; Nanjing: 59.43.139.113, 59.43.248.246; Xi'an: 59.43.188.122, 59.43.93.109 | [查看](https://globalping.io?measurement=2i5PdfyPYYRsgSUR100020wEj) |
| `68.64.182.205` | 443 | HK/HKG | AS139659 | 2169 ms | Guangzhou: 59.43.188.122; Nanjing: 59.43.139.113, 59.43.188.122 | [查看](https://globalping.io?measurement=2hKLJq2QZUIqO49JX00020wF6) |
| `83.229.127.224` | 443 | HK/HKG | AS139659 | 3023 ms | Guangzhou: 59.43.16.166, 59.43.248.246; Nanjing: 59.43.248.246, 59.43.42.33; Beijing: 59.43.132.26, 59.43.248.2, 59.43.38.126 | [查看](https://globalping.io?measurement=2ncIvuNXz1ja3ZdjS00020wFE) |
| `43.159.4.80` | 443 | SG/SIN | AS132203 | 2781 ms | Nanjing: 59.43.132.153 | [查看](https://globalping.io?measurement=29AtQBn00L1V1R3C200020wEj) |
| `103.143.81.178` | 443 | HK/HKG | AS139659 | 2574 ms | Nanjing: 59.43.139.109, 59.43.248.250; Beijing: 59.43.246.226 | [查看](https://globalping.io?measurement=2Kn6eo2bcmlLzRYTD00020wEi) |
| `149.104.30.51` | 443 | HK/HKG | AS139659 | 1318 ms | Guangzhou: 59.43.248.250; Nanjing: 59.43.123.89, 59.43.130.162, 59.43.188.122; Beijing: 59.43.183.118, 59.43.19.98, 59.43.248.2 | [查看](https://globalping.io?measurement=2ZkBeGKCQPaa0Zl8a00020wF6) |
| `156.239.12.210` | 443 | HK/HKG | AS154321 | 2836 ms | Guangzhou: 59.43.183.110; Nanjing: 59.43.139.117, 59.43.248.250, 59.43.250.50 | [查看](https://globalping.io?measurement=2ETnrcuAQ5F2u06YD00020wEP) |
| `165.154.20.213` | 443 | HK/HKG | AS135377 | 2322 ms | Xi'an: 59.43.156.129 | [查看](https://globalping.io?measurement=2NwI4Ze38yVhBR39600020wEP) |
| `193.134.209.123` | 443 | HK/HKG | AS139659 | 1256 ms | Guangzhou: 59.43.248.246; Nanjing: 59.43.139.117, 59.43.248.250 | [查看](https://globalping.io?measurement=2NFwZUFDzH4BFXkEK00020wEK) |
| `38.207.164.126` | 443 | HK/HKG | AS967 | 1193 ms | Guangzhou: 59.43.188.122; Nanjing: 59.43.139.109, 59.43.248.246; Beijing: 59.43.181.222, 59.43.246.226 | [查看](https://globalping.io?measurement=2WZK2j3AZtkAnR32x00020wEi) |
| `38.207.184.41` | 443 | HK/HKG | AS967 | 1098 ms | Nanjing: 59.43.130.154, 59.43.139.129, 59.43.183.110; Beijing: 59.43.246.226 | [查看](https://globalping.io?measurement=2csbDRXYaLSPTuEXv00020wFk) |
| `38.47.103.167` | 443 | HK/HKG | AS55933 | 1258 ms | Guangzhou: 59.43.183.110; Nanjing: 59.43.139.117, 59.43.183.110, 59.43.250.110 | [查看](https://globalping.io?measurement=2oj5vtScOVEvRra5w00020wFk) |
| `38.55.192.142` | 443 | HK/HKG | AS139659 | 2360 ms | Guangzhou: 59.43.188.122; Nanjing: 59.43.139.109, 59.43.248.246 | [查看](https://globalping.io?measurement=2XbBrH5J4NlBEBp9J00020wF6) |
| `38.55.195.57` | 443 | HK/HKG | AS139659 | 1083 ms | Guangzhou: 59.43.248.250; Beijing: 59.43.181.242, 59.43.246.226 | [查看](https://globalping.io?measurement=2Gk42xhx24xGFOxfx00020wFk) |
| `38.55.198.250` | 443 | HK/HKG | AS139659 | 1334 ms | Guangzhou: 59.43.183.110 | [查看](https://globalping.io?measurement=2ifg2E4hdUdSYIzpT00020wFc) |
| `45.136.13.92` | 443 | HK/HKG | AS139659 | 3580 ms | Nanjing: 59.43.123.89, 59.43.183.110; Beijing: 59.43.132.14, 59.43.248.2; Nanjing: 59.43.139.117, 59.43.183.110 | [查看](https://globalping.io?measurement=21ly5tG8ak9iwn7km00020wFF) |
| `45.152.67.25` | 443 | HK/HKG | AS139659 | 1225 ms | Guangzhou: 59.43.130.110, 59.43.248.250; Beijing: 59.43.181.222, 59.43.246.226; Nanjing: 59.43.139.109 | [查看](https://globalping.io?measurement=2TSqFcGneZjdCCNDV00020wFF) |
| `68.64.182.79` | 443 | HK/HKG | AS139659 | 1959 ms | Guangzhou: 59.43.248.246; Nanjing: 59.43.139.109, 59.43.248.246; Nanjing: 59.43.139.109, 59.43.183.110 | [查看](https://globalping.io?measurement=27qOEvbWcyQ0hRwyq00020w5b) |
| `165.154.21.142` | 443 | HK/HKG | AS135377 | 3998 ms | Guangzhou: 59.43.250.50; Nanjing: 59.43.139.137 | [查看](https://globalping.io?measurement=2EQh1zOqacEfIa8AB00020wF7) |
| `45.152.65.100` | 443 | HK/HKG | AS139659 | 1070 ms | Guangzhou: 59.43.183.110; Nanjing: 59.43.139.109, 59.43.183.110 | [查看](https://globalping.io?measurement=2M9l2WN9GGQ0KjE7o00020wF6) |
| `162.4.136.79` | 443 | HK/HKG | AS55933 | 2253 ms | Guangzhou: 59.43.130.162, 59.43.248.250; Nanjing: 59.43.139.109, 59.43.16.166, 59.43.188.122; Nanjing: 59.43.139.109 | [查看](https://globalping.io?measurement=29VdEhBAEGhfE1nvK00020wFE) |
| `38.207.175.9` | 443 | HK/HKG | AS967 | 1120 ms | Guangzhou: 59.43.188.122; Beijing: 59.43.19.98, 59.43.246.226 | [查看](https://globalping.io?measurement=2alfJgwo8pSicW45F00020wFk) |
| `38.207.177.204` | 443 | HK/HKG | AS139659 | 2473 ms | Nanjing: 59.43.130.122, 59.43.139.117, 59.43.248.246; Nanjing: 59.43.123.89, 59.43.188.122 | [查看](https://globalping.io?measurement=2Nu40TJGXzkCPLi8000020w5c) |
| `43.160.254.163` | 443 | SG/SIN | AS132203 | 4312 ms | Nanjing: 59.43.139.117 | [查看](https://globalping.io?measurement=2Hg4PXQzKGJNyRjR700020wEP) |
| `45.89.219.65` | 443 | SG/SIN | AS8888 | 1072 ms | Nanjing: 59.43.139.113; Beijing: 59.43.16.182, 59.43.250.54, 59.43.46.70 | [查看](https://globalping.io?measurement=2xtLfk4VmOGgUT2LE00020wFk) |
| `82.158.88.94` | 443 | HK/HKG | AS401701 | 1343 ms | Guangzhou: 59.43.183.110; Nanjing: 59.43.139.129, 59.43.183.110; Beijing: 59.43.183.122, 59.43.248.2; Xi'an: 59.43.137.241, 59.43.188.122 | [查看](https://globalping.io?measurement=2MoUn7gsFJdC3BnLz00020wES) |
| `161.117.181.127` | 443 | SG/SIN | AS45102 | 1106 ms | Beijing: 59.43.137.222 | [查看](https://globalping.io?measurement=2SJwt8SKBaPFgvCdS00020wFc) |
| `194.156.162.151` | 443 | SG/SIN | AS23961 | 1736 ms | Nanjing: 59.43.130.106, 59.43.139.113 | [查看](https://globalping.io?measurement=2aEucN23q8bEaIObP00020wFF) |
| `43.133.62.238` | 443 | SG/SIN | AS132203 | 2474 ms | Beijing: 59.43.137.222 | [查看](https://globalping.io?measurement=2zfcN2PQbO4sKGQqr00020wFc) |
| `150.109.11.223` | 443 | SG/SIN | AS132203 | 1259 ms | Nanjing: 59.43.139.129; Beijing: 59.43.145.62, 59.43.22.41; Xi'an: 59.43.137.241 | [查看](https://globalping.io?measurement=26FEmuI702JMATYME00020wEO) |
| `43.160.209.30` | 443 | SG/SIN | AS132203 | 1101 ms | Nanjing: 59.43.139.109; Xi'an: 59.43.137.241 | [查看](https://globalping.io?measurement=2IIkBo0KB5IV0xrl500020wEO) |
| `43.160.240.180` | 443 | SG/SIN | AS132203 | 1665 ms | Nanjing: 59.43.130.126, 59.43.139.117 | [查看](https://globalping.io?measurement=2IABIyi079OhY0s0E00020wEt) |
| `43.156.159.240` | 443 | SG/SIN | AS132203 | 3318 ms | Beijing: 59.43.137.222 | [查看](https://globalping.io?measurement=28gLy2PiTE4MsQazU00020wFc) |
| `45.194.18.109` | 443 | SG/SIN | AS137535 | 1795 ms | Nanjing: 59.43.139.129, 59.43.16.182 | [查看](https://globalping.io?measurement=2quu38VadGanRObfq00020wF6) |
| `43.156.142.191` | 443 | SG/SIN | AS132203 | 1190 ms | Nanjing: 59.43.139.113 | [查看](https://globalping.io?measurement=20h2UogvgwUaboyCo00020wEO) |
| `43.160.197.205` | 443 | SG/SIN | AS132203 | 2320 ms | Nanjing: 59.43.139.109 | [查看](https://globalping.io?measurement=2KT94gubBZQWEKhyF00020wEo) |
| `43.160.253.225` | 443 | SG/SIN | AS132203 | 2198 ms | Nanjing: 59.43.139.117 | [查看](https://globalping.io?measurement=2d5yRvREhWyGxkFzQ00020wEM) |
| `45.89.219.72` | 443 | SG/SIN | AS8888 | 1873 ms | Beijing: 59.43.137.222 | [查看](https://globalping.io?measurement=2DMe2ORi27H6TnZMh00020wFc) |
| `111.119.193.50` | 443 | SG/SIN | AS136907 | 1119 ms | Guangzhou: 59.43.130.102; Nanjing: 59.43.39.118, 59.43.46.101; Beijing: 59.43.159.18, 59.43.46.82 | [查看](https://globalping.io?measurement=2whzoXU1xDkzVQVJr00020w5c) |
| `43.156.23.85` | 443 | SG/SIN | AS132203 | 1287 ms | Guangzhou: 59.43.250.50; Nanjing: 59.43.139.109, 59.43.16.166 | [查看](https://globalping.io?measurement=2bPYUg7gIR76yVGed00020w5l) |
| `202.144.194.140` | 443 | JP/NRT | AS63916 | 1815 ms | Guangzhou: 59.43.144.209, 59.43.159.98; Beijing: 59.43.46.82 | [查看](https://globalping.io?measurement=23Ah9j9TmBr7MvQvb00020wFc) |
| `191.222.209.238` | 443 | JP/NRT | AS906 | 2080 ms | Guangzhou: 59.43.159.98; Nanjing: 59.43.132.149, 59.43.39.234 | [查看](https://globalping.io?measurement=2HvGPlVYGCbu4FfBF00020wF6) |
| `191.222.212.153` | 443 | JP/NRT | AS906 | 1153 ms | Guangzhou: 59.43.144.209; Nanjing: 59.43.139.133; Beijing: 59.43.138.54, 59.43.46.82 | [查看](https://globalping.io?measurement=2TlwLfz6LcPHMJNSB00020wF6) |
| `64.83.35.17` | 443 | JP/NRT | AS979 | 1158 ms | Guangzhou: 59.43.130.194, 59.43.137.226, 59.43.246.26; Beijing: 59.43.183.2, 59.43.46.82 | [查看](https://globalping.io?measurement=2rz54An05uRTu1SlD00020wFk) |
| `64.83.40.57` | 443 | JP/NRT | AS979 | 2554 ms | Guangzhou: 59.43.137.226; Nanjing: 59.43.139.133, 59.43.39.118; Guangzhou: 59.43.138.70, 59.43.144.209, 59.43.181.50 | [查看](https://globalping.io?measurement=2k2wswi3LgLh8gcBe00020wF6) |
| `64.83.46.12` | 443 | JP/NRT | AS979 | 1256 ms | Nanjing: 59.43.139.137, 59.43.159.18, 59.43.183.2, 59.43.39.82; Beijing: 59.43.130.190, 59.43.183.2 | [查看](https://globalping.io?measurement=2abFiRlLkOweAQh9000020wFk) |
| `191.222.212.77` | 443 | JP/NRT | AS906 | 1169 ms | Guangzhou: 59.43.130.194, 59.43.144.209; Nanjing: 59.43.139.133 | [查看](https://globalping.io?measurement=2EqHVS3p3juopEHaZ00020wEO) |
| `74.82.196.20` | 443 | JP/NRT | AS25820 | 2595 ms | Guangzhou: 59.43.137.226; Beijing: 59.43.46.82 | [查看](https://globalping.io?measurement=2G4XgBiHUqPaWwSbG00020wFF) |
| `82.40.33.173` | 443 | JP/NRT | AS400618 | 1338 ms | Guangzhou: 59.43.141.146, 59.43.183.2, 59.43.247.186; Nanjing: 59.43.183.2; Beijing: 59.43.246.26, 59.43.46.82; Guangzhou: 59.43.138.46, 59.43.246.26, 59.43.46.77 | [查看](https://globalping.io?measurement=2WzPJmyeibciCZEJu00020wF6) |
| `82.40.33.62` | 443 | JP/NRT | AS400618 | 1226 ms | Guangzhou: 59.43.144.209, 59.43.246.26; Nanjing: 59.43.246.26; Beijing: 59.43.138.54, 59.43.183.2, 59.43.46.82 | [查看](https://globalping.io?measurement=2I9wMX37IiGgESj8300020wEs) |
| `45.89.235.39` | 443 | JP/NRT | AS3258 | 6719 ms | Guangzhou: 59.43.141.146, 59.43.39.122 | [查看](https://globalping.io?measurement=2wnpD4YKlwaQbi2M400020wFc) |
| `64.83.38.37` | 443 | JP/NRT | AS979 | 2633 ms | Beijing: 59.43.22.6, 59.43.39.98, 59.43.46.82; Shenzhen: 59.43.137.226; Guangzhou: 59.43.144.209, 59.43.22.18 | [查看](https://globalping.io?measurement=2iOr9xiqk3Tt8pag900020wFc) |
| `74.82.198.138` | 443 | JP/NRT | AS25820 | 1201 ms | Guangzhou: 59.43.144.209; Beijing: 59.43.46.82 | [查看](https://globalping.io?measurement=2LlS6I0XJFJairKfn00020wFk) |
| `74.82.198.58` | 443 | JP/KIX | AS25820 | 1605 ms | Beijing: 59.43.46.82; Shenzhen: 59.43.46.77; Guangzhou: 59.43.141.146, 59.43.22.6 | [查看](https://globalping.io?measurement=2TAmbDiVREaE4wexC00020wFc) |
| `102.204.223.9` | 443 | JP/NRT | AS139923 | 1450 ms | Guangzhou: 59.43.144.209; Nanjing: 59.43.46.101; Beijing: 59.43.46.82; Shenzhen: 59.43.141.146 | [查看](https://globalping.io?measurement=2wDnlIZiMJW5cIkf900020wFF) |
| `14.137.238.86` | 443 | JP/NRT | AS401339 | 1965 ms | Guangzhou: 59.43.130.118, 59.43.187.182; Beijing: 59.43.19.94, 59.43.250.174 | [查看](https://globalping.io?measurement=2wGyjWvGSo6O1nX8l00020wFc) |
| `142.248.137.22` | 443 | JP/NRT | AS140227 | 1923 ms | Beijing: 59.43.22.6, 59.43.246.26, 59.43.247.186, 59.43.46.82 | [查看](https://globalping.io?measurement=2TV4kQjcnKdbjR8Cv00020wFc) |
| `142.248.139.188` | 443 | JP/NRT | AS140227 | 2462 ms | Guangzhou: 59.43.141.146, 59.43.159.18, 59.43.246.26; Nanjing: 59.43.130.198, 59.43.246.26; Beijing: 59.43.183.2, 59.43.22.18; Shenzhen: 59.43.138.50, 59.43.183.2, 59.43.46.77 | [查看](https://globalping.io?measurement=2fTSZ6fmEgQiYAujV00020wFF) |
| `142.248.139.25` | 443 | JP/NRT | AS140227 | 3601 ms | Guangzhou: 59.43.144.209, 59.43.183.2; Nanjing: 59.43.132.153, 59.43.246.26; Beijing: 59.43.246.26, 59.43.46.82 | [查看](https://globalping.io?measurement=2qw332P8VMNJilgtM00020wF6) |
| `207.56.227.33` | 443 | JP/NRT | AS140227 | 1236 ms | Guangzhou: 59.43.183.2, 59.43.22.6, 59.43.46.77; Nanjing: 59.43.139.137, 59.43.159.18, 59.43.183.2, 59.43.39.130 | [查看](https://globalping.io?measurement=26kHW3PfBvhTc09zp00020wER) |
| `38.47.198.28` | 443 | JP/NRT | AS140227 | 1495 ms | Guangzhou: 59.43.130.194, 59.43.246.26; Nanjing: 59.43.130.190, 59.43.132.153, 59.43.183.2 | [查看](https://globalping.io?measurement=2oZ73TJqD3bAwxaaH00020wF6) |
| `156.245.236.136` | 443 | TW/TPE | AS54801 | 1214 ms | Nanjing: 59.43.132.153 | [查看](https://globalping.io?measurement=2rxpYZ9EDjKFcdRf700020wFk) |
| `134.122.194.186` | 443 | JP/NRT | AS152194 | 1287 ms | Guangzhou: 59.43.141.146; Nanjing: 59.43.139.137 | [查看](https://globalping.io?measurement=2tJi6MZaOkYbKfOuk00020wFk) |
| `64.83.40.108` | 443 | JP/NRT | AS979 | 1267 ms | Guangzhou: 59.43.137.226; Nanjing: 59.43.139.133 | [查看](https://globalping.io?measurement=2WwgNok9OmuShunjL00020wFk) |
| `207.56.226.132` | 443 | JP/NRT | AS140227 | 2391 ms | Guangzhou: 59.43.144.209, 59.43.183.2, 59.43.39.238; Beijing: 59.43.246.26, 59.43.39.86, 59.43.46.82 | [查看](https://globalping.io?measurement=2lB2EfhpUlFhNOwgM00020wFF) |
| `142.248.139.237` | 443 | JP/NRT | AS140227 | 1135 ms | Nanjing: 59.43.139.137, 59.43.183.2, 59.43.39.62 | [查看](https://globalping.io?measurement=2Wph93t3e0bthhNb100020wFk) |
| `154.64.246.151` | 443 | HK/HKG | AS979 | 1551 ms | Nanjing: 59.43.139.109, 59.43.188.122; Shenzhen: 59.43.188.122 | [查看](https://globalping.io?measurement=2yzg8AxKvZs4cbX1L00020wEI) |
| `38.47.213.57` | 443 | HK/HKG | AS140227 | 1054 ms | Nanjing: 59.43.132.153 | [查看](https://globalping.io?measurement=2Msh7cmr25nWGHlXo00020wF6) |
| `64.90.24.26` | 443 | HK/HKG | AS979 | 4959 ms | Nanjing: 59.43.132.149; Xi'an: 59.43.156.129 | [查看](https://globalping.io?measurement=27uSTgcGacpPHUc6M00020wER) |
| `64.90.28.28` | 443 | HK/HKG | AS61112 | 1404 ms | Guangzhou: 59.43.187.182; Nanjing: 59.43.139.129, 59.43.183.106 | [查看](https://globalping.io?measurement=2lAE0HrZAmtwuZZNy00020wF6) |
| `64.90.7.42` | 443 | HK/HKG | AS979 | 1166 ms | Guangzhou: 59.43.248.250 | [查看](https://globalping.io?measurement=2OBtop16g4Ek0Eszf00020wFc) |
