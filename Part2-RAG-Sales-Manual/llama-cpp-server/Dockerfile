FROM registry.access.redhat.com/ubi9:9.4-1214.1726694543 AS env-build

RUN yum -y install gcc-toolset-13 
RUN source /opt/rh/gcc-toolset-13/enable

# Install base utilities
RUN yum -y install -y wget
    
RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-ppc64le.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda

# Put conda in path so we can use conda activate
ENV PATH=$CONDA_DIR/bin:$PATH

RUN conda config --prepend channels rocketce
RUN conda config --append channels conda-forge
RUN conda install pytorch-cpu -c rocketce
RUN conda install gfortran -c conda-forge
RUN conda install openblas -c rocketce
