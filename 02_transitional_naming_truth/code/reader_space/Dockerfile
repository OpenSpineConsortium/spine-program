FROM python:3.11-slim
RUN useradd -m -u 1000 user
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# app.py imports carm and viewport; copying app.py alone builds cleanly and dies on first start
COPY app.py carm.py viewport.py ./
RUN chown -R user:user /app
USER user
ENV HOME=/home/user PORT=7860 GRADIO_SERVER_NAME=0.0.0.0
EXPOSE 7860
CMD ["python", "app.py"]
