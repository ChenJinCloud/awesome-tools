# 产品策展实施计划

[English](2026-07-29-product-curation-implementation.md) | [简体中文](2026-07-29-product-curation-implementation.zh-CN.md)

> 历史计划：本文描述的是一套拟议的实施顺序，不能证明其中提到的文件、检查或仓库状态目前仍然存在或已经实现。

> **面向 Agent 执行者：** 必需子 Skill：建议使用 `superpowers:subagent-driven-development`，也可以使用 `superpowers:executing-plans`，逐项实施此计划。步骤使用复选框（`- [ ]`）追踪。

**目标：** 增加一个小而严格的产品策展系统，将候选项与正式条目分开，执行基于证据的状态规则，并保护公开仓库免受格式错误、过时、重复或敏感提交的影响。

**架构：** Markdown 保持为人类可读的事实源。每个产品位于一个按类型划分的目录中，并使用固定的元数据和章节结构；小型 Python 标准库验证器负责检查结构、时效性、重复 URL 和链接可用性。GitHub Issue 与 Pull Request 模板提供人工准入门禁，一个 CI 工作流将新的 catalog 检查与已有公开安全扫描结合。

**技术栈：** Markdown、GitHub Issue Forms、GitHub Actions、Python 3.11+ 标准库，以及已有的 `scripts/check_public_safety.py`。

## 全局约束

- 仓库是小而严格的个人集合，不是完整目录或广告渠道。
- 产品类型为 `software`、`saas`、`hardware`、`services` 和 `open-source`。
- 正式状态严格限定为 `researched`、`tested` 和 `recommended`；`candidate` 只存在于 Issues。
- `tested` 和 `recommended` 要求维护者的直接体验。
- `researched` 要求持续观察或可信用户的具体一手经验，同时需要一手来源。
- 一个产品条目对应一个 Markdown 文件；一次产品提交对应一个 Pull Request。
- 凭证、原始私有记录、账号标识、Cookie、会话、日志或特定机器的私有路径不得进入仓库。
- catalog 验证只使用 Python 标准库，不增加包管理器依赖。
- 链接检查必须限制超时和重试，且不得提交凭证或发起认证请求。
- 自动化只验证结构和公开安全，不判断产品是否真的优秀。

---

## 文件映射

| 路径 | 职责 |
| --- | --- |
| `templates/product-entry.md` | 可复制的权威产品条目模板及字段说明。 |
| `products/README.md` | 解释正式状态、类型目录和准入边界。 |
| `products/software/.gitkeep` | 在首个条目出现前保留软件目录。 |
| `products/saas/.gitkeep` | 在首个条目出现前保留 SaaS 目录。 |
| `products/hardware/.gitkeep` | 在首个条目出现前保留硬件目录。 |
| `products/services/.gitkeep` | 在首个条目出现前保留服务目录。 |
| `products/open-source/.gitkeep` | 在首个条目出现前保留开源目录。 |
| `archive/README.md` | 定义归档元数据，避免归档条目暗示当前仍然推荐。 |
| `scripts/check_product_catalog.py` | 解析并验证条目元数据、标题、状态证据、类型位置、重复 URL、风险审查周期和时效性。 |
| `scripts/test_product_catalog.py` | 不联网的 catalog 验证回归测试。 |
| `scripts/check_product_links.py` | 使用有边界的匿名 HTTP 请求检查公开产品和来源 URL。 |
| `scripts/test_product_links.py` | 测试链接成功、重试和失败行为的本地假服务器测试。 |
| `.github/ISSUE_TEMPLATE/suggest-product.yml` | 只用于候选产品、包含关系披露的建议表单。 |
| `.github/PULL_REQUEST_TEMPLATE/product.md` | 不影响代码 PR 的产品专用单条目检查清单和维护者状态声明。 |
| `.github/workflows/product-catalog-checks.yml` | 运行结构测试、catalog 验证、公开安全检查和链接检查。 |
| `README.md` | 解释策展模型，并链接候选项、正式产品、归档和贡献路径。 |

---

### 任务 1：建立产品条目契约和仓库目录

**文件：**

