FROM fedora:36

RUN dnf update --refresh && \
    dnf -y install python && \
    dnf -y install make && \
    dnf -y install pip

COPY . /home

CMD cd /home/ && \
    ls -la && \
    make install_packages && \
    make receive_data && \
    make post_process
