# CN2 代理筛选

`Find CN2 proxies` 工作流读取仓库根目录的 `Global-proxyip-443.csv`，按以下两阶段筛选：

1. 使用给定的百度 HTTP CONNECT 节点连接每个 CSV IP，并完成 TLS/HTTP 探测；
2. 从中国电信探针向可用代理 IP 发起回程 `traceroute`，出现 `59.43.0.0/16` 才标为 CN2。

结果会写入 `cn2/README.md`、`cn2/cn2.csv` 和 `cn2/cn2.json`，同时作为 Actions artifact 保存。

公开仓库可直接使用 GitHub-hosted runner。Globalping 的匿名额度较小，建议在仓库 Secret `GLOBALPING_TOKEN` 中配置 API token；工作流未配置 token 时仍可运行，但可能提前耗尽追踪额度。

可在仓库 Secret `GLOBALPING_PROXY_POOL` 中配置临时 HTTP 代理池，每行一个 `用户名:密码@IP:端口`。工作流只在运行时写入权限为 `600` 的临时文件，不会把代理账号提交到公开仓库；Globalping API 返回额度不足或代理连接失败时会自动轮换下一条。

工作流每小时运行一次。`cn2/progress.csv` 保存每个 IP 的百度可用性和路由追踪状态；每完成一个路由追踪都会在锁保护下原子更新本地断点，本轮结束后提交到仓库，并且无论任务是否意外失败都会上传紧急进度 artifact。下一轮会复测全部候选的百度可用性，但只追踪尚未完成的可用候选。临时没有探针的候选排到未扫描候选之后轮转重试，避免永久漏测。匿名 Globalping 配额耗尽时，本轮正常停止并发布进度，额度恢复后从断点继续。定时任务默认每轮最多新增 60 个路由追踪；手动全量任务可设置 `max_traces=0` 并使用并发追踪，定时任务不会取消仍在发布进度的上一轮任务。

扫描结果分为 `cn2_gia`、`cn2_gt`、`telecom_163_direct` 和 `other` 四档，并分别写入同名 CSV。DNS 巡检为前三档维护 `cn2-gia-国家`、`cn2-gt-国家`、`telecom-163-direct-国家` 独立域名；原有 `cn2-国家` 域名按 GIA → GT → 163 直连顺序故障切换。所有域名都先测试当前 IP，当前仍可用时保持不变。
