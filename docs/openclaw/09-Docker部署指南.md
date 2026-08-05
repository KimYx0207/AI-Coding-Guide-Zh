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

**环境一致性** — 本地能跑的，服务器上一定能跑。不会出现"我这里没问题啊"的经典场景。Docker 把 Node.js 版本、系统依赖、配置文件全部打包在一起，消除了环境差异。

**一键部署** — 不需要在服务器上手动装 Node.js、配置 npm、处理依赖冲突。一条 `docker compose up` 搞定一切。

**隔离性** — OpenClaw 跑在自己的容器里，不会污染宿主机环境。你可以在同一台机器上跑多个版本的 OpenClaw，互不干扰。

**易于迁移** — 想换服务器？把 docker-compose.yml（Docker 的编排工具，用一个配置文件管理多个容器）和数据卷拷过去，几分钟就能恢复。

**Agent 沙箱** — Docker 天然适合做 Agent 工具执行的沙箱。通过 `agents.defaults.sandbox.mode` 配置（默认 `"non-main"`），非主会话的 Agent 自动在独立 Docker 容器中隔离执行，不会搞坏宿主机。

**回滚方便** — 升级出问题？切回上一个镜像（容器的模板，包含了运行所需的一切）版本就行，数据都在 volume（数据卷，让容器重启后数据不丢失）里，不受影响。

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
docker pull openclaw/openclaw:v2026.6.8  # 指定稳定版本
docker images | grep openclaw           # 查看本地镜像
```

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
| `latest` | 最新稳定版 | 生产环境 |
| `vYYYY.M.D` | 指定版本号（如 `v2026.6.8`） | 需要版本锁定 |
| `nightly` | 每日构建 | 尝鲜新功能 |
| `local` | 本地构建 | 自定义需求 |

### Gateway ready 与 restart trace

v2026.5.22 对 Gateway 启动路径做了多处性能和诊断优化：插件元数据、channel catalog、startup-idle plugin work、ACPX runtime 会尽量延迟或缓存，Gateway ready 信号不再被未用到的 handler tree 阻塞。

生产部署的健康检查建议区分三件事：

1. 容器进程是否存活。
2. Gateway `/readyz` 或状态命令是否 ready。
3. channel sidecar、插件服务、meeting notes 等可选能力是否已启动。

如果 restart 变慢或 ready 抖动，先看 restart trace 和 Gateway 日志，不要直接扩大超时时间掩盖问题。

### 快速启动单容器

不想写 docker-compose.yml？一条命令也能跑：

```bash
docker run -d --name openclaw-gateway -p 18789:18789 \
  -v ~/.openclaw:/home/node/.openclaw \
  -e OPENCLAW_GATEWAY_TOKEN=your-token-here \
  --restart unless-stopped openclaw/openclaw:latest
```

但对于生产环境，强烈建议用 Docker Compose。

---

## docker-compose 完整配置详解

### 基础版：只跑 Gateway

最简单的配置，适合个人使用：

```yaml
# docker-compose.yml
version: "3.8"

services:
  openclaw-gateway:
    image: openclaw/openclaw:latest
    container_name: openclaw-gateway
    ports:
      - "18789:18789"
    volumes:
      - openclaw-data:/home/node/.openclaw
      - openclaw-workspace:/home/node/.openclaw/workspace
    environment:
      - OPENCLAW_GATEWAY_TOKEN=${OPENCLAW_GATEWAY_TOKEN}
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
```

### 进阶版：Gateway + 数据库 + Redis

适合团队使用，需要持久化存储和缓存：

```yaml
# docker-compose.yml
version: "3.8"

services:
  # ========== OpenClaw Gateway ==========
  openclaw-gateway:
    image: openclaw/openclaw:latest
    container_name: openclaw-gateway
    ports:
      - "18789:18789"
    volumes:
      - openclaw-data:/home/node/.openclaw
      - openclaw-workspace:/home/node/.openclaw/workspace
    environment:
      - OPENCLAW_GATEWAY_TOKEN=${OPENCLAW_GATEWAY_TOKEN}
      - DATABASE_URL=postgresql://openclaw:${DB_PASSWORD}@postgres:5432/openclaw
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
      - POSTGRES_PASSWORD=${DB_PASSWORD}
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
  postgres-data:
  redis-data:

