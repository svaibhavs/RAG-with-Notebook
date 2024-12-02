FROM registry.access.redhat.com/ubi9:9.4-1214.1726694543 AS env-build

# WORKDIR /srv

# ARG MODEL_DOWNLOAD_URL
# ARG MODEL_FILENAME

RUN dnf -y install gcc-toolset-13 && \
    source /opt/rh/gcc-toolset-13/enable

# install build tools and clone and compile llama.cpp
RUN dnf -y update && dnf install -y git cmake make automake gcc gcc-c++ llvm-toolset wget
    
RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-ppc64le.sh -O ~/conda.sh && \
    /bin/bash ~/conda.sh -b -p /opt/conda

# Put conda in path so we can use conda activate
ENV PATH /opt/conda/bin:/anaconda3/bin:/anaconda3/condabin:$PATH

RUN conda config --prepend channels rocketce && \
    conda config --append channels conda-forge && \
    conda install -y pytorch-cpu==2.0.1 -c rocketce && \
    conda install -y gfortran==11.2.0 -c conda-forge && \
    conda install -y openblas -c rocketce 
    
ENV PKG_CONFIG_PATH=$HOME/anaconda3/lib/pkgconfig:$PKG_CONFIG_PATH
ENV LD_LIBRARY_PATH $HOME/anaconda3/lib:$LD_LIBRARY_PATH

RUN echo $PATH && \
    echo $PKG_CONFIG_PATH && \
    echo $LD_LIBRARY_PATH && \
    git clone --recursive https://github.com/ggerganov/llama.cpp && \
    cd llama.cpp && \
    make LLAMA_OPENBLAS=1
#    git reset --hard ${LLAMA_CPP_SHA} && \
#    cmake -B build -DCMAKE_INSTALL_PREFIX:PATH=/usr && \
#    cmake -B build -LLAMA_OPENBLAS=1 && \
#    cmake --build build --config Release -j $(nproc) && \
#    cmake --install build && \
#    cd / && \
#    rm -rf llama.cpp
