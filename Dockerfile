FROM python
COPY requirements.txt /requirements.txt
COPY main.py /main.py
COPY cogs/ /cogs/
COPY utils/ /utils/

RUN python3 -m pip install -r /requirements.txt
CMD ["python3", "main.py"]