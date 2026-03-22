#!/bin/bash

# 移除 set -e，改用自定义错误处理机制
# set -e 会导致 SSH 连接直接断掉

set -o pipefail

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

BRANCH="${BRANCH:-master}"


# 颜色与状态提示函数
color_echo() {
    local color="$1"
    shift
    local message="$@"
    local prefix=""
    local code="0"
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

section() {
    local title="$1"
    echo -e "\n\e[1;36m========== ${title} ==========\e[0m"
}

run_step() {
    local title="$1"
    local cmd="$2"
    local error_msg="$3"

    section "$title"
    exec_safe "$cmd" "$error_msg"
}

# 统一的目录切换函数
cd_safe() {
    cd "$1" || { color_echo "red" "进入目录 $1 失败"; return 1; }
}

# 统一的虚拟环境管理
activate_venv() {
    source "$1/venv/bin/activate" 2>/dev/null || { color_echo "red" "虚拟环境激活失败: $1"; return 1; }
}

# 安全执行命令
exec_safe() {
    local cmd="$1"
    local error_msg="$2"
    if ! eval "$cmd"; then
        color_echo "red" "$error_msg"
        return 1
    fi
    return 0
}

# 错误处理
cleanup() {
    local exit_code="$?"
    if [ "$exit_code" -ne 0 ]; then
        color_echo "red" "脚本执行中断，退出码：$exit_code"
        echo -e "\e[1;31m请检查上方日志信息排查问题。\e[0m"
    fi
}
trap cleanup EXIT

get_package_version() {
    python - << 'EOF'
import pathlib, re

init_path = pathlib.Path("ask_me/version.py")
text = init_path.read_text(encoding="utf-8")

m = re.search(r"""__version__\s*=\s*['"]([^'"]+)['"]""", text)
print(m.group(1) if m else "0.0.0")
EOF
}

get_docker_image_name() {
    local version="$1"
    if [ -n "$REGISTRY" ]; then
        echo "${REGISTRY}/${NAMESPACE}/${IMAGE_BASENAME}:${version}-${ENV_SUFFIX}"
    else
        echo "${NAMESPACE}/${IMAGE_BASENAME}:${version}-${ENV_SUFFIX}"
    fi
}

build_frontend() {
    local version="$1"
    cd_safe "$REPO_DIR/frontend" || return 1
    exec_safe "npm ci" "npm install 失败" || return 1
    color_echo "green" "npm install 完成。"

    exec_safe "VITE_APP_VERSION='${version}' npm run build" "npm build 构建失败" || return 1
    color_echo "green" "前端构建完成。"
    cd_safe "$REPO_DIR" || return 1
}

# 主要部署流程
main() {
    clear
    color_echo "cyan" "🚀 正在部署 AskMe 项目..."

    cd_safe "$REPO_DIR" || return 1

    # === 拉取代码 ===
    run_step "🔁 拉取最新代码" "git pull origin '${BRANCH}'" "git pull 失败" || return 1
    color_echo "green" "代码更新完成。"

    # === 启用 Python 虚拟环境并安装依赖 ===
    activate_venv "$REPO_DIR" || return 1
    color_echo "green" "虚拟环境已激活。"

    run_step "📦 安装后端依赖" "pip install -r requirements.txt" "pip 安装依赖失败" || return 1
    color_echo "green" "后端依赖安装完成。"

    # === 读取版本号（单一事实源），供前端构建与镜像标签复用 ===
    VERSION="$(get_package_version)"
    if [ -z "$VERSION" ]; then
        VERSION="0.0.0"
    fi
    color_echo "white" "当前包版本: $VERSION"

    DOCKER_IMAGE_NAME="$(get_docker_image_name "$VERSION")"
    color_echo "white" "规范 Docker 镜像名: $DOCKER_IMAGE_NAME"

    # === 前端构建 ===
    section "🛠️ 安装并构建前端"
    build_frontend "$VERSION" || return 1

    # === 构建 Python 分发包 ===
    rm -rf dist/*
    run_step "📦 构建 .whl 包" "python setup.py bdist_wheel" "构建 .whl 包失败" || return 1
    color_echo "green" ".whl 构建成功。"

    # ===（可选）构建 Docker 镜像 ===
    if [ "$BUILD_DOCKER_IMAGE" = "1" ]; then
        run_step "🐳 构建 Docker 镜像" "docker build --build-arg APP_VERSION='${VERSION}' -t '${DOCKER_IMAGE_NAME}' '${REPO_DIR}'" "Docker 镜像构建失败" || return 1
        color_echo "green" "Docker 镜像构建完成：$DOCKER_IMAGE_NAME"
    else
        color_echo "blue" "跳过 Docker 镜像构建（如需构建，设置 BUILD_DOCKER_IMAGE=1）"
    fi


    # === 部署到目标目录 ===
    if [ "$BUILD_DOCKER_IMAGE" != "1" ]; then
        activate_venv "$DEPLOY_DIR" || return 1
        run_step "📁 部署新包" "pip install --force-reinstall '${REPO_DIR}'/dist/*.whl" ".whl 安装失败" || return 1
        color_echo "green" ".whl 安装完成。"

        # === 重启服务 ===
        section "☠️ 检查并重启服务"
        if pkill -f "gunicorn.*$APP_MODULE" 2>/dev/null; then
            color_echo "yellow" "已终止旧的 gunicorn 进程"
        else
            color_echo "blue" "未发现运行中的服务进程"
        fi

        section "🚀 启动服务"
        cd_safe "$DEPLOY_DIR" || return 1
        exec_safe "gunicorn -b '127.0.0.1:$PORT' -D --log-file './askme.log' '$APP_MODULE'" "服务启动失败" || return 1
        color_echo "green" "服务启动成功，监听端口 $PORT 🎉"
    fi
}

# 执行主函数并处理错误
if ! main "$@"; then
    color_echo "red" "部署过程中遇到错误，请检查上方日志信息"
    exit 1
fi

trap - EXIT
