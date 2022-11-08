FROM python:3.8-buster
RUN pip install ray cryptography
COPY . /ray-secrets-plugin
RUN pip install -e /ray-secrets-plugin
COPY examples/example.py script.py
CMD python script.py