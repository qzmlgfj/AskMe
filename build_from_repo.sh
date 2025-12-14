#!/bin/bash

set -e

# 配置集中管理
REPO_DIR="${REPO_DIR:-$HOME/repo/AskMe}"
DEPLOY_DIR="${DEPLOY_DIR:-$HOME/askme}"
PORT="${PORT:-5000}"
APP_MODULE="ask_me:create_app()"

# DOCKER 相关配置
DOCKER_IMAGE_NAME="${DOCKER_IMAGE_NAME:-askme:latest}"
REGISTRY="${REGISTRY:-}"
NAMESPACE="${NAMESPACE:-antrol}"
IMAGE_BASENAME="${IMAGE_BASENAME:-askme}"  
ENV_SUFFIX="${ENV_SUFFIX:-dev}"


# 颜色与状态提示函数
color_echo() {
    local color="$1"
    shift
    local message="$@"
    local prefix=""
    case "$color" in
        "red")    prefix="❌"; code="31";;
        "green")  prefix="✅"; code="32";;
        "yellow") prefix="⚠️ "; code="33";;
        "blue")   prefix="🔷"; code="34";;
        "purple") prefix="🟣"; code="35";;
        "cyan")   prefix="🔹"; code="36";;
        "white")  prefix="ℹ️ "; code="37";;
        *)        prefix="";   code="0";;
    esac
    echo -e "\e[1;${code}m${prefix} $message\e[0m"
}

# 统一的目录切换函数
cd_safe() {
    cd "$1" || { color_echo "red" "进入目录 $1 失败"; return 1; }
}

# 统一的虚拟环境管理
activate_venv() {
    source "$1/venv/bin/activate" || { color_echo "red" "虚拟环境激活失败: $1"; return 1; }
}

# 安全执行命令
exec_safe() {
    local cmd="$1"
    local error_msg="$2"
    if ! eval "$cmd"; then
        color_echo "red" "$error_msg"
        return 1
    fi
}

# 错误处理
cleanup() {
    local exit_code="$?"
    if [ "$exit_code" -ne 0 ]; then
        color_echo "red" "脚本执行中断，退出码：$exit_code"
        echo -e "\e[1;31m请检查上方日志信息排查问题。\e[0m"
    fi
    set +e
}
trap cleanup EXIT

get_package_version() {
    python - << 'EOF'
import pathlib, re

init_path = pathlib.Path("ask_me/__init__.py")
text = init_path.read_text(encoding="utf-8")

m = re.search(r"""__version__\s*=\s*['"]([^'"]+)['"]""", text)
print(m.group(1) if m else "0.0.0")
EOF
}

# 主要部署流程
main() {
    clear
    color_echo "cyan" "🚀 正在部署 AskMe 项目..."

    # === 拉取代码 ===
    echo -e "\n\e[1;36m========== 🔁 拉取最新代码 ==========\e[0m"
    cd_safe "$REPO_DIR" || return 1
    exec_safe "git pull origin master" "git pull 失败" || return 1
    color_echo "green" "代码更新完成。"

    # === 启用 Python 虚拟环境并安装依赖 ===
    echo -e "\n\e[1;36m========== 🐍 启用 Python 虚拟环境 ==========\e[0m"
    activate_venv "$REPO_DIR" || return 1
    color_echo "green" "虚拟环境已激活。"

    echo -e "\n\e[1;36m========== 📦 安装后端依赖 ==========\e[0m"
    exec_safe "pip install -r requirements.txt" "pip 安装依赖失败" || return 1
    color_echo "green" "后端依赖安装完成。"

    # === 前端构建 ===
    echo -e "\n\e[1;36m========== 🛠️ 安装并构建前端 ==========\e[0m"
    cd_safe "$REPO_DIR/frontend" || return 1
    exec_safe "npm ci" "npm install 失败" || return 1
    color_echo "green" "npm install 完成。"

    exec_safe "npm run build" "npm build 构建失败" || return 1
    color_echo "green" "前端构建完成。"
    cd_safe "$REPO_DIR" || return 1

    # === 构建 Python 分发包 ===
    echo -e "\n\e[1;36m========== 📦 构建 .whl 包 ==========\e[0m"
    rm -rf dist/*
    exec_safe "python setup.py bdist_wheel" "构建 .whl 包失败" || return 1
    color_echo "green" ".whl 构建成功。"

     # === 读取版本号，生成规范镜像名 ===
    VERSION="$(get_package_version)"
    if [ -z "$VERSION" ]; then
        VERSION="0.0.0"
    fi
    if [ -n "$REGISTRY" ]; then
        DOCKER_IMAGE_NAME="${REGISTRY}/${NAMESPACE}/${IMAGE_BASENAME}:${VERSION}-${ENV_SUFFIX}"
    else
        DOCKER_IMAGE_NAME="${NAMESPACE}/${IMAGE_BASENAME}:${VERSION}-${ENV_SUFFIX}"
    fi
    color_echo "white" "当前包版本: $VERSION"
    color_echo "white" "规范 Docker 镜像名: $DOCKER_IMAGE_NAME"
    # ===（可选）构建 Docker 镜像 ===
    if [ "$BUILD_DOCKER_IMAGE" = "1" ]; then
        echo -e "\n\e[1;36m========== 🐳 构建 Docker 镜像 ==========\\e[0m"
        exec_safe "docker build -t '$DOCKER_IMAGE_NAME' '$REPO_DIR'" "Docker 镜像构建失败" || return 1
        color_echo "green" "Docker 镜像构建完成：$DOCKER_IMAGE_NAME"
    else
        color_echo "blue" "跳过 Docker 镜像构建（如需构建，设置 BUILD_DOCKER_IMAGE=1）"
    fi


    # === 部署到目标目录 ===
    if [ "$BUILD_DOCKER_IMAGE" != "1" ]; then
        echo -e "\n\e[1;36m========== 📁 部署新包 ==========\e[0m"
        activate_venv "$DEPLOY_DIR" || return 1
        exec_safe "pip install --force-reinstall '$REPO_DIR'/   dist/*.whl" ".whl 安装失败" || return 1
        color_echo "green" ".whl 安装完成。"

        # === 重启服务 ===
        echo -e "\n\e[1;36m========== ☠️ 检查并重启服务     ==========\e[0m"
        if pkill -f "gunicorn.*$APP_MODULE" 2>/dev/null; then
            color_echo "yellow" "已终止旧的 gunicorn 进程"
        else
            color_echo "blue" "未发现运行中的服务进程"
        fi

        echo -e "\n\e[1;36m========== 🚀 启动服务 ==========\e[0m"
        cd_safe "$DEPLOY_DIR" || return 1
        exec_safe "gunicorn -b '127.0.0.1:$PORT' -D --log-file  './askme.log' '$APP_MODULE'" "服务启动失败" || return 1
        color_echo "green" "服务启动成功，监听端口 $PORT 🎉"
    fi
}

# 执行主函数并处理错误
if ! main "$@"; then
    color_echo "red" "部署过程中遇到错误，请检查上方日志信息"
    exit 1
fi

trap - EXIT
set +e