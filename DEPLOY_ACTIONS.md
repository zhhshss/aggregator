# GitHub Actions + Cloudflare R2 部署说明

## 仓库 / 资源

- Fork: https://github.com/zhhshss/aggregator
- Gist: https://gist.github.com/zhhshss/45a28988a638e1251f10365bd3c4d6bc
- R2 Bucket: `aggregator`
- R2 公网: https://pub-70d7c1657a864bb1a041b001f07549cf.r2.dev

## Workflows

| 名称 | 触发 | 行为 |
|------|------|------|
| Collect | 每周一 / 手动 | 收集机场 → 上传 Gist → 拆主流机场 → 上传 R2 |
| Refresh | 每 6 小时 / 手动 | 刷新订阅 → 拆主流机场 → 上传 R2 |

主流关键字：`data/mainstream_brands.txt`

## Secrets

| Name | 示例 |
|------|------|
| `GIST_PAT` | GitHub token（gist 权限） |
| `GIST_LINK` | `zhhshss/45a28988a638e1251f10365bd3c4d6bc` |
| `R2_ENDPOINT` | `https://6ebc3ef97b0aca55c0f4660685627750.r2.cloudflarestorage.com` |
| `R2_ACCESS_KEY_ID` | R2 Access Key ID |
| `R2_SECRET_ACCESS_KEY` | R2 Secret Access Key |
| `R2_BUCKET` | `aggregator` |
| `R2_PUBLIC_BASE` | `https://pub-70d7c1657a864bb1a041b001f07549cf.r2.dev` |
| `R2_PREFIX` | 可选，对象前缀 |

## 公网订阅地址（R2）

- 全部 Clash: https://pub-70d7c1657a864bb1a041b001f07549cf.r2.dev/clash.yaml
- 全部 V2Ray: https://pub-70d7c1657a864bb1a041b001f07549cf.r2.dev/v2ray.txt
- 全部 SingBox: https://pub-70d7c1657a864bb1a041b001f07549cf.r2.dev/singbox.json
- 主流机场 Clash: https://pub-70d7c1657a864bb1a041b001f07549cf.r2.dev/mainstream-clash.yaml
- 主流列表: https://pub-70d7c1657a864bb1a041b001f07549cf.r2.dev/mainstream-list.txt
- 索引: https://pub-70d7c1657a864bb1a041b001f07549cf.r2.dev/index.txt

## 手动触发

Actions → Collect / Refresh → Run workflow
