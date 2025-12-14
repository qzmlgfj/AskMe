FROM python:3.11-slim

ENV TZ=Asia/Shanghai \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# 如果有编译扩展，可以保留 build-essential；如果 requirements 里全是纯 Python，可去掉
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# 从宿主机拷贝刚刚 build_from_repo.sh 生成的 whl
# （build_from_repo.sh 已经 rm -rf dist/* 并构建了新的 .whl）
COPY dist/*.whl /dist/

RUN pip install --no-cache-dir gunicorn \
    && pip install --no-cache-dir /dist/*.whl

# SQLite 默认放 /app/instance/backend.sqlite（AskMe 里就是这个目录）
RUN mkdir -p /app/instance

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "ask_me:create_app()"]
