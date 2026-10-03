# 09. Docker 部署指南

> **课程信息**
>
> - **作者**：老金
> - **GitHub**：https://github.com/KimYx0207
> - **公众号**：老金带你玩AI
> - **X（Twitter）**：老金带你玩AI
> - **个人博客**：https://aiking.dev
> - **难度等级**：🔴 高级
> - **阅读时间**：30 分钟
> - **前置知识**：了解 Docker 基础概念、已完成快速开始（[03-快速开始指南](03-快速开始指南.md)）
>
> **本篇你将学会：** 用 Docker 部署 OpenClaw 到服务器、配置 docker-compose、管理数据持久化、设置自动更新
>
> **谁需要看这篇？** 如果你只是在自己电脑上用，不需要看这篇。这篇是给想把 OpenClaw 部署到远程服务器（比如云服务器）的人准备的

## 为什么用 Docker 部署 OpenClaw？

老金在部署课里不会只写一条 docker 命令，因为真正上线后要面对的是升级、日志、回滚和权限。





> **官方文档**：[docs.openclaw.ai/install/docker](https://docs.openclaw.ai/install/docker)

在聊具体操作之前，先搞清楚一个问题：我直接装不行吗，为什么要折腾 Docker（容器化平台，把应用和环境打包在一起运行）？

### Docker 部署的优势

**环境一致性** — 镜像固定了运行时和依赖，可以减少机器间的环境差异。换服务器仍要确认 CPU 架构、挂载路径、文件权限和网络；配置与数据需要单独持久化。

**统一启动** — 使用预构建镜像时，无需在宿主机安装 Node.js。先准备持久化目录、完成 onboarding 和认证，再用 `docker compose up -d` 启动服务。

**隔离性** — OpenClaw 跑在自己的容器里，不会污染宿主机环境。你可以在同一台机器上跑多个版本的 OpenClaw，互不干扰。

**易于迁移** — 想换服务器？把 docker-compose.yml（Docker 的编排工具，用一个配置文件管理多个容器）和数据卷拷过去，几分钟就能恢复。

**Agent 沙箱** — 可以另行启用 Docker 沙箱隔离工具执行。`agents.defaults.sandbox.mode` 默认是 `"off"`，需要显式选择 `"non-main"` 或 `"all"`。隔离程度还取决于挂载、网络和工具权限；容器化 Gateway 本身不会自动启用工具沙箱。

**版本可固定** — 可以保留旧镜像供回滚使用，但旧程序必须兼容现有数据库结构。发生迁移后要用匹配版本和已验证的升级前备份恢复；volume 负责持久化，不保证旧版本能读取新数据。

### 什么时候不需要 Docker

- 在自己电脑上开发调试，直接本地安装更快
- 只是临时试用，不需要持久化部署
- 机器资源极其有限（Docker 本身有一定开销）

> **经验法则**：本地开发用原生安装，远程部署用 Docker。

---

## Docker 基础环境准备

### 安装 Docker

#### Linux（推荐 Ubuntu 22.04+）

```bash
# 官方一键安装脚本（最省事）
curl -fsSL https://get.docker.com | sh

# 把当前用户加入 docker 组（免 sudo）
sudo usermod -aG docker $USER

# 重新登录让权限生效
newgrp docker

# 验证安装
docker --version
docker compose version
```

#### macOS

```bash
# 方法一：Docker Desktop（图形界面）
# 从 https://www.docker.com/products/docker-desktop/ 下载安装

# 方法二：Homebrew
brew install --cask docker

# 安装后启动 Docker Desktop，验证
docker --version
docker compose version
```

#### Windows

```powershell
# 方法一：Docker Desktop（推荐）
# 从 https://www.docker.com/products/docker-desktop/ 下载安装
# 需要开启 WSL2 或 Hyper-V

# 方法二：winget
winget install Docker.DockerDesktop

# 安装后重启，验证
docker --version
docker compose version
```

### 系统要求

| 项目 | 最低要求 | 推荐配置 |
|------|---------|---------|
| CPU | 1 核 | 2 核+ |
| 内存 | 2 GB | 4 GB+ |
| 磁盘 | 10 GB | 20 GB+ |
| Docker | 24.0+ | 最新稳定版 |
| Docker Compose | v2.20+ | 最新稳定版 |

### 验证 Docker 环境

```bash
docker run --rm hello-world    # 确认 Docker 正常
docker compose version         # 确认 Compose v2（不带横杠）
```

> **注意**：本文全部使用 `docker compose`（v2 语法），不是 `docker-compose`（v1 已弃用）。

---

## 官方 Docker 镜像使用


### 拉取官方镜像

```bash
docker pull openclaw/openclaw:latest    # 最新稳定版
docker pull openclaw/openclaw:2026.9.4   # 指定版本（镜像标签不带 v，核查日 2026-09-14）
docker images | grep openclaw           # 查看本地镜像
```

> **2026-09-14 当前基线（v2026.9.4）**：生产部署有两处要改口径。一是 v2026.9.4 新增 `OPENCLAW_CONFIG_READONLY=1`，容器和配置托管场景下可以让 OpenClaw 不再改写部署方管理的配置，同时保留只读诊断和正常运行状态。二是 `openclaw update` 的自动回滚只在数据库结构未变、旧包兼容且配置校验通过时才恢复包、配置和服务，**数据库迁移仍然要求有一份已验证的升级前备份**。Docker 直接替换镜像不会走这套 CLI 回滚流程，需按下文备份和恢复步骤处理。官方镜像标签不带 `v`，例如 `2026.9.4`；生产环境要锁定验证过的标签或 digest。当前 `latest` 为 2026.9.4，`extended-stable` 为 2026.6.35（核查日：2026-09-14）。来源：[官方 Docker 说明](https://docs.openclaw.ai/install/docker)、[回滚与恢复](https://docs.openclaw.ai/install/updating/rollback-and-recovery)。

> **v2026.6.8 发布校验**：Docker / npm 生产部署时，优先用官方发布包和固定 tag；自建镜像要保留 package integrity check，不要为了减小镜像随手删 lockfile / shrinkwrap。v2026.6.8 release notes 强化了 release / CI / Docker / E2E / diagnostics 证据链、bounded logs、readiness probes、latest tag parsing 和 rollback snapshots，生产升级时要把这些证据当成升级核对入口。

> **安全补丁提示**：这一轮还包含 `protobufjs` 8.4.0 安全更新。生产镜像不要长期停在旧 tag；升级镜像后用 `openclaw doctor` 和容器健康检查确认 Gateway、插件和 channels 都仍能启动。

### 从仓库 Dockerfile 构建镜像

> ⏭️ **小白可跳过** — 这部分面向运维专家，单机部署不需要

如果需要自定义镜像（比如加额外系统包）：

```bash
git clone https://github.com/openclaw/openclaw.git && cd openclaw

# 基础构建
docker build -t openclaw:local -f Dockerfile .

# 带额外 apt 包构建
docker build --build-arg OPENCLAW_DOCKER_APT_PACKAGES="ffmpeg imagemagick" \
  -t openclaw:custom -f Dockerfile .
```

### 镜像标签说明

| 标签 | 说明 | 适用场景 |
|------|------|---------|
| `latest` | 随稳定版发布移动的标签 | 先验证，再锁定具体版本 |
| `YYYY.M.D` | 指定版本号（如 `2026.9.4`，不带 `v`） | 需要版本锁定 |
| `extended-stable` | 滞后月份的 Gateway 维护通道 | 按兼容需求选择，仍需验证 |
| `local` | 本地构建 | 自定义需求 |

### Gateway ready 与 restart trace

v2026.5.22 对 Gateway 启动路径做了多处性能和诊断优化：插件元数据、channel catalog、startup-idle plugin work、ACPX runtime 会尽量延迟或缓存，Gateway ready 信号不再被未用到的 handler tree 阻塞。

生产部署的健康检查建议区分三件事：

1. 容器进程是否存活。
2. Gateway `/readyz` 或状态命令是否 ready。
3. channel sidecar、插件服务、meeting notes 等可选能力是否已启动。

如果 restart 变慢或 ready 抖动，先看 restart trace 和 Gateway 日志，不要直接扩大超时时间掩盖问题。

### 快速启动单容器

新环境推荐先走官方 Docker 初始化流程。下面固定本章已有的 `2026.9.4` 示例版本，避免镜像和脚本来自不同版本；升级时另选经过验证的 tag。

```bash
git clone --branch v2026.9.4 --depth 1 https://github.com/openclaw/openclaw.git
cd openclaw
export OPENCLAW_IMAGE=openclaw/openclaw:2026.9.4
./scripts/docker/setup.sh
```

脚本会准备目录与权限、运行 onboarding、配置 Gateway 并启动官方 Compose。完成后按终端提示打开 Control UI，使用初始化生成的 Gateway token。已有部署先备份配置、卷与外部工作区，再按原部署方式更新，不能直接拿新空卷替换。

下面继续说明手动 Compose。另建一个部署目录，在该目录保存 `docker-compose.yml` 和 `.env`；它使用独立项目和三个命名卷，不要在刚克隆的官方仓库里覆盖或混用 bind mount 部署。新卷沿用固定镜像预创建的 node（UID 1000）目录权限；已有卷或自定义 bind mount 仍要单独核对可写权限。

---

## docker-compose 完整配置详解

### 基础版：只跑 Gateway

最简单的配置，适合个人使用：

```yaml
# docker-compose.yml
services:
  openclaw-gateway:
    image: openclaw/openclaw:2026.9.4
    command: ["node", "dist/index.js", "gateway", "--bind", "lan", "--port", "18789"]
    container_name: openclaw-gateway
    ports:
      - "127.0.0.1:18789:18789"
    volumes:
      - openclaw-data:/home/node/.openclaw
      - openclaw-workspace:/home/node/.openclaw/workspace
      - openclaw-auth-secrets:/home/node/.config/openclaw
    environment:
      - OPENCLAW_GATEWAY_TOKEN=${OPENCLAW_GATEWAY_TOKEN:?Set OPENCLAW_GATEWAY_TOKEN in .env before initialization}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "node", "-e", "fetch('http://localhost:18789/health').then(r => { if (!r.ok) process.exit(1) })"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 15s

volumes:
  openclaw-data:
  openclaw-workspace:
  openclaw-auth-secrets:
```

### 进阶版：Gateway + 数据库 + Redis

如果你的自定义插件或外部业务另外需要 PostgreSQL、Redis，可以把它们放在同一个 Compose 项目中。下面是多服务编排示例；[官方 Docker 配置](https://github.com/openclaw/openclaw/blob/main/docker-compose.yml)并不要求这两个服务，默认记忆检索引擎使用 [SQLite](https://docs.openclaw.ai/concepts/memory)。仅添加 `DATABASE_URL` / `REDIS_URL` 不能证明 Gateway 已接入外部数据库，必须按实际组件的文档完成连接配置。只使用标准 Gateway 时，选上面的基础版即可。

```yaml
# docker-compose.yml
services:
  # ========== OpenClaw Gateway ==========
  openclaw-gateway:
    image: openclaw/openclaw:2026.9.4
    command: ["node", "dist/index.js", "gateway", "--bind", "lan", "--port", "18789"]
    container_name: openclaw-gateway
    ports:
      - "127.0.0.1:18789:18789"
    volumes:
      - openclaw-data:/home/node/.openclaw
      - openclaw-workspace:/home/node/.openclaw/workspace
      - openclaw-auth-secrets:/home/node/.config/openclaw
    environment:
      - OPENCLAW_GATEWAY_TOKEN=${OPENCLAW_GATEWAY_TOKEN:?Set OPENCLAW_GATEWAY_TOKEN in .env before initialization}
      # 以下连接串仅供明确支持这些变量的自定义组件使用
      - DATABASE_URL=postgresql://openclaw:${DB_PASSWORD:?Set DB_PASSWORD in .env for the advanced stack}@postgres:5432/openclaw
      - REDIS_URL=redis://redis:6379/0
      - NODE_ENV=production
      - LOG_LEVEL=info
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "node", "-e", "fetch('http://localhost:18789/health').then(r => { if (!r.ok) process.exit(1) })"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 15s
    networks:
      - openclaw-net

  # ========== PostgreSQL 数据库 ==========
  postgres:
    image: postgres:16-alpine
    container_name: openclaw-postgres
    environment:
      - POSTGRES_USER=openclaw
      - POSTGRES_PASSWORD=${DB_PASSWORD:?Set DB_PASSWORD in .env for the advanced stack}
      - POSTGRES_DB=openclaw
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U openclaw"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    networks:
      - openclaw-net

  # ========== Redis 缓存 ==========
  redis:
    image: redis:7-alpine
    container_name: openclaw-redis
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    networks:
      - openclaw-net

volumes:
  openclaw-data:
  openclaw-workspace:
  openclaw-auth-secrets:
  postgres-data:
  redis-data:

networks:
  openclaw-net:
    driver: bridge
```

### 启动和管理

先在独立部署目录保存你选择的 `docker-compose.yml`，再准备同目录的 `.env`。已有 `.env` 时保留并核对，下面的命令不覆盖旧文件。两个版本都需要随机 Gateway token，模型认证由 onboarding 完成：

```bash
set -eu
umask 077
if [ ! -e .env ]; then
  gateway_token=$(openssl rand -hex 32)
  printf 'OPENCLAW_GATEWAY_TOKEN=%s\n' "$gateway_token" > .env
  unset gateway_token
fi
```

**选进阶版的读者，还要在首次启动前准备数据库密码。** PostgreSQL 空数据卷初始化要求 `POSTGRES_PASSWORD` 非空，本例通过 `DB_PASSWORD` 传入。基础版没有数据库，跳过这一小步即可。

```bash
set -eu
umask 077
if ! grep -Eq '^[[:space:]]*(export[[:space:]]+)?DB_PASSWORD[[:space:]]*[:=]' .env; then
  db_password=$(openssl rand -hex 32)
  printf '\nDB_PASSWORD=%s\n' "$db_password" >> .env
  unset db_password
fi
```

生成的十六进制密码可以直接放进本例的连接串。已有 `DB_PASSWORD` 不会被替换；已有数据库也不会因改 `.env` 自动改密码。若现有值为空，按原部署的凭据补齐，不要为了通过检查给已有数据库随意换密码。[官方 PostgreSQL 镜像说明](https://github.com/docker-library/docs/blob/master/postgres/README.md)解释了空卷初始化与已有数据的区别。

两个版本准备好变量后，再按下面顺序检查、初始化。`config --quiet` 不输出配置内容；缺少或空的 token，或进阶版缺少或空的数据库密码，会在拉取和启动前报错。检查失败时先修 `.env`，不要继续 `up`。三个命名卷分别保存数据、workspace 和认证加密密钥，新部署只初始化一次，后续重建使用原来的卷。

```bash
docker compose config --quiet
docker compose pull openclaw-gateway
docker compose run --rm --no-deps --entrypoint node openclaw-gateway \
  dist/index.js onboard --mode local --no-install-daemon --gateway-auth token --gateway-token-ref-env OPENCLAW_GATEWAY_TOKEN
docker compose run --rm --no-deps --entrypoint node openclaw-gateway \
  dist/index.js config set gateway.mode local
docker compose run --rm --no-deps --entrypoint node openclaw-gateway \
  dist/index.js config set gateway.controlUi.allowedOrigins '["http://localhost:18789","http://127.0.0.1:18789"]' --strict-json
```

浏览器通过 SSH 隧道访问时可以沿用上面的本地 origin。用域名反代时，将实际 HTTPS origin 加入 `gateway.controlUi.allowedOrigins`，不要用通配符替代。保持 token 认证；生产实例上线前检查反代地址与 `gateway.trustedProxies`。

```bash
docker compose up -d                          # 启动所有服务（后台）
docker compose ps                             # 查看运行状态
docker compose logs -f                        # 实时查看日志
docker compose logs -f openclaw-gateway       # 只看 Gateway 日志
docker compose down                           # 停止所有服务
docker compose down -v                        # 停止并删除数据卷（谨慎！）
docker compose restart openclaw-gateway       # 重启单个服务
docker compose pull && docker compose up -d   # 更新镜像并重启
```

---

## 环境变量配置大全


### .env 文件模板

下面是字段说明模板。首次部署先按上文“启动和管理”准备并检查 `.env`；进阶版的 `DB_PASSWORD` 必须在第一次启动前就存在。不要用这份示例模板覆盖已有凭据：

```bash
# ========== 核心配置 ==========
# Gateway 访问令牌（必填）
OPENCLAW_GATEWAY_TOKEN=your-secure-token-here

# Gateway 访问密码（可选，与 Token 二选一或同时使用）
OPENCLAW_GATEWAY_PASSWORD=your-secure-password-here

# 运行环境
NODE_ENV=production

# 日志级别：silent, fatal, error, warn, info, debug, trace
LOG_LEVEL=info

# ========== 仅进阶版必填：PostgreSQL 初始化密码 ==========
DB_PASSWORD=your-strong-db-password

# ========== 模型提供商 API Keys ==========
# OpenAI
OPENAI_API_KEY=sk-proj-xxxxx

# Anthropic
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Google Gemini
GEMINI_API_KEY=AIzaSyxxxxx

# Azure OpenAI
AZURE_OPENAI_API_KEY=xxxxx
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com

# 本地模型（Ollama）
OLLAMA_BASE_URL=http://host.docker.internal:11434

# ========== 聊天平台集成 ==========
# Telegram
TELEGRAM_BOT_TOKEN=your-telegram-bot-token

# Discord
DISCORD_BOT_TOKEN=your-discord-bot-token

# Slack
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
SLACK_APP_TOKEN=xapp-your-slack-app-token

# ========== 可选配置 ==========
# 额外 apt 包（构建时安装）
OPENCLAW_DOCKER_APT_PACKAGES=ffmpeg imagemagick

# 持久化 home 目录
OPENCLAW_HOME_VOLUME=openclaw-home

# 额外挂载路径
OPENCLAW_EXTRA_MOUNTS=/path/to/data:/data
```

### 环境变量优先级

Docker Compose 中环境变量优先级（从高到低）：命令行 `-e` > `environment:` 直接设置 > `env_file:` > `.env` 文件 > 镜像默认值。

### 敏感信息处理

生产环境不要把密钥直接写在 docker-compose.yml 里。用 `${VARIABLE}` 引用 `.env` 文件中的值，或使用 Docker Secrets（Swarm 模式）。记得把 `.env` 加入 `.gitignore`。

---

## 数据持久化（Volumes 配置）

### 为什么需要 Volumes

Docker 容器是临时的 — 容器删了，里面的数据就没了。Volumes 把数据存在宿主机上，容器重建后数据还在。

### 关键数据目录

| 容器内路径 | 说明 | 是否需要持久化 |
|-----------|------|--------------|
| `/home/node/.openclaw` | OpenClaw 配置和数据 | 必须 |
| `/home/node/.openclaw/workspace` | 工作空间文件 | 必须 |
| `/home/node/.config/openclaw` | 认证加密密钥目录，须与认证数据配套保存 | 必须 |
| `/var/lib/postgresql/data` | 可选 PostgreSQL 服务的数据 | 启用该服务时必需 |
| `/data` | 可选 Redis 服务的持久化数据 | 需要保留该服务数据时备份 |

### Named Volumes vs Bind Mounts

```yaml
volumes:
  # Named Volume（推荐）— Docker 管理，性能好
  openclaw-data:/home/node/.openclaw

  # Bind Mount — 直接映射宿主机目录，方便查看文件
  ./local-data:/home/node/.openclaw
```

Named Volume 性能更好（尤其 macOS/Windows），可移植性高，Docker 自动处理权限。Bind Mount 方便直接查看和编辑文件，但依赖宿主机路径。

### 查看和管理 Volumes

Compose 默认给命名卷加上项目前缀。例如项目叫 `openclaw`，实际名称通常是 `openclaw_openclaw-data`。因此先从现有容器的挂载记录取名字；直接写 `-v openclaw-data:...` 可能新建一个空卷，得到一份看起来成功却没有业务数据的备份。下面是三卷 Gateway 的 Bash 备份示例，保存为 `scripts/backup.sh`，从 Compose 文件所在目录运行：

```bash
set -euo pipefail

# 列出所有 volumes
docker volume ls

GATEWAY_CONTAINER=$(docker compose ps -aq openclaw-gateway)
[ -n "$GATEWAY_CONTAINER" ] || { echo "没有找到 Gateway 容器" >&2; exit 1; }
DATA_VOLUME=$(docker inspect "$GATEWAY_CONTAINER" --format '{{range .Mounts}}{{if and (eq .Type "volume") (eq .Destination "/home/node/.openclaw")}}{{.Name}}{{end}}{{end}}')
WORKSPACE_VOLUME=$(docker inspect "$GATEWAY_CONTAINER" --format '{{range .Mounts}}{{if and (eq .Type "volume") (eq .Destination "/home/node/.openclaw/workspace")}}{{.Name}}{{end}}{{end}}')
AUTH_SECRET_VOLUME=$(docker inspect "$GATEWAY_CONTAINER" --format '{{range .Mounts}}{{if and (eq .Type "volume") (eq .Destination "/home/node/.config/openclaw")}}{{.Name}}{{end}}{{end}}')
[ -n "$DATA_VOLUME" ] && [ -n "$WORKSPACE_VOLUME" ] && [ -n "$AUTH_SECRET_VOLUME" ] || { echo "本例要求三个独立命名卷；绑定目录请按实际路径备份" >&2; exit 1; }
docker volume inspect "$DATA_VOLUME" "$WORKSPACE_VOLUME" "$AUTH_SECRET_VOLUME"

# 在维护窗口内先停止写入；原始 tar 不能保证运行中 SQLite/WAL 的一致性
GATEWAY_WAS_RUNNING=$(docker inspect "$GATEWAY_CONTAINER" --format '{{.State.Running}}')
docker compose stop openclaw-gateway
BACKUP_DIR="$PWD/openclaw-volume-backup-$(date +%Y%m%d_%H%M%S)"
mkdir -m 700 "$BACKUP_DIR"

# workspace 是独立挂载，必须单独备份
docker run --rm -v "$DATA_VOLUME":/source:ro -v "$BACKUP_DIR":/backup \
  alpine tar czf /backup/openclaw-data.tar.gz -C /source .
docker run --rm -v "$WORKSPACE_VOLUME":/source:ro -v "$BACKUP_DIR":/backup \
  alpine tar czf /backup/openclaw-workspace.tar.gz -C /source .
docker run --rm -v "$AUTH_SECRET_VOLUME":/source:ro -v "$BACKUP_DIR":/backup \
  alpine tar czf /backup/openclaw-auth-secrets.tar.gz -C /source .
tar -tzf "$BACKUP_DIR/openclaw-auth-secrets.tar.gz" >/dev/null
tar -tzf "$BACKUP_DIR/openclaw-data.tar.gz" >/dev/null
tar -tzf "$BACKUP_DIR/openclaw-workspace.tar.gz" >/dev/null

# 确认备份命令成功后，只恢复此前运行的 Gateway
if [ "$GATEWAY_WAS_RUNNING" = true ]; then
  docker compose start openclaw-gateway
fi
```

这段只演示三个 OpenClaw 卷的备份；包含部署文件、镜像记录和外部服务的示例见下文。若中途失败，Gateway 会保持停止，先排查再手动启动。恢复时也要读取目标容器的实际挂载，先保留现有数据，再使用空卷；不要把旧 tar 直接叠加到正在使用的数据库目录。

---

## 网络配置

### 端口映射

OpenClaw 使用多个端口提供不同服务：

| 端口 | 服务 | 说明 |
|------|------|------|
| 18789 | Gateway | 主服务入口 |
| 18790 | Bridge | 内部桥接通信 |
| 18791 | Browser Control | 浏览器控制接口 |
| 18793 | Canvas Host | 画布渲染服务 |
| 18800-18899 | Browser CDP | Chrome DevTools Protocol 端口池 |

```yaml
ports:
  # 格式：宿主机端口:容器端口
  # 注意：下面两种 Gateway 映射是二选一，不能同时保留，否则 18789 会被映射两次
  - "18789:18789"              # Gateway 主服务（对外暴露）
  # - "127.0.0.1:18789:18789"  # 生产环境改用这条：只监听本地，更安全
  - "18790:18790"              # Bridge
  - "18791:18791"              # Browser Control
  - "18793:18793"              # Canvas Host
  - "18800-18899:18800-18899"  # Browser CDP 端口池
```

> **安全提示**：生产环境建议绑定 `127.0.0.1`，通过反向代理暴露服务，不要直接把端口开放到公网。只有 Gateway（18789）需要对外暴露，其他端口仅在需要时映射。

> **反向代理 Forwarded Headers 安全提示（v2026.4.x+）**：OpenClaw 现在会检查转发头（`X-Forwarded-For` / `X-Forwarded-Host` / `X-Forwarded-Proto`）的一致性。即使请求通过 loopback 到达，如果携带了指向非本地来源的转发头，Gateway 会将该请求视为远程请求，不再享有 loopback 本地信任。反向代理必须**覆盖**（而非追加）来自客户端的转发头。如果使用 trusted-proxy 认证模式，需要在 `gateway.trustedProxies` 中配置代理 IP，且不能使用 loopback 地址。详见 [10-安全配置指南](10-安全配置指南.md)。

### Docker 网络模式

```yaml
services:
  openclaw-gateway:
    networks:
      - openclaw-net    # bridge 模式（默认，推荐）
    # network_mode: host  # host 模式（性能最好，但没有隔离）
```

### 容器间通信

在同一个 Docker 网络中，容器可以通过服务名互相访问：

```dotenv
# 供支持这些连接串的自定义组件使用；服务名在 Compose 网络内解析
DATABASE_URL=postgresql://openclaw:password@postgres:5432/openclaw
REDIS_URL=redis://redis:6379/0
```

### 连接宿主机服务

如果 Ollama 跑在宿主机上，容器里用 `host.docker.internal` 访问：

```yaml
environment:
  - OLLAMA_BASE_URL=http://host.docker.internal:11434
extra_hosts:
  - "host.docker.internal:host-gateway"   # Linux 需要这行
```

---

## 生产环境部署最佳实践

### Nginx 反向代理配置

生产环境不要直接暴露 OpenClaw 端口，用 Nginx 做反向代理：

```nginx
# /etc/nginx/sites-available/openclaw.conf
server {
    listen 80;
    server_name openclaw.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name openclaw.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/openclaw.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/openclaw.yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;

    add_header Strict-Transport-Security "max-age=63072000" always;
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    client_max_body_size 50M;

    location / {
        proxy_pass http://127.0.0.1:18789;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        # 重要：使用 = 赋值覆盖客户端传入的转发头，不要追加
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_send_timeout 300s;
    }
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/openclaw.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### SSL/TLS 证书配置

**Let's Encrypt（免费）：**

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d openclaw.yourdomain.com
sudo certbot renew --dry-run   # 验证自动续期
```

**Caddy（更简单，自动 HTTPS）：**

```
# /etc/caddy/Caddyfile
openclaw.yourdomain.com {
    reverse_proxy 127.0.0.1:18789
}
```

Caddy 自动申请和续期证书，比 Nginx + certbot 省事得多。

### 日志管理

#### Docker 日志驱动配置

```yaml
services:
  openclaw-gateway:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"     # 单个日志文件最大 10MB
        max-file: "5"       # 最多保留 5 个文件
        compress: "true"    # 压缩旧日志
```

#### 查看和分析日志

```bash
docker compose logs -f openclaw-gateway          # 实时查看
docker compose logs --tail 100 openclaw-gateway   # 最近 100 行
docker compose logs --since "2024-01-01" openclaw-gateway  # 按时间过滤
```

#### 集中式日志（生产推荐）

> ⏭️ **小白可跳过** — 这部分面向运维专家，单机部署不需要

多节点部署建议用 Loki + Grafana 或 ELK 收集日志，通过 `fluentd` 日志驱动转发。

### 健康检查

```yaml
services:
  openclaw-gateway:
    healthcheck:
      # 检查 Gateway 是否响应（注意：OpenClaw 镜像中没有 curl，使用 Node.js fetch）
      test: ["CMD", "node", "-e", "fetch('http://localhost:18789/health').then(r => { if (!r.ok) process.exit(1) })"]
      interval: 30s       # 每 30 秒检查一次
      timeout: 10s        # 超时时间
      retries: 3          # 连续失败 3 次标记为 unhealthy
      start_period: 15s   # 启动后等 15 秒再开始检查
```

配合监控告警，可以写一个简单的 cron 脚本检查 `docker inspect --format='{{.State.Health.Status}}' openclaw-gateway` 的输出，unhealthy 时发邮件并自动重启。

### 生产上线工坊：从空 VPS 到可维护服务

下面是一条适合个人、小团队和开源项目维护者的生产部署路径。它的目标不是"把容器跑起来"，而是让你以后能更新、排错、恢复。

假设服务器是 Ubuntu，域名是 `openclaw.example.com`，部署目录是 `/opt/openclaw`。

第一步，创建专用目录：

```bash
sudo mkdir -p /opt/openclaw
sudo chown -R $USER:$USER /opt/openclaw
cd /opt/openclaw
```

第二步，准备 `.env`：

```bash
umask 077
touch .env
```

写入最小配置：

```dotenv
NODE_ENV=production
OPENCLAW_GATEWAY_PORT=18789
OPENCLAW_GATEWAY_TOKEN=replace-with-long-random-token

OPENAI_API_KEY=${OPENAI_API_KEY}
ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
```

下面的端口映射把宿主机入口限制在 `127.0.0.1`，由 Nginx/Caddy 对外服务。容器内的 Gateway 仍需监听容器网络，不能把容器里的 loopback 和宿主机的 loopback 混为一谈。

第三步，准备新部署的 `docker-compose.yml`。已有部署要保留原来的卷与工作区挂载，不能直接新增空卷遮住原数据；先备份，再单独规划迁移。

```yaml
services:
  openclaw-gateway:
    image: openclaw/openclaw:2026.9.4
    command: ["node", "dist/index.js", "gateway", "--bind", "lan", "--port", "18789"]
    container_name: openclaw-gateway
    env_file:
      - .env
    ports:
      - "127.0.0.1:18789:18789"
    volumes:
      - openclaw-home:/home/node/.openclaw
      - openclaw-workspace:/home/node/.openclaw/workspace
      - openclaw-auth-secrets:/home/node/.config/openclaw
      - ./logs:/var/log/openclaw
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "node", "-e", "fetch('http://localhost:18789/health').then(r => { if (!r.ok) process.exit(1) })"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 20s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "5"

volumes:
  openclaw-home:
  openclaw-workspace:
  openclaw-auth-secrets:
```

第四步，先初始化，再启动。新部署使用上文“启动和管理”的 onboarding、`gateway.mode` 和 origin 配置步骤；域名反代时把 `https://openclaw.example.com` 换成实际 HTTPS origin 加入允许列表。初始化后再运行：

```bash
docker compose pull
docker compose up -d
docker compose ps
docker compose logs --tail 100 openclaw-gateway
```

第五步，本机探测：

```bash
curl -i http://127.0.0.1:18789/health
```

第六步，再配置反向代理和 TLS。确认反代能访问后，再尝试外部访问域名。不要在 Gateway 没有 token、没有 TLS、没有反代限制时把 `18789` 直接暴露到公网。

### 上线后的目录布局

一个容易维护的部署目录可以这样组织：

```text
/opt/openclaw/
├── docker-compose.yml
├── .env
├── logs/
├── backups/
│   ├── 2026-06-09T030000+0800/
│   └── ...
├── scripts/
│   ├── backup.sh
│   ├── restore-stack.sh
│   ├── update.sh
│   └── health.sh
└── README.ops.md
```

`README.ops.md` 不是给用户看的文档，而是给未来的你看的操作笔记。建议记录：

```markdown
# OpenClaw 运维笔记

## 服务器

- 域名：openclaw.example.com
- 部署目录：/opt/openclaw
- Gateway 内部端口：127.0.0.1:18789
- 反向代理：Nginx

## 常用命令

- 启动：docker compose up -d
- 日志：docker compose logs -f openclaw-gateway
- 更新：bash scripts/update.sh
- 备份：bash scripts/backup.sh

## 注意

- 不直接开放 18789 到公网。
- 更新前先备份 volume 和 .env。
- 恢复后必须重建/确认记忆索引。
```

有了这个文件，新成员或一个月后的你都不会靠记忆操作生产服务。

---

## 云平台部署

### AWS 部署

#### EC2 + Docker Compose

```bash
# 推荐 t3.medium: 2 vCPU, 4GB RAM
ssh -i your-key.pem ubuntu@ec2-xx-xx-xx-xx.compute-1.amazonaws.com
curl -fsSL https://get.docker.com | sh && sudo usermod -aG docker ubuntu
git clone https://github.com/openclaw/openclaw.git && cd openclaw
cp .env.example .env   # 编辑 .env 填入配置
docker compose up -d
```

#### AWS ECS（容器服务）

适合需要自动扩缩容的场景。在 AWS 控制台创建 ECS 任务定义，指定镜像 `openclaw/openclaw:latest`，端口映射 `18789:18789`，分配 2048MB 内存和 1024 CPU 单位。详细配置参考 [AWS ECS 文档](https://docs.aws.amazon.com/ecs/)。

### GCP 部署

#### Cloud Run（Serverless）

```bash
# 构建并推送镜像到 GCR
gcloud builds submit --tag gcr.io/your-project/openclaw

# 部署到 Cloud Run
gcloud run deploy openclaw \
  --image gcr.io/your-project/openclaw \
  --port 18789 \
  --memory 2Gi \
  --cpu 2 \
  --set-env-vars "NODE_ENV=production" \
  --allow-unauthenticated
```

#### GCE（虚拟机）

创建 `e2-medium` 实例，SSH 连接后安装 Docker 并部署（流程同 EC2）。

### Azure 部署

#### Azure Container Instances

```bash
# 创建资源组
az group create --name openclaw-rg --location eastus

# 部署容器
az container create \
  --resource-group openclaw-rg \
  --name openclaw \
  --image openclaw/openclaw:latest \
  --ports 18789 \
  --cpu 2 \
  --memory 4 \
  --environment-variables NODE_ENV=production
```

### 阿里云部署

#### ECS + Docker

```bash
# 1. 创建 ECS 实例（推荐 ecs.c6.large: 2 vCPU, 4GB）
# 2. SSH 连接后安装 Docker
ssh root@your-ecs-ip
curl -fsSL https://get.docker.com | sh

# 配置阿里云镜像加速器
sudo tee /etc/docker/daemon.json <<-'EOF'
{ "registry-mirrors": ["https://your-id.mirror.aliyuncs.com"] }
EOF
sudo systemctl daemon-reload && sudo systemctl restart docker

# 部署
git clone https://github.com/openclaw/openclaw.git
cd openclaw && docker compose up -d
```

### VPS 部署（Hetzner / Vultr / DigitalOcean）

性价比最高的方案，适合个人和小团队（约 $5-10/月）：

```bash
ssh root@your-vps-ip
curl -fsSL https://get.docker.com | sh
git clone https://github.com/openclaw/openclaw.git
cd openclaw && ./docker-setup.sh
```

#### 远程访问方案

Gateway 默认绑定 `127.0.0.1`，外部无法直接访问。三种方案：

**方案一：SSH 隧道（最简单）**

```bash
# 在本地机器上
ssh -L 18789:127.0.0.1:18789 root@your-vps-ip
# 然后本地浏览器访问 http://127.0.0.1:18789/
```

**方案二：Tailscale（推荐长期使用）**

```bash
# VPS 和本地都安装 Tailscale
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up
# 通过 Tailscale IP 访问：http://100.x.x.x:18789/
```

**方案三：反向代理 + HTTPS（对外服务）**

参考上面的 Nginx 或 Caddy 配置。

---

## Agent 沙箱（Docker 隔离）

Docker 在 OpenClaw 中扮演双重角色：一是容器化部署 Gateway 本身，二是为 Agent 工具执行提供沙箱隔离。这两者是独立的概念：

- **Gateway 容器化** — 整个 OpenClaw 跑在 Docker 里
- **Agent 沙箱** — Gateway 跑在主机上（或容器里），但 Agent 的工具执行在独立的 Docker 容器中

沙箱的核心价值：Agent 执行的代码（shell 命令、脚本等）被限制在隔离容器中，即使代码有破坏性操作也不会影响宿主机。

### 沙箱模式

OpenClaw 的沙箱通过 `agents.defaults.sandbox.mode` 控制。配置文件位于 `~/.openclaw/openclaw.json`（JSON5 格式）：

```jsonc
// ~/.openclaw/openclaw.json
{
  "agents": {
    "defaults": {
      "sandbox": {
        // "non-main" — 非主会话在 Docker 沙箱中运行（推荐）
        // "all"      — 所有会话都在沙箱中运行
        // "off"      — 关闭沙箱
        "mode": "non-main",
        "docker": { "image": "openclaw:sandbox" }
      }
    }
  }
}
```

`"non-main"` 表示非主会话使用沙箱，并不是只隔离某几个 Agent。默认沙箱关闭；启用后还要检查实际会话键、workspace 访问方式和容器挂载。对所有会话都要求隔离时选择 `"all"`。

### 沙箱镜像类型

| 镜像 | 说明 | 大小 |
|------|------|------|
| `Dockerfile.sandbox` | 基础沙箱，最小化 | ~200MB |
| `Dockerfile.sandbox-browser` | 带浏览器（Playwright） | ~800MB |
| `Dockerfile.sandbox-common` | 通用沙箱，常用工具齐全 | ~500MB |

### 构建沙箱镜像

```bash
# 基础沙箱
docker build -t openclaw:sandbox -f Dockerfile.sandbox .

# 带浏览器的沙箱
docker build -t openclaw:sandbox-browser -f Dockerfile.sandbox-browser .
```

### Podman Rootless 替代方案

如果你的环境不允许使用 Docker 或需要无 root 权限运行容器，OpenClaw 官方支持 Podman rootless 部署。

**核心区别：** Podman 以当前用户身份运行容器（`--userns=keep-id`），不需要 Docker 守护进程，也不需要 root 权限。

**快速开始：**

```bash
# 一键初始化（构建镜像 + 创建配置 + 启动 Gateway）
./scripts/podman/setup.sh

# 使用 CLI 管理容器化的 Gateway
openclaw --container <容器名> gateway status
```

**SELinux 环境：** Podman 启动脚本会自动检测 SELinux 状态，在 enforcing/permissive 模式下自动为挂载目录追加 `:Z` 选项，无需手动配置。

**Systemd 集成（Quadlet）：** 使用 `--quadlet` 标志可生成 systemd 用户服务，支持开机自启和 `systemctl --user` 管理。需要 `loginctl enable-linger` 以支持 SSH/无头环境下的持久运行。

**端口绑定：** 默认只绑定 `127.0.0.1`（Gateway 18789，Bridge 18790），可通过 `OPENCLAW_PODMAN_GATEWAY_HOST_PORT` 等环境变量覆盖。

> 详细的 Podman 部署文档见 [docs.openclaw.ai/install/podman](https://docs.openclaw.ai/install/podman)。

---

## 自动更新和 CI/CD

### Watchtower 自动更新

Watchtower 会自动检测镜像更新并重启容器：

```yaml
# 添加到 docker-compose.yml
services:
  watchtower:
    image: containrrr/watchtower
    container_name: watchtower
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - WATCHTOWER_CLEANUP=true
      - WATCHTOWER_POLL_INTERVAL=86400   # 每 24 小时检查一次
      - WATCHTOWER_INCLUDE_STOPPED=false
    restart: unless-stopped
```

### GitHub Actions CI/CD

```yaml
# .github/workflows/deploy.yml
name: Deploy OpenClaw
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to server
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /opt/openclaw
            docker compose pull && docker compose up -d
            docker image prune -f
```

### 手动更新流程

```bash
docker compose pull                    # 拉取最新镜像
docker compose up -d                   # 重启服务
docker image prune -f                  # 清理旧镜像
```

### 更新与回滚工坊

不要把更新理解成三条命令。生产环境更新应该包含“记录当前版本、备份、更新、观察、必要时回滚”。

先记录当前镜像：

```bash
cd /opt/openclaw
docker compose images
docker inspect openclaw-gateway --format '{{.Image}}'
```

更新前备份。下面调用前文的 Gateway 三卷脚本；使用含 PostgreSQL、Redis 的扩展示例时，改用后文的 `scripts/backup-stack.sh`：

```bash
bash scripts/backup.sh
```

拉取新镜像但先不清理旧镜像：

```bash
docker compose pull
docker compose up -d
docker compose ps
docker compose logs --tail 200 openclaw-gateway
```

观察这几件事：

```bash
curl -i http://127.0.0.1:18789/health
docker inspect openclaw-gateway --format='{{.State.Health.Status}}'
docker compose logs --since "10m" openclaw-gateway
```

如果新版本异常，先保留日志和旧镜像，确认旧版仍能读取当前配置与数据库。兼容性已确认时，才改回固定 tag 或旧 digest：

```yaml
services:
  openclaw-gateway:
    image: openclaw/openclaw:<previous-tag>
```

然后重启：

```bash
docker compose up -d
docker compose logs --tail 100 openclaw-gateway
```

如果数据结构已经迁移，先停止写入，按下文恢复流程用升级前的已验证备份和匹配镜像恢复；不要只换镜像就让旧版读取迁移后的数据库。

可以把更新流程写成脚本，但脚本里不要自动删除旧镜像：

```bash
#!/usr/bin/env bash
set -euo pipefail

cd /opt/openclaw
echo "[1/5] backup"
bash scripts/backup.sh

echo "[2/5] current image"
docker inspect openclaw-gateway --format '{{.Image}}' || true

echo "[3/5] pull"
docker compose pull

echo "[4/5] restart"
docker compose up -d

echo "[5/5] health"
sleep 10
docker compose ps
curl -i http://127.0.0.1:18789/health
```

更新成功并观察一段时间后，再清理：

```bash
docker image prune -f
```

---

## 性能调优和资源限制

> ⏭️ **小白可跳过** — 这部分面向运维专家，单机部署不需要

### 容器资源限制

防止单个容器吃光服务器资源：

```yaml
services:
  openclaw-gateway:
    deploy:
      resources:
        limits:
          cpus: "2.0"
          memory: 4G
        reservations:
          cpus: "0.5"
          memory: 512M
  postgres:
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 2G
  redis:
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 512M
```

### Docker 守护进程优化

编辑 `/etc/docker/daemon.json`，配置日志轮转、overlay2 存储驱动、文件描述符限制：

```json
{
  "log-driver": "json-file",
  "log-opts": { "max-size": "10m", "max-file": "3" },
  "storage-driver": "overlay2",
  "default-ulimits": {
    "nofile": { "Name": "nofile", "Hard": 65536, "Soft": 65536 }
  }
}
```

### 监控资源使用

> ⏭️ **小白可跳过** — 这部分面向运维专家，单机部署不需要

```bash
docker stats                          # 实时查看所有容器资源
docker stats openclaw-gateway         # 查看特定容器
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"  # 格式化输出
```

---

## 备份和恢复

### 全量备份脚本

下面针对本章包含可选 PostgreSQL、Redis 服务的多服务示例，使用 Bash。只部署基础版 Gateway 时，用前面的三卷备份流程即可。保存为 `scripts/backup-stack.sh`，从 `docker-compose.yml` 所在目录运行。运行前安排维护窗口，并停止其他会写入这些卷的程序；脚本会暂时停止 Gateway 和 Redis，结束时恢复它们原先的运行状态。备份归档可能包含凭据，目录权限限制为仅当前用户可读。自定义外置数据库、工作区和挂载不在这份示例里，需另外纳入备份。

```bash
#!/bin/bash
# backup-stack.sh — 备份本章 Compose 示例的数据和部署记录
set -euo pipefail
umask 077
BACKUP_DIR="/opt/backups/openclaw"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_PATH="${BACKUP_DIR}/${DATE}"
mkdir -p "$BACKUP_DIR"
# 同一秒重复执行时退出，避免覆盖上一份备份
mkdir "$BACKUP_PATH"

volume_at() {
  docker inspect "$1" --format "{{range .Mounts}}{{if and (eq .Type \"volume\") (eq .Destination \"$2\")}}{{.Name}}{{end}}{{end}}"
}

GATEWAY_CONTAINER=$(docker compose ps -aq openclaw-gateway)
REDIS_CONTAINER=$(docker compose ps -aq redis)
[ -n "$GATEWAY_CONTAINER" ] && [ -n "$REDIS_CONTAINER" ] || { echo "缺少示例中的 Gateway 或 Redis 容器" >&2; exit 1; }
DATA_VOLUME=$(volume_at "$GATEWAY_CONTAINER" /home/node/.openclaw)
WORKSPACE_VOLUME=$(volume_at "$GATEWAY_CONTAINER" /home/node/.openclaw/workspace)
AUTH_SECRET_VOLUME=$(volume_at "$GATEWAY_CONTAINER" /home/node/.config/openclaw)
REDIS_VOLUME=$(volume_at "$REDIS_CONTAINER" /data)
[ -n "$DATA_VOLUME" ] && [ -n "$WORKSPACE_VOLUME" ] && [ -n "$AUTH_SECRET_VOLUME" ] && [ -n "$REDIS_VOLUME" ] || { echo "挂载不是本例要求的命名卷，请按实际挂载另做备份" >&2; exit 1; }
docker volume inspect "$DATA_VOLUME" "$WORKSPACE_VOLUME" "$AUTH_SECRET_VOLUME" "$REDIS_VOLUME" >/dev/null

# 记录实际镜像，恢复时要用同一个版本；latest 本身不能锁定恢复点
GATEWAY_IMAGE_ID=$(docker inspect "$GATEWAY_CONTAINER" --format '{{.Image}}')
printf '%s\n' "$GATEWAY_IMAGE_ID" > "$BACKUP_PATH/gateway-image-id.txt"
docker image inspect "$GATEWAY_IMAGE_ID" --format '{{json .RepoDigests}}' > "$BACKUP_PATH/gateway-image-digests.json"
date -Is > "$BACKUP_PATH/backup-time.txt"

# 备份配置文件
cp docker-compose.yml .env "$BACKUP_PATH/"

GATEWAY_WAS_RUNNING=$(docker inspect "$GATEWAY_CONTAINER" --format '{{.State.Running}}')
REDIS_WAS_RUNNING=$(docker inspect "$REDIS_CONTAINER" --format '{{.State.Running}}')
resume_services() {
  if [ "$REDIS_WAS_RUNNING" = true ]; then docker compose start redis; fi
  if [ "$GATEWAY_WAS_RUNNING" = true ]; then docker compose start openclaw-gateway; fi
}
trap resume_services EXIT
docker compose stop openclaw-gateway redis

# 备份 OpenClaw 数据卷
docker run --rm \
  -v "$DATA_VOLUME":/source:ro \
  -v "$BACKUP_PATH":/backup \
  alpine tar czf /backup/openclaw-data.tar.gz -C /source .

# 备份 OpenClaw workspace 卷
# 独立挂载不会被上一条只挂载数据卷的 tar 捎带上
docker run --rm \
  -v "$WORKSPACE_VOLUME":/source:ro \
  -v "$BACKUP_PATH":/backup \
  alpine tar czf /backup/openclaw-workspace.tar.gz -C /source .

# 认证加密密钥必须与数据一起备份
docker run --rm \
  -v "$AUTH_SECRET_VOLUME":/source:ro \
  -v "$BACKUP_PATH":/backup \
  alpine tar czf /backup/openclaw-auth-secrets.tar.gz -C /source .

# PostgreSQL 用逻辑备份，服务需要在线
docker compose exec -T postgres \
  pg_dump -U openclaw openclaw | gzip > "$BACKUP_PATH/db-backup.sql.gz"

# 备份 Redis
docker run --rm \
  -v "$REDIS_VOLUME":/source:ro \
  -v "$BACKUP_PATH":/backup \
  alpine tar czf /backup/redis-data.tar.gz -C /source .

# 检查归档可读；是否真的能恢复，还要做下文的恢复演练
for archive in openclaw-data openclaw-workspace openclaw-auth-secrets redis-data; do
  tar -tzf "$BACKUP_PATH/$archive.tar.gz" >/dev/null
done
gzip -t "$BACKUP_PATH/db-backup.sql.gz"
echo "Backup archives checked: $BACKUP_PATH"
```

脚本故意不在末尾自动删除旧备份。恢复演练通过后，再按你的保留策略清理；本地自建镜像还要另存或传输对应镜像，卷备份里没有程序包。

> **v2026.5.22 备份命名**：新版更倾向使用 local-time backup archive names。生产脚本里建议保留时区信息或在备份目录旁写入 `date -Is` 输出，方便跨服务器恢复时判断备份先后。

### 恢复流程

下面演示把这份多服务备份恢复到新机器或空的演练环境。先在独立目录放好备份中的 `docker-compose.yml` 和 `.env`，根据 `gateway-image-digests.json` 把 Gateway 的 `image` 锁到备份时的 digest；本地自建镜像需先导入匹配镜像。确认容器名不会和其他部署冲突，再运行脚本。已有部署要先另存当前状态；脚本会拒绝已有容器和非空目标卷。保存为 `scripts/restore-stack.sh`，从演练目录运行。

```bash
#!/bin/bash
# restore-stack.sh — 把备份恢复到本章 Compose 示例的空卷
set -euo pipefail
BACKUP_PATH=$(cd "${1:?Usage: bash scripts/restore-stack.sh /absolute/path/to/backup}" && pwd)

for archive in openclaw-data openclaw-workspace openclaw-auth-secrets redis-data; do
  tar -tzf "$BACKUP_PATH/$archive.tar.gz" >/dev/null
done
gzip -t "$BACKUP_PATH/db-backup.sql.gz"

# 本例只恢复到空环境，发现已有容器就退出，避免误操作其他部署
if [ -n "$(docker compose ps -aq)" ]; then
  echo "当前 Compose 项目已有容器，请换用独立的空演练项目" >&2
  exit 1
fi
# 创建目标容器以读取实际挂载，但不启动服务
docker compose create

volume_at() {
  docker inspect "$1" --format "{{range .Mounts}}{{if and (eq .Type \"volume\") (eq .Destination \"$2\")}}{{.Name}}{{end}}{{end}}"
}
GATEWAY_CONTAINER=$(docker compose ps -aq openclaw-gateway)
REDIS_CONTAINER=$(docker compose ps -aq redis)
POSTGRES_CONTAINER=$(docker compose ps -aq postgres)
DATA_VOLUME=$(volume_at "$GATEWAY_CONTAINER" /home/node/.openclaw)
WORKSPACE_VOLUME=$(volume_at "$GATEWAY_CONTAINER" /home/node/.openclaw/workspace)
AUTH_SECRET_VOLUME=$(volume_at "$GATEWAY_CONTAINER" /home/node/.config/openclaw)
REDIS_VOLUME=$(volume_at "$REDIS_CONTAINER" /data)
POSTGRES_VOLUME=$(volume_at "$POSTGRES_CONTAINER" /var/lib/postgresql/data)
[ -n "$DATA_VOLUME" ] && [ -n "$WORKSPACE_VOLUME" ] && [ -n "$AUTH_SECRET_VOLUME" ] && [ -n "$REDIS_VOLUME" ] && [ -n "$POSTGRES_VOLUME" ] || { echo "目标挂载不是本例要求的命名卷" >&2; exit 1; }
docker volume inspect "$DATA_VOLUME" "$WORKSPACE_VOLUME" "$AUTH_SECRET_VOLUME" "$REDIS_VOLUME" "$POSTGRES_VOLUME" >/dev/null

EXPECTED_IMAGE_ID=$(cat "$BACKUP_PATH/gateway-image-id.txt")
ACTUAL_IMAGE_ID=$(docker inspect "$GATEWAY_CONTAINER" --format '{{.Image}}')
[ "$ACTUAL_IMAGE_ID" = "$EXPECTED_IMAGE_ID" ] || { echo "Gateway 镜像与备份不匹配；先恢复匹配镜像，再重试" >&2; exit 1; }

# 拒绝覆盖已有数据，避免混合不同代的 SQLite / WAL 或其他数据库文件
for volume in "$DATA_VOLUME" "$WORKSPACE_VOLUME" "$AUTH_SECRET_VOLUME" "$REDIS_VOLUME" "$POSTGRES_VOLUME"; do
  docker run --rm -v "$volume":/target:ro alpine \
    sh -c 'if [ "$1" = "$2" ]; then
      test ! -L /target/workspace &&
      test -z "$(find /target -mindepth 1 ! -path /target/workspace -print -quit)" &&
      { test ! -e /target/workspace || test -d /target/workspace; }
    else
      test -z "$(find /target -mindepth 1 -maxdepth 1 -print -quit)"
    fi' sh "$volume" "$DATA_VOLUME" \
    || { echo "目标卷已有数据，停止恢复：$volume" >&2; exit 1; }
done

# 恢复数据卷
docker run --rm -v "$DATA_VOLUME":/target -v "$BACKUP_PATH":/backup:ro \
  alpine tar xzf /backup/openclaw-data.tar.gz -C /target

# 恢复 workspace 卷（记忆与技能所在，必须单独恢复）
docker run --rm -v "$WORKSPACE_VOLUME":/target -v "$BACKUP_PATH":/backup:ro \
  alpine tar xzf /backup/openclaw-workspace.tar.gz -C /target

# 恢复认证加密密钥，必须与本次数据备份匹配
docker run --rm -v "$AUTH_SECRET_VOLUME":/target -v "$BACKUP_PATH":/backup:ro \
  alpine tar xzf /backup/openclaw-auth-secrets.tar.gz -C /target

# 恢复 Redis
docker run --rm -v "$REDIS_VOLUME":/target -v "$BACKUP_PATH":/backup:ro \
  alpine tar xzf /backup/redis-data.tar.gz -C /target

# 恢复 PostgreSQL：等到服务就绪，不固定假设 5 秒足够
docker compose up -d postgres
ready=false
for attempt in $(seq 1 60); do
  if docker compose exec -T postgres pg_isready -U openclaw >/dev/null 2>&1; then
    ready=true
    break
  fi
  sleep 1
done
[ "$ready" = true ] || { echo "PostgreSQL 未就绪，停止恢复" >&2; exit 1; }
gunzip -c "$BACKUP_PATH/db-backup.sql.gz" | \
  docker compose exec -T postgres psql -v ON_ERROR_STOP=1 -U openclaw openclaw

# 启动所有服务
docker compose up -d
echo "Restore completed from: ${BACKUP_PATH}"
```

### 定时备份（Cron）

用 `crontab -e` 编辑现有任务，追加下面一行，每天凌晨 3 点运行。使用有备份目录和日志文件写权限的账号，先手动验证同一条命令能成功。

```cron
0 3 * * * cd /opt/openclaw && bash scripts/backup-stack.sh >> /var/log/openclaw-backup.log 2>&1
```

### 恢复演练：备份不是存下来就结束

很多部署事故不是没有备份，而是从来没恢复过。建议在非生产目录做一次恢复演练。

创建演练目录：

```bash
mkdir -p /opt/openclaw-restore-drill
cd /opt/openclaw-restore-drill
```

复制备份时保存的部署文件和恢复脚本。下面的备份路径是示例，请换成你已经校验过的备份：

```bash
BACKUP_PATH=/opt/backups/openclaw/20260914_030000
cp "$BACKUP_PATH/docker-compose.yml" "$BACKUP_PATH/.env" .
mkdir -p scripts
cp /opt/openclaw/scripts/restore-stack.sh scripts/
```

按备份中的镜像记录固定 Gateway digest；同时删除演练 Compose 中三个服务的 `container_name`，让 Compose 用独立项目名生成容器名，避免与生产容器冲突。

把端口改成演练端口，避免碰到生产实例：

```yaml
ports:
  - "127.0.0.1:28789:18789"
```

在 Compose 顶层设置独立项目名，保留原来的五个卷声明及服务挂载；不要给卷指定生产环境的 `name` 或 `external`：

```yaml
name: openclaw-restore-drill
```

确认当前终端没有指向生产项目的 `COMPOSE_PROJECT_NAME`，也不要传生产项目的 `-p` 参数。这时五个实际卷名都应以 `openclaw-restore-drill_` 开头；恢复脚本会从容器挂载读取它们，无需手改脚本里的卷名。执行恢复后检查服务：

```bash
bash scripts/restore-stack.sh "$BACKUP_PATH"
docker compose ps
curl -i http://127.0.0.1:28789/health
docker compose logs --tail 100 openclaw-gateway
```

然后进入容器或通过 OpenClaw 命令确认关键数据存在：

```bash
docker compose exec openclaw-gateway ls -la /home/node/.openclaw
```

演练结束后停止演练服务：

```bash
docker compose down
```

这一步保留演练卷。确认恢复结果、项目名和实际卷名后，再按需清理；下次演练也可以使用新的项目名。恢复演练可以按月安排，并在升级或备份流程变更后重做。除了能解压和启动，还要检查代表性的会话、工作区文件与记忆是否完整。

### Volume 安全：不要让数据跟容器一起消失

容器可以随时删除，数据不应该。OpenClaw 的配置、记忆、会话、认证资料都应该放在 volume 或 bind mount 中。

危险做法：

```yaml
services:
  openclaw-gateway:
    image: openclaw/openclaw:latest
    ports:
      - "127.0.0.1:18789:18789"
```

这个配置没有持久化挂载。容器重建后，你可能丢失工作空间。

稳妥做法：

```yaml
services:
  openclaw-gateway:
    image: openclaw/openclaw:latest
    volumes:
      - openclaw-home:/home/node/.openclaw

volumes:
  openclaw-home:
```

如果你选择 bind mount，也要明确宿主机路径和权限：

```yaml
services:
  openclaw-gateway:
    volumes:
      - ./data/openclaw:/home/node/.openclaw
```

设置权限：

```bash
mkdir -p /opt/openclaw/data/openclaw
sudo chown -R 1000:1000 /opt/openclaw/data/openclaw
chmod 700 /opt/openclaw/data/openclaw
```

Named volume 管理省心，bind mount 方便备份和人工查看。生产中二者都可以，关键是不要无挂载运行。

---

## 常见 Docker 问题排查

### 镜像构建失败

```bash
docker build --no-cache -t openclaw:local -f Dockerfile .   # 清理缓存重建
docker build --progress=plain -t openclaw:local -f Dockerfile .  # 详细输出
docker system prune -a   # 磁盘空间不足时清理
```

### 容器无法启动

```bash
# 查看容器日志
docker compose logs openclaw-gateway

# 查看退出原因
docker inspect openclaw-gateway --format='{{.State.ExitCode}} {{.State.Error}}'

# 进入容器调试（运行中）
docker compose exec openclaw-gateway /bin/bash

# 容器已停止时用 run
docker compose run --rm openclaw-gateway /bin/bash
```

### 端口冲突

```bash
lsof -i :18789          # 检查端口占用
ss -tlnp | grep 18789   # 或者用 ss
# 解决方案：在 docker-compose.yml 中改为 "28789:18789"
```

### 权限问题

```bash
docker compose exec openclaw-gateway ls -la /home/node/.openclaw   # 检查权限
docker compose exec openclaw-gateway chown -R node:node /home/node/.openclaw  # 修复
```

### 内存不足（OOM Killed）

```bash
docker inspect openclaw-gateway --format='{{.State.OOMKilled}}'  # 检查 OOM
docker stats openclaw-gateway --no-stream                         # 查看内存使用
# 解决方案：增加 deploy.resources.limits.memory 或升级服务器
```

### 网络连接问题

```bash
# 检查容器网络
docker network inspect openclaw-net

# 容器间连通性测试
docker compose exec openclaw-gateway ping postgres
```

### 数据卷挂载问题

```bash
GATEWAY_CONTAINER=$(docker compose ps -aq openclaw-gateway)
[ -n "$GATEWAY_CONTAINER" ] || { echo "没有找到 Gateway 容器" >&2; exit 1; }
docker inspect "$GATEWAY_CONTAINER" --format '{{json .Mounts}}'
# Gateway 运行时，从实际挂载检查内容
docker compose exec openclaw-gateway ls -la /home/node/.openclaw
docker compose exec openclaw-gateway ls -la /home/node/.openclaw/workspace
```

### Docker Compose 版本问题

确认使用 v2 语法（`docker compose`，不带横杠）。v1 的 `docker-compose` 已弃用，v2 内置在 Docker Engine 中。

### 反向代理后登录或 WebSocket 异常

如果页面能打开，但聊天一直断开、WebChat 没有响应，优先检查反代是否保留了升级头：

```nginx
proxy_http_version 1.1;
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection "upgrade";
proxy_read_timeout 300s;
```

如果日志里的来源 IP 全是 `127.0.0.1`，检查 `X-Forwarded-For`：

```nginx
proxy_set_header X-Forwarded-For $remote_addr;
proxy_set_header X-Real-IP $remote_addr;
```

不要把客户端传来的 `X-Forwarded-For` 直接追加进信任链。生产安全配置里应该由反向代理覆盖这些头。

### 更新后模型或消息平台不可用

按环境变量、容器、应用三层查：

```bash
# 1. 宿主机 .env 是否还在
ls -la /opt/openclaw/.env

# 2. 容器是否拿到环境变量
docker compose exec openclaw-gateway env | grep -E "OPENAI|ANTHROPIC|TELEGRAM|DISCORD"

# 3. OpenClaw 自身状态
docker compose logs --tail 200 openclaw-gateway
```

如果 `.env` 没问题但容器里没有变量，检查 `env_file` 是否写在正确 service 下。如果容器有变量但平台仍失败，检查平台 token 是否过期或 webhook 地址是否变更。

### 磁盘空间突然打满

先看 Docker 占用：

```bash
docker system df
docker ps -a --size
```

再看日志：

```bash
du -sh /var/lib/docker/containers/* 2>/dev/null | sort -h | tail
du -sh /opt/openclaw/logs
```

处理顺序：

1. 确认备份存在。
2. 清理停止容器和未使用镜像。
3. 调整 logging max-size/max-file。
4. 不要直接删除 volume，除非你确认里面不是 OpenClaw 数据。

```bash
docker container prune
docker image prune
```

---

## 快速参考卡片

### 常用命令速查

| 操作 | 命令 |
|------|------|
| 启动服务 | `docker compose up -d` |
| 停止服务 | `docker compose down` |
| 查看状态 | `docker compose ps` |
| 查看日志 | `docker compose logs -f` |
| 重启服务 | `docker compose restart` |
| 更新镜像 | `docker compose pull && docker compose up -d` |
| 进入容器 | `docker compose exec openclaw-gateway /bin/bash` |
| 资源监控 | `docker stats` |
| 清理空间 | `docker system prune -a` |

### 部署方案对比

| 方案 | 成本 | 难度 | 适用场景 |
|------|------|------|---------|
| VPS + Docker Compose | $5-10/月 | 低 | 个人/小团队 |
| AWS EC2 | $15-50/月 | 中 | 中小团队 |
| AWS ECS | $20-100/月 | 高 | 需要自动扩缩容 |
| GCP Cloud Run | 按用量计费 | 中 | Serverless 场景 |
| 阿里云 ECS | ¥50-200/月 | 低 | 国内用户 |

---

## 下一步

Docker 部署搞定了！去 [10. 安全配置指南](10-安全配置指南.md) 加固你的 AI 助手。
