# CN2 代理筛选

`Find CN2 proxies` 工作流读取仓库根目录的 `Global-proxyip-443.csv`，按以下两阶段筛选：

1. 使用给定的百度 HTTP CONNECT 节点连接每个 CSV IP，并完成 TLS/HTTP 探测；
2. 从中国电信探针向可用代理 IP 发起回程 `traceroute`，出现 `59.43.0.0/16` 才标为 CN2。

结果会写入 `cn2/README.md`、`cn2/cn2.csv` 和 `cn2/cn2.json`，同时作为 Actions artifact 保存。

公开仓库可直接使用 GitHub-hosted runner。Globalping 的匿名额度较小，建议在仓库 Secret `GLOBALPING_TOKEN` 中配置 API token；工作流未配置 token 时仍可运行，但可能提前耗尽追踪额度。

手动运行：Actions → `Find CN2 proxies` → Run workflow。默认扫描香港、日本、新加坡、台湾和韩国的全部候选，并对全部可用候选做回程追踪；参数设为正整数时才限制数量。全量回程会消耗较多 Globalping 额度，因此工作流改为仅手动触发。
