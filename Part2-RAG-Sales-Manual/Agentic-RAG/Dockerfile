FROM registry.access.redhat.com/ubi8/python-311

# Set the working directory within the container
WORKDIR /app

RUN chmod +w /

# Copy the necessary files and directories into the container
#COPY app.py /app/

# Upgrade pip and install Python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install pymilvus sentence-transformers llama-cpp-python --extra-index-url https://repo.fury.io/mgiessing --prefer-binary
RUN pip3 install -U langchain
RUN pip3 install -U langchain-community
RUN pip3 install -U jupyter

# Expose port 8888 for the notebook application
EXPOSE 8888

# Run Jupyter Notebook when the container launches
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--user root"]
