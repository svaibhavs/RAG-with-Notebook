FROM registry.access.redhat.com/ubi9:9.4-1214.1726694543 AS env-build

RUN yum -y install gcc-toolset-13 
RUN source /opt/rh/gcc-toolset-13/enable

RUN curl -L https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-ppc64le.sh
RUN ./Anaconda3-2023.09-0-Linux-ppc64le.sh
