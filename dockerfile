FROM python:3.7
COPY pip.conf /root/.pip/pip.conf
RUN pip install --no-cache ptvsd
COPY requirements .
RUN pip install -r requirements
EXPOSE 3000
WORKDIR /opt/
CMD ["python", "py"]
