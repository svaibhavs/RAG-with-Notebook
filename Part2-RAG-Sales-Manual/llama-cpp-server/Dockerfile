FROM registry.access.redhat.com/ubi9:9.4-1214.1726694543 AS env-build

# WORKDIR /srv

# ARG MODEL_DOWNLOAD_URL
# ARG MODEL_FILENAME

RUN dnf -y install gcc-toolset-13 && \
    source /opt/rh/gcc-toolset-13/enable

# Set LLAMA.CPP SHA for git pull
# ARG LLAMA_CPP_SHA=1329c0a75e6a7defc5c380eaf80d8e0f66d7da78
# RUN dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm && \
#    crb enable && \
#    dnf install -y epel-release && \
#    dnf --enablerepo=ubi-9-appstream-rpms install -y git procps-ng vim \
#      dnf-plugins-core python3-dnf-plugin-versionlock cmake gcc-c++
#     dnf-plugins-core python3-dnf-plugin-versionlock cmake gcc-c++ \
#     python3-pip python3-argcomplete && \
#    dnf copr enable -y slp/mesa-krunkit epel-9-$(uname -m) && \
#    dnf install -y mesa-vulkan-drivers-23.3.3-102.el9 \
#      vulkan-headers vulkan-loader-devel vulkan-tools spirv-tools glslc && \
#    dnf clean all && \
#    rm -rf /var/cache/*dnf*

# install build tools and clone and compile llama.cpp
RUN dnf -y update && dnf install -y git cmake make automake gcc gcc-c++ llvm-toolset wget
    
RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-ppc64le.sh -O ~/conda.sh && \
    /bin/bash ~/conda.sh -b -p /opt/conda

# Put conda in path so we can use conda activate
ENV PATH /opt/conda/bin:$PATH

RUN conda config --prepend channels rocketce && \
    conda config --append channels conda-forge && \
    conda install -y pytorch-cpu -c rocketce && \
    conda install -y gfortran -c conda-forge && \
    conda install -y openblas -c rocketce

RUN git clone --recursive https://github.com/ggerganov/llama.cpp && \
    cd llama.cpp && \
#    git reset --hard ${LLAMA_CPP_SHA} && \
#    cmake -B build -DCMAKE_INSTALL_PREFIX:PATH=/usr && \
    cmake -B build -DGGML_BLAS=ON -DGGML_BLAS_VENDOR=OpenBLAS && \
    cmake --build build --config Release -j $(nproc) && \
    cmake --install build && \
    cd / && \
    rm -rf llama.cpp
