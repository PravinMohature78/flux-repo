FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
RUN git config --system --add safe.directory /repos/interview-local/.git
COPY server.py /server.py
CMD ["python", "/server.py"]
