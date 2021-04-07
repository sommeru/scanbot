FROM ubuntu:20.04

RUN apt-get update 
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata
RUN apt-get install -y \
  autofs \
  cifs-utils

RUN echo /- /etc/auto.smb.shares --timeout 15 browse >> /etc/auto.master
RUN echo /mnt -fstype=cifs,rw,username=scan,password=99scan80,iocharset=utf8 ://10.0.0.31/scan >> /etc/auto.smb.shares

CMD service autofs restart
CMD bash

