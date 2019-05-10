FROM python:3.7
COPY pip.conf /root/.pip/pip.conf
RUN pip3 install --no-cache ptvsd
COPY debug/requirements .
RUN pip3 install -r requirements
EXPOSE 3000
WORKDIR /opt/
CMD ["/bin/bash", "debug.sh"]
