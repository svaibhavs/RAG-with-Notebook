FROM registry.access.redhat.com/ubi9:9.4-1214.1726694543 AS env-build

RUN yum -y install gcc-toolset-13 
RUN source /opt/rh/gcc-toolset-13/enable

# Install base utilities
RUN yum -y install -y wget
    
RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-ppc64le.sh -O ~/conda.sh && \
    /bin/bash ~/conda.sh -b -p /opt/conda

# Put conda in path so we can use conda activate
ENV PATH /opt/conda/bin:$PATH

RUN conda config --prepend channels rocketce
RUN conda config --append channels conda-forge
RUN conda install -y pytorch-cpu -c rocketce
RUN conda install -y gfortran -c conda-forge
RUN conda install -y openblas -c rocketce

RUN yum -y install -y git make cmake automake gcc gcc-c++ llvm-toolset pkgconfig perf

ENV PKG_CONFIG_PATH $HOME/anaconda3/lib/pkgconfig:$PKG_CONFIG_PATH
ENV LD_LIBRARY_PATH $HOME/anaconda3/lib:$LD_LIBRARY_PATH
RUN git clone https://github.com/ggerganov/llama.cpp
RUN cd llama.cpp
RUN make LLAMA_OPENBLAS=1
