# Dockerfile
FROM ubuntu:22.04

# ffmpegとPython3（dateutil用）をインストール
RUN apt-get update && \
    apt-get install -y ffmpeg python3 python3-pip && \
    pip3 install python-dateutil && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY monitor.py /app/monitor.py

# 監視対象ディレクトリをコンテナ起動時に引数で指定
ENTRYPOINT ["python3", "monitor.py"]
