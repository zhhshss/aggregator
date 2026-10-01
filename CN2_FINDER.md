# CN2 代理筛选

`Find CN2 proxies` 工作流**实时**从 `https://zip.cm.edu.kg/ip.zip` 拉取 CF 反代 IP（不写死任何 IP），按以下两阶段筛选：

1. 使用给定的百度 HTTP CONNECT 节点连接每个 CSV IP，并完成 TLS/HTTP 探测；
2. 从中国电信探针向可用代理 IP 发起回程 `traceroute`，出现 `59.43.0.0/16` 才标为 CN2。

结果会写入 `cn2/README.md`、`cn2/cn2.csv` 和 `cn2/cn2.json`，同时作为 Actions artifact 保存。
其他优质线路（CMIN2、CU9929、CUVIP、SoftBank、NTT、IIJ、TATA、GTT、Cogent、HKIX、EIE）按同样格式分别写入 `cn2/<route_class>.csv`。

公开仓库可直接使用 GitHub-hosted runner。Globalping 的匿名额度较小，建议在仓库 Secret `GLOBALPING_TOKEN` 中配置 API token；工作流未配置 token 时仍可运行，但可能提前耗尽追踪额度。

可在仓库 Secret `GLOBALPING_PROXY_POOL` 中配置临时 HTTP 代理池，每行一个 `用户名:密码@IP:端口`。工作流只在运行时写入权限为 `600` 的临时文件，不会把代理账号提交到公开仓库；每个代理同一时刻只创建一个 Globalping 测量，返回额度不足或连接失败时自动轮换下一条。

工作流每小时运行一次，每次运行前都会重新从 `zip.cm.edu.kg` 拉取最新 IP 列表。`cn2/progress.csv` 保存每个 IP 的百度可用性和路由追踪状态；每完成一个路由追踪都会在锁保护下原子更新本地断点，本轮结束后提交到仓库，并且无论任务是否意外失败都会上传紧急进度 artifact。下一轮会复测全部候选的百度可用性，但只追踪尚未完成的可用候选。临时没有探针的候选排到未扫描候选之后轮转重试，避免永久漏测。匿名 Globalping 配额耗尽时，本轮正常停止并发布进度，额度恢复后从断点继续。定时任务默认每轮最多新增 60 个路由追踪；手动全量任务可设置 `max_traces=0` 并使用并发追踪，定时任务不会取消仍在发布进度的上一轮任务。

扫描结果分为 `cn2_gia`、`cn2_gt`、`telecom_163_direct`、`cmin2`、`cu9929`、`cuvip`、`softbank`、`ntt`、`iij`、`tata`、`gtt`、`cogent`、`hkix`、`eie` 和 `other` 等档，并分别写入同名 CSV。DNS 巡检为 CN2 前三档维护 `cn2-gia-国家`、`cn2-gt-国家`、`telecom-163-direct-国家` 独立域名；原有 `cn2-国家` 域名按 GIA → GT → 163 直连顺序故障切换。所有域名都先测试当前 IP，当前仍可用时保持不变。

## 数据源

实时拉取地址：`https://zip.cm.edu.kg/ip.zip`（可在 workflow_dispatch 的 `zip_url` 中覆盖）。  
压缩包结构：`443/<国家代码>.txt` 每行一个 IPv4/IPv6，脚本按端口和地区过滤后生成 `Global-proxyip-443.csv` 供扫描使用。
