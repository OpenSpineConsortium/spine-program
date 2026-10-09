# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): service/Dockerfile [tracked at 097933a]
FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 OMP_NUM_THREADS=4 HF_HOME=/tmp/hf
RUN apt-get update && apt-get install -y --no-install-recommends libglib2.0-0 libgl1 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --index-url https://download.pytorch.org/whl/cpu torch==2.6.0 torchvision==0.21.0 && pip install -r requirements.txt
COPY app.py model_defs.py ./
RUN useradd -m app && chown -R app /app && mkdir -p /tmp/weights /tmp/hf && chown -R app /tmp/weights /tmp/hf
USER app
EXPOSE 7860
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860", "--workers", "1"]
