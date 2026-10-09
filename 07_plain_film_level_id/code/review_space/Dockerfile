# The review tool as a Docker Space. Docker rather than the Gradio SDK because the Spaces this project can
# host on were created as Docker Spaces before the free tier changed, and a Docker Space accepts any server.
FROM python:3.11-slim

WORKDIR /app
RUN useradd -m -u 1000 user && chown -R user /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app.py /app/app.py
USER user
ENV HOME=/home/user \
    GRADIO_SERVER_NAME=0.0.0.0 \
    GRADIO_SERVER_PORT=7860 \
    HF_HOME=/home/user/.cache/huggingface \
    REVIEW_PORT=7860
EXPOSE 7860
CMD ["python", "app.py"]
