# FROM registry.access.redhat.com/ubi9 AS builder
FROM registry.access.redhat.com/ubi9

# ARG MODEL_DOWNLOAD_URL
# ARG MODEL_FILENAME

RUN dnf -y install gcc-toolset-13 && \
    source /opt/rh/gcc-toolset-13/enable

# install build tools and clone and compile llama.cpp
RUN dnf -y update && dnf install -y git cmake automake gcc gcc-c++ llvm-toolset wget
    
RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-ppc64le.sh -O ~/conda.sh && \
    /bin/bash ~/conda.sh -b -p /opt/conda

# Put conda in path so we can use conda activate
ENV PATH /opt/conda/bin:$PATH

RUN conda update -n base -c defaults conda && \
    conda config --prepend channels rocketce && \
    conda config --append channels conda-forge && \
    conda install -y pytorch-cpu==2.0.1 -c rocketce && \
    conda install -y gfortran==11.2.0 -c conda-forge && \
    conda install -y openblas -c rocketce 
    
ENV PKG_CONFIG_PATH=/opt/conda/lib/pkgconfig:$PKG_CONFIG_PATH
ENV LD_LIBRARY_PATH /opt/conda/lib:$LD_LIBRARY_PATH

RUN git clone --recursive https://github.com/ggerganov/llama.cpp && \
    cd llama.cpp && \
# Using cmake breaks for me, so forcing the basic make instead
    make LLAMA_OPENBLAS=1 LLAMA_MAKEFILE=1
    
CMD bash
########################################################
# Copying the built executable and libraries needed for the runtime on a simple ubi9 so it is a small container
########################################################
#FROM registry.access.redhat.com/ubi9/ubi

#COPY --from=builder --chmod=755 /llama.cpp/build/bin/llama-server /usr/local/bin
#COPY --from=builder --chmod=644 /llama.cpp/build/src/libllama.so /llama.cpp/build/src/libllama.so
#COPY --from=builder --chmod=644 /llama.cpp/build/ggml/src/libggml.so /llama.cpp/build/ggml/src/libggml.so

#ENTRYPOINT [ "/usr/local/bin/llama-server", "--host", "0.0.0.0"]
