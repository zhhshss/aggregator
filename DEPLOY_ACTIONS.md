# GitHub Actions 部署说明

## 已配置

- Fork: `zhhshss/aggregator`
- Gist: `zhhshss/45a28988a638e1251f10365bd3c4d6bc`
- Workflow:
  - `Collect`：每周一收集机场并上传 Gist
  - `Refresh`：每 6 小时刷新已有订阅
  - 两者结束后都会跑 `scripts/split_mainstream.py`，把命中主流关键字的节点单独写入 Gist 文件：
    - `mainstream-clash.yaml`
    - `mainstream-list.txt`

## Secrets（仓库 Settings → Secrets and variables → Actions）

| Name | Value |
|------|-------|
| `GIST_PAT` | 具有 `gist` 权限的 GitHub Token |
| `GIST_LINK` | `zhhshss/45a28988a638e1251f10365bd3c4d6bc` |
| `CUSTOMIZE_LINK` | 可选，自定义机场列表 URL |

## 手动触发

Actions → Collect / Refresh → Run workflow

## 订阅地址（Secret Gist 需 token 或登录后 raw）

- 全部节点 Clash：`https://gist.githubusercontent.com/zhhshss/45a28988a638e1251f10365bd3c4d6bc/raw/clash.yaml`
- 主流机场 Clash：`https://gist.githubusercontent.com/zhhshss/45a28988a638e1251f10365bd3c4d6bc/raw/mainstream-clash.yaml`

> Private Gist 的 raw 链接可能需带 token 或保持登录访问。

## 调整主流机场关键字

编辑 `data/mainstream_brands.txt`，一行一个关键字，提交后下次 workflow 生效。
