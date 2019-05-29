FROM centos:7.2.1511
RUN yum -y update --nogpgcheck && \
    yum groupinstall -y --nogpgcheck development && \
    yum install -y --nogpgcheck\
    yum-utils \
    https://mirrors.tuna.tsinghua.edu.cn/ius/stable/Redhat/7/x86_64/ius-release-1.0-15.ius.el7.noarch.rpm &&\
    yum install -y --nogpgcheck\
    bzip2-devel \
    git \
    hostname \
    openssl \
    openssl-devel \
    wget \
    sudo \
    tar \
    zlib-dev \
    libaio \
    libvirt-devel \
    which \
    python36u \
    python36u-devel \
    python36u-pip \
    gcc \
    mysql-devel
ADD . /ZOP
VOLUME /ZOP
WORKDIR /ZOP
RUN localedef -i en_US -f UTF-8 en_US.UTF-8
RUN pip3.6 install -r requirements.txt -i https://pypi.doubanio.com/simple


EXPOSE 5000
#ENTRYPOINT ["sh", "/ZOP/entrypoint.sh"]
CMD python3.6 /ZOP/web/manage.py run