- 创建：`templates/product-entry.md`
- 创建：`products/README.md`
- 创建：`products/software/.gitkeep`
- 创建：`products/saas/.gitkeep`
- 创建：`products/hardware/.gitkeep`
- 创建：`products/services/.gitkeep`
- 创建：`products/open-source/.gitkeep`
- 创建：`archive/README.md`

**接口：**

- 输入：`docs/superpowers/specs/2026-07-29-product-curation-design.md` 中已批准的状态定义和准入标准。
- 输出：供 `scripts/check_product_catalog.py` 使用的精确元数据标签和标题名称：`Status`、`Last reviewed`、`Product type`、`Official website`，以及下列 13 个必需的 `##` 标题。

- [ ] **步骤 1：创建权威条目模板**

创建 `templates/product-entry.md`。它是可复制模板，不是正式产品条目，因此可以使用安全的字面占位值。完整模板代码保持与[英文版对应步骤](2026-07-29-product-curation-implementation.md#task-1-establish-the-product-entry-contract-and-repository-directories)一致，包含：

- 产品名称、状态、最近审查日期、产品类型、官方网站和审查周期；
- `What It Is`、`Why It Earned A Place`、`Best For`、`Experience Basis`；
- `What Has Been Verified`、`What Has Not Been Verified`；
- `Strengths`、`Limitations And Risks`、`Pricing And Access`；
- `Privacy And Data Handling`、`Alternatives`、`Source Links`、`Disclosure`。

`tested` 或 `recommended` 只有在事实准确时，才可以在未验证部分写 `None material for the documented use case.`；不存在利益冲突时在披露部分写 `None.`。

- [ ] **步骤 2：记录正式产品的放置规则**

创建 `products/README.md`，说明只有通过产品策展设计准入标准的正式条目才能放在这里；未经审查的发现保留为候选 Issues。

文档必须解释：

- `researched`：基于持续观察、可信一手经验和一手来源形成独立判断，但维护者尚未亲自测试；
- `tested`：维护者亲自完成至少一个核心工作流；
- `recommended`：维护者可以说明谁应该使用、为什么，以及何时不应该使用。

收录不等于推荐。`Recommended`、`Tested` 和 `Researched` 三个列表初始均写 `No entries yet.`。

- [ ] **步骤 3：创建类型目录和归档规则**

创建五个空 `.gitkeep` 文件。创建 `archive/README.md`，要求归档条目记录 `Archived`、`Former status`、`Archive reason`、`Possible replacements`，以及历史结论可能过时的警告。

- [ ] **步骤 4：运行公开安全检查**

运行：

```bash
python scripts/check_public_safety.py --root .
python scripts/test_public_safety.py
```

预期：两个命令都以 `0` 退出并打印通过信息。

- [ ] **步骤 5：提交条目契约**

```bash
git add templates/product-entry.md products archive
git commit -m "docs: define product entry contract"
```

---

### 任务 2：使用测试驱动开发构建 catalog 验证器

**文件：**

- 创建：`scripts/check_product_catalog.py`
- 创建：`scripts/test_product_catalog.py`

**接口：**

- 输入：`products/<product-type>/*.md` 下的 Markdown 文件，以及任务 1 定义的字段和标题契约。
- 输出：`validate_catalog(root: Path, today: date) -> list[Finding]`；无错误时 CLI 退出码为 `0`，否则为 `2`；诊断只包含文件、规则 ID 和安全说明。

- [ ] **步骤 1：为有效和格式错误的条目编写失败夹具测试**

在 `scripts/test_product_catalog.py` 中使用 `tempfile.TemporaryDirectory`。导入 `check_product_catalog` 的 `validate_catalog`，建立隔离真实文件的 `entry`、`write_entry`、`rule_ids_for` 和 `rules_for_two_entries_with_same_url` 辅助函数。完整 Python 夹具保持与[英文版](2026-07-29-product-curation-implementation.md#task-2-build-the-catalog-validator-with-test-driven-development)一致。

测试必须覆盖：

- 有效 catalog 没有发现项；
- `candidate` 触发 `invalid-status`；
- 产品类型和目录不一致触发 `type-directory-mismatch`；
- `researched` 缺少未验证说明触发 `researched-unverified-required`；
- `tested` 缺少直接体验触发 `tested-direct-experience-required`；
- `recommended` 缺少不推荐边界触发 `recommended-boundary-required`；
- 重复官方网站触发 `duplicate-official-url`；
- 超过审查周期触发 `review-stale`；
- 不允许的审查周期触发 `review-interval`。

- [ ] **步骤 2：运行测试并确认导入失败**

```bash
python scripts/test_product_catalog.py
```

预期：非零退出，并出现 `ModuleNotFoundError: No module named 'check_product_catalog'`。

- [ ] **步骤 3：实现解析器和发现项类型**

创建 `scripts/check_product_catalog.py`，定义 `Finding`、`Entry`、`parse_entry`、`validate_entry` 和 `validate_catalog`。字段签名、允许状态、允许类型、默认审查周期、允许周期以及 13 个必需章节，均保持与英文版代码完全一致。

规范化官方网站 URL 时：小写化 scheme 和 host、移除末尾斜杠，并拒绝查询字符串和 fragment。`Review interval months` 只能为 `3`、`6` 或 `12`，可以缩短但不得延长产品类型的默认周期。处理敏感数据、权限或私有工作流的产品使用 `3` 或 `6`。`tested` 和 `recommended` 的 `Experience Basis` 必须包含精确标记 `Direct use:`；`recommended` 的 `Limitations And Risks` 必须包含 `Do not use when:`。

- [ ] **步骤 4：实现安全的 CLI 行为**

支持：

```text
--root PATH          仓库根目录，默认为 scripts/ 的父目录
--today YYYY-MM-DD   用于测试和维护的确定性日期覆盖
--json               以 JSON 输出发现项，不包含条目内容
```

只打印安全诊断，例如：

```text
Product catalog validation failed.
- products/saas/example.md [review-stale] Review is older than the 6-month interval.
```

不得打印章节内容或 URL。

- [ ] **步骤 5：运行验证器测试和空的真实 catalog**

```bash
python scripts/test_product_catalog.py
python scripts/check_product_catalog.py --root .
```

预期：测试打印 `Product catalog validator tests passed.`，真实 catalog 打印 `Product catalog validation passed.`，退出码均为 `0`。

- [ ] **步骤 6：提交验证器**

```bash
git add scripts/check_product_catalog.py scripts/test_product_catalog.py
git commit -m "feat: validate product catalog entries"
```

---

### 任务 3：增加有边界的匿名链接验证

**文件：**

- 创建：`scripts/check_product_links.py`
- 创建：`scripts/test_product_links.py`

**接口：**

- 输入：从正式产品 Markdown 文件的 `Official website` 和 `Source Links` 中提取的公开 `http`、`https` URL。
- 输出：`check_urls(urls: Iterable[str], timeout: float, retries: int) -> list[LinkFinding]`；成功时 CLI 退出码为 `0`，确认失败时为 `2`；不保存或打印响应正文。

- [ ] **步骤 1：编写失败的假服务器测试**

用本地 `ThreadingHTTPServer` 创建 `/ok`、`/head405`、`/missing` 和 `/flaky` 四个路径，分别覆盖成功、HEAD 不支持后 GET 成功、404 和首次 503 后成功。断言成功项无发现，`/missing` 返回 `link-http-error`，`file:///private/path` 返回 `link-scheme`。完整测试代码见英文版对应步骤。

- [ ] **步骤 2：运行测试并确认导入失败**

```bash
python scripts/test_product_links.py
```

预期：非零退出，并出现 `ModuleNotFoundError: No module named 'check_product_links'`。

- [ ] **步骤 3：实现 URL 提取和检查**

使用 `urllib.request` 和 `urllib.parse` 创建 `scripts/check_product_links.py`，定义 `LinkFinding`、`extract_urls` 和 `check_urls`。要求：

- 只允许 `http` 和 `https`；
- 不从环境或配置中读取凭证；
- 拒绝包含用户名或密码的 URL；
- 使用静态 `User-Agent: awesome-tools-link-check/1.0`；
- 使用 `HEAD`，只在状态为 `405` 或 `501` 时回退到 `GET`；
- 状态 `429`、`500`、`502`、`503` 和 `504` 按 `0.5`、`1.0` 秒延迟重试；
- 重定向使用 `urllib` 默认行为；
- 只打印主机名、规则和状态类别，不打印查询字符串或响应正文。

- [ ] **步骤 4：增加确定性的 CLI 控制**

支持：

```text
--root PATH
--timeout SECONDS
--retries COUNT
```

没有正式条目时打印 `No product links to check.` 并以 `0` 退出。

- [ ] **步骤 5：运行本地测试**

```bash
python scripts/test_product_links.py
python scripts/check_product_links.py --root . --timeout 5 --retries 2
```

预期：假服务器测试通过；空 catalog 报告没有链接并以 `0` 退出。

- [ ] **步骤 6：提交链接检查器**

```bash
git add scripts/check_product_links.py scripts/test_product_links.py
git commit -m "feat: check product catalog links"
```

---

### 任务 4：增加候选项入口和 Pull Request 治理

**文件：**

- 创建：`.github/ISSUE_TEMPLATE/suggest-product.yml`
- 创建：`.github/ISSUE_TEMPLATE/config.yml`
- 创建：`.github/PULL_REQUEST_TEMPLATE/product.md`

**接口：**

- 输入：已批准设计中的候选字段和权限边界。
- 输出：带有 `candidate` 标签的候选 Issues、`needs-review` 维护标签，以及要求单条目范围且由维护者决定状态的产品 PR。

- [ ] **步骤 1：创建候选 Issue 表单**

创建 `.github/ISSUE_TEMPLATE/suggest-product.yml`。完整 YAML 保持与英文版一致，必须收集：产品名、官方网站、产品类型、问题与具体用例、经验基础、具体经验和一手来源、限制与替代方案、提交者与产品的关系、关系详情，以及不包含凭证或私有记录的安全确认。

表单名称为 `Suggest a product`，默认标题前缀为 `Candidate: `，标签为 `candidate`。候选项在维护者独立接纳前一直保留在 Issues 中。

- [ ] **步骤 2：关闭无结构 Issue 并定义 PR 检查清单**

创建 `.github/ISSUE_TEMPLATE/config.yml`，设置 `blank_issues_enabled: false`。创建 `.github/PULL_REQUEST_TEMPLATE/product.md`，要求：

- 只包含一个产品条目；
- 链接一个现有候选 Issue；
- 披露提交者关系；
- 维护者确认正式状态；
- 提供一手来源链接；
- 完成公开安全和 catalog 检查；
- `tested`/`recommended` 包含 `Direct use:`；
- `recommended` 包含 `Do not use when:`。

- [ ] **步骤 3：在本地验证 YAML 和必需文案**

使用 Python 标准库冒烟测试，确认 Issue 表单包含 `labels: ["candidate"]`、`id: relationship`、`id: disclosure` 和 `id: safety`。完整命令见英文版。预期退出码为 `0` 且无输出。分支推送后，由 GitHub 对 Issue Form 结构作权威验证。

- [ ] **步骤 4：创建所需仓库标签**

```bash
gh label create candidate --repo ChenJinCloud/awesome-tools --color D4C5F9 --description "Product proposed for investigation; not formally included" --force
gh label create needs-review --repo ChenJinCloud/awesome-tools --color FBCA04 --description "Current evidence or review date needs maintainer attention" --force
```

然后列出标签，并确认只打印 `candidate` 和 `needs-review` 两个名称。

- [ ] **步骤 5：提交治理模板**

```bash
git add .github/ISSUE_TEMPLATE .github/PULL_REQUEST_TEMPLATE/product.md
git commit -m "docs: add product contribution workflow"
```

---

### 任务 5：将 catalog 和隐私检查接入 GitHub Actions

**文件：**

- 创建：`.github/workflows/product-catalog-checks.yml`

**接口：**

- 输入：任务 2 和任务 3 的测试与 CLI 脚本，以及已有的 `scripts/check_public_safety.py` 和 `scripts/test_public_safety.py`。
- 输出：一个名为 `product-catalog` 的必需检查候选项，在影响产品、模板、验证器、工作流或公开安全规则的 Push 和 Pull Request 上运行。

- [ ] **步骤 1：创建工作流**

完整 YAML 保持与英文版一致。它应当：

- 仅在相关 `products/`、`archive/`、`templates/`、`.github/` 和 `scripts/` 路径变化时触发；
- 使用只读 `contents` 权限；
- 在 Ubuntu 和 Python 3.11 上运行；
- 依次测试并执行公开安全扫描、产品 catalog 验证和产品链接检查；
- 将超时限制为 10 分钟。

首次实施中不要增加写权限、Secrets、定时任务或自动提交。

- [ ] **步骤 2：按工作流顺序在本地验证全部命令**

运行英文版列出的六个 Python 命令，依次测试与执行公开安全、产品 catalog 和产品链接检查。预期全部以 `0` 退出。

- [ ] **步骤 3：提交 CI**

```bash
git add .github/workflows/product-catalog-checks.yml
git commit -m "ci: validate product catalog"
```

---

### 任务 6：把策展系统整合到公开 README

**文件：**

- 修改：`README.md`
- 修改：`docs/public-review-checklist.md`

**接口：**

- 输入：任务 1–5 生成的全部模板、验证器、贡献路径和命令。
- 输出：帮助公众发现、建议、审查、新增和归档产品的导航与操作说明。

- [ ] **步骤 1：在 README 中加入产品策展定位**

在开头说明后加入 `Product Curation` 部分，说明这是小而严格的个人集合，不是完整目录；正式产品条目必须基于直接使用、持续观察或可信用户的具体一手经验；收录不等于推荐。

用表格解释 `researched`、`tested` 和 `recommended`，并链接：

- 正式产品列表；
- 候选产品建议表单；
- 产品条目模板；
- 归档条目。

扩展目录结构，加入 `products/`、`archive/`、`templates/product-entry.md`、两个产品检查脚本和 `.github/` 贡献文件。真实产品通过审查前，不得加入 `Current Entries`。

- [ ] **步骤 2：扩展人工公开审查清单**

在 `docs/public-review-checklist.md` 中增加产品条目部分，要求检查：

- 经验基础具体且可以归因；
- 已验证与未验证声明分开；
- 推荐受众和不适用边界明确；
- 价格和隐私声明引用当前一手来源；
- 披露完整；
- 未把私有证据复制到公开条目。

- [ ] **步骤 3：运行完整本地验证套件**

运行公开安全、产品 catalog 和产品链接的测试与检查，最后运行 `git diff --check`。完整命令见英文版。预期所有 Python 命令以 `0` 退出，`git diff --check` 无输出。

- [ ] **步骤 4：根据已批准设计验证实施结果**

逐项检查 `docs/superpowers/specs/2026-07-29-product-curation-design.md` 的验收标准，并在最终 Pull Request 描述中记录证据：

```text
候选项与产品分离：Issue Form + products/README.md
三种状态得到执行：check_product_catalog.py
可复用模板：product-entry.md + suggest-product.yml
一个产品一个 PR：PULL_REQUEST_TEMPLATE.md
结构/链接/重复/时效/安全检查：scripts + workflow
README 展示顺序：README 状态表，不展示未审查条目
归档历史：archive/README.md
```

- [ ] **步骤 5：提交公开文档**

```bash
git add README.md docs/public-review-checklist.md
git commit -m "docs: publish product curation guide"
```

---

### 任务 7：最终分支验证和发布

**文件：**

- 仅验证；预期不新增文件。

**接口：**

- 输入：已完成的任务 1–6。
- 输出：包含完整产品策展系统、可以审查的分支或 Pull Request。

- [ ] **步骤 1：确认预期范围和干净工作区**

```bash
git status -sb
git diff --stat origin/main...HEAD
git diff --name-status origin/main...HEAD
```

预期：只出现本计划点名的文件，工作区没有未暂存修改。

- [ ] **步骤 2：执行全新的最终验证**

重新运行公开安全、产品 catalog、产品链接的全部测试和检查，然后对 `origin/main...HEAD` 运行 `git diff --check`。预期所有命令以 `0` 退出并打印通过信息。

- [ ] **步骤 3：发布供审查**

如果在功能分支执行，推送分支并创建 Draft PR。PR 正文必须说明修改内容、原因、证据和状态边界、隐私保护、验证命令，以及这次基础设施修改没有新增真实产品推荐。

```bash
git push -u origin "$(git branch --show-current)"
```

未经维护者明确指示，不得强制推送、自动合并或将 PR 标记为 Ready。