networks:
  openclaw-net:
    driver: bridge
```

### 启动和管理

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

在 `docker-compose.yml` 同目录下创建 `.env` 文件：

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

# ========== 数据库配置 ==========
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
| `/var/lib/postgresql/data` | PostgreSQL 数据 | 必须 |
| `/data` | Redis 持久化数据 | 推荐 |

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

```bash
# 列出所有 volumes
docker volume ls

# 查看 volume 详情
docker volume inspect openclaw-data

# 备份 volume 到 tar 文件
docker run --rm -v openclaw-data:/source:ro -v $(pwd):/backup \
  alpine tar czf /backup/openclaw-data-backup.tar.gz -C /source .

# 从 tar 恢复 volume
docker run --rm -v openclaw-data:/target -v $(pwd):/backup \
  alpine tar xzf /backup/openclaw-data-backup.tar.gz -C /target

# 删除未使用的 volumes（谨慎）
docker volume prune
```

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
  - "18789:18789"              # Gateway 主服务
  - "18790:18790"              # Bridge
  - "18791:18791"              # Browser Control
  - "18793:18793"              # Canvas Host
  - "18800-18899:18800-18899"  # Browser CDP 端口池
  - "127.0.0.1:18789:18789"   # 只监听本地（更安全，替代上面的 18789 映射）
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

```yaml
# Gateway 连接数据库，用服务名 "postgres" 而不是 IP
DATABASE_URL=postgresql://openclaw:password@postgres:5432/openclaw

# Gateway 连接 Redis
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
OPENCLAW_GATEWAY_HOST=127.0.0.1
OPENCLAW_GATEWAY_PORT=18789
OPENCLAW_GATEWAY_TOKEN=replace-with-long-random-token

OPENAI_API_KEY=${OPENAI_API_KEY}
ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
```

`OPENCLAW_GATEWAY_HOST=127.0.0.1` 很重要。生产环境让 Nginx/Caddy 对外服务，Gateway 自己只监听本机，减少直接暴露面。

第三步，准备 `docker-compose.yml`：

```yaml
services:
  openclaw-gateway:
    image: openclaw/openclaw:latest
    container_name: openclaw-gateway
    env_file:
      - .env
    ports:
      - "127.0.0.1:18789:18789"
    volumes:
      - openclaw-home:/home/node/.openclaw
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
```

第四步，启动：

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
│   ├── restore.sh
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
        "image": "openclaw:sandbox"
      }
    }
  }
}
```

`"non-main"` 是推荐的默认值：主会话直接在宿主环境执行以保证交互性能，而 Agent 派生的子会话自动在 Docker 容器中隔离运行，防止工具执行影响宿主机。

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

更新前备份：

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

如果新版本异常，先不要 `docker image prune`。改回固定 tag 或旧 digest：

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

如果数据结构已经被新版本迁移，回滚镜像未必够用，需要恢复备份。这就是更新前备份必须存在的原因。

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

```bash
#!/bin/bash
# backup.sh — OpenClaw 全量备份
BACKUP_DIR="/opt/backups/openclaw"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p "${BACKUP_DIR}/${DATE}"

# 备份配置文件
cp docker-compose.yml .env "${BACKUP_DIR}/${DATE}/"

# 备份 OpenClaw 数据卷
docker run --rm \
  -v openclaw-data:/source:ro \
  -v "${BACKUP_DIR}/${DATE}":/backup \
  alpine tar czf /backup/openclaw-data.tar.gz -C /source .

# 备份 PostgreSQL
docker compose exec -T postgres \
  pg_dump -U openclaw openclaw | gzip > "${BACKUP_DIR}/${DATE}/db-backup.sql.gz"

# 备份 Redis
docker run --rm \
  -v redis-data:/source:ro \
  -v "${BACKUP_DIR}/${DATE}":/backup \
  alpine tar czf /backup/redis-data.tar.gz -C /source .

# 清理 30 天前的备份
find "${BACKUP_DIR}" -maxdepth 1 -type d -mtime +30 -exec rm -rf {} \;
echo "Backup completed: ${BACKUP_DIR}/${DATE}"
```

