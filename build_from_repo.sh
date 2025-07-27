#!/bin/bash

set -e

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

clear
color_echo "cyan" "🚀 正在部署 AskMe 项目..."

# === 拉取代码 ===
echo -e "\n\e[1;36m========== 🔁 拉取最新代码 ==========\e[0m"
cd ~/repo/AskMe || { color_echo "red" "进入项目目录失败。"; exit 1; }
git pull origin master || { color_echo "red" "git pull 失败。"; exit 1; }
color_echo "green" "代码更新完成。"

# === 启用 Python 虚拟环境 ===
echo -e "\n\e[1;36m========== 🐍 启用 Python 虚拟环境 ==========\e[0m"
source venv/bin/activate || { color_echo "red" "虚拟环境激活失败。"; exit 1; }
color_echo "green" "虚拟环境已激活。"

# === 安装 Python 依赖 ===
echo -e "\n\e[1;36m========== 📦 安装后端依赖 ==========\e[0m"
pip3 install -r requirements.txt || { color_echo "red" "pip 安装依赖失败。"; exit 1; }
color_echo "green" "后端依赖安装完成。"

# === 前端构建 ===
echo -e "\n\e[1;36m========== 🛠️ 安装并构建前端 ==========\e[0m"
cd frontend
npm install || { color_echo "red" "npm install 失败。"; exit 1; }
color_echo "green" "npm install 完成。"

npm run build || { color_echo "red" "npm build 构建失败。"; exit 1; }
color_echo "green" "前端构建完成。"
cd ..

# === 构建 Python 分发包 ===
echo -e "\n\e[1;36m========== 📦 构建 .whl 包 ==========\e[0m"
rm -rf dist/*
python setup.py sdist bdist_wheel || { color_echo "red" "构建 .whl 包失败。"; exit 1; }
color_echo "green" ".whl 构建成功。"

# === 拷贝并安装新包 ===
echo -e "\n\e[1;36m========== 📁 拷贝新包并安装 ==========\e[0m"
rm -rf ~/askme/*.whl
cp dist/*.whl ~/askme/
color_echo "green" "包已拷贝到 ~/askme/"

deactivate

cd ~/askme/
source venv/bin/activate
pip3 install --force-reinstall *.whl || { color_echo "red" ".whl 安装失败。"; exit 1; }
color_echo "green" ".whl 安装完成。"

# === 杀死旧进程 ===
echo -e "\n\e[1;36m========== ☠️ 检查端口并关闭旧进程 ==========\e[0m"
if pids=$(lsof -ti:5000); [ -n "$pids" ]; then
    color_echo "yellow" "检测到端口 5000 被占用，进程号：$pids"
    kill $pids
    color_echo "green" "已终止旧进程。"
else
    color_echo "blue" "端口 5000 当前未被占用。"
fi

# === 启动服务 ===
echo -e "\n\e[1;36m========== 🚀 启动服务 ==========\e[0m"
gunicorn -b 127.0.0.1:5000 -D --log-file "./askme.log" "ask_me:create_app()" || { color_echo "red" "服务启动失败。"; exit 1; }
color_echo "green" "服务启动成功，监听端口 5000 🎉"

trap - EXIT
set +e