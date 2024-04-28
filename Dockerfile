FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    minisat \
 && rm -rf /var/lib/apt/lists/*

COPY . /app

COPY requirements.txt /app/
RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "server.py"]