> **v2026.5.22 备份命名**：新版更倾向使用 local-time backup archive names。生产脚本里建议保留时区信息或在备份目录旁写入 `date -Is` 输出，方便跨服务器恢复时判断备份先后。

### 恢复流程

```bash
#!/bin/bash
# restore.sh — 从备份恢复
BACKUP_PATH=$1
[ -z "$BACKUP_PATH" ] && echo "Usage: ./restore.sh /opt/backups/openclaw/20240101_120000" && exit 1

# 停止服务
docker compose down

# 恢复配置
cp "${BACKUP_PATH}/docker-compose.yml" "${BACKUP_PATH}/.env" .

# 恢复数据卷
docker volume create openclaw-data
docker run --rm -v openclaw-data:/target -v "${BACKUP_PATH}":/backup \
  alpine tar xzf /backup/openclaw-data.tar.gz -C /target

# 恢复数据库
docker compose up -d postgres && sleep 5
gunzip -c "${BACKUP_PATH}/db-backup.sql.gz" | \
  docker compose exec -T postgres psql -U openclaw openclaw

# 恢复 Redis
docker volume create redis-data
docker run --rm -v redis-data:/target -v "${BACKUP_PATH}":/backup \
  alpine tar xzf /backup/redis-data.tar.gz -C /target

# 启动所有服务
docker compose up -d
echo "Restore completed from: ${BACKUP_PATH}"
```

### 定时备份（Cron）

```bash
# 每天凌晨 3 点自动备份
echo "0 3 * * * cd /opt/openclaw && bash backup.sh >> /var/log/openclaw-backup.log 2>&1" | crontab -
```

### 恢复演练：备份不是存下来就结束

很多部署事故不是没有备份，而是从来没恢复过。建议在非生产目录做一次恢复演练。

创建演练目录：

```bash
mkdir -p /opt/openclaw-restore-drill
cd /opt/openclaw-restore-drill
```

复制 compose 和备份：

```bash
cp /opt/openclaw/docker-compose.yml .
cp /opt/openclaw/.env .
```

把端口改成演练端口，避免碰到生产实例：

```yaml
ports:
  - "127.0.0.1:28789:18789"
```

恢复到新的 volume 名称，避免覆盖生产 volume：

```yaml
volumes:
  openclaw-home-drill:
```

运行恢复脚本前，确认脚本里的 volume 名称也指向演练 volume。恢复完成后：

```bash
docker compose up -d
curl -i http://127.0.0.1:28789/health
docker compose logs --tail 100 openclaw-gateway
```

然后进入容器或通过 OpenClaw 命令确认关键数据存在：

```bash
docker compose exec openclaw-gateway ls -la /home/node/.openclaw
```

演练结束后清理：

```bash
docker compose down
docker volume rm openclaw-restore-drill_openclaw-home-drill
```

恢复演练每月做一次就够。关键是确认三个东西：备份文件能解压、volume 能挂载、Gateway 能启动。

### Volume 安全：不要让数据跟容器一起消失

容器可以随时删除，数据不应该。OpenClaw 的配置、记忆、会话、认证资料都应该放在 volume 或 bind mount 中。

危险做法：

```yaml
services:
  openclaw-gateway:
    image: openclaw/openclaw:latest
    ports:
      - "18789:18789"
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
docker inspect openclaw-gateway | grep -A 10 Mounts   # 检查挂载
docker run --rm -v openclaw-data:/data alpine ls -la /data  # 查看 volume 内容
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
