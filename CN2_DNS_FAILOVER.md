# CN2 DNS 自动故障切换

该任务与 CN2 发现工作流完全分离。`CN2 DNS failover` 每小时读取已发布的 `cn2/cn2.csv`，按国家维护一个仅 DNS 的 A 记录：

- `cn2-jp.ciallo0d000721.cc.cd`
- `cn2-sg.ciallo0d000721.cc.cd`
- `cn2-tw.ciallo0d000721.cc.cd`

测试时通过百度 HTTP CONNECT 前置，把 `cp.cloudflare.com:443` 强制连接到候选 IP，并要求 Cloudflare 返回 HTTP 200/204。当前 DNS 指向会优先测试；失效后才依次切换到该国家其他已确认 CN2 IP。若该国家全部候选失效，则保留现有 DNS，不写入坏地址。

DNS 记录使用 `DNS only`，TTL 为 60 秒。工作流只读取 CN2 发现结果，不启动、重跑或修改 CN2 发现任务。
