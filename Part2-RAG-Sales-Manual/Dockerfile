FROM registry.fedoraproject.org/f33/python3:3.11

# Add application sources to a directory that the assemble script expects them
# and set permissions so that the container runs without root access
USER 0
ADD app-src /tmp/src
RUN /usr/bin/fix-permissions /tmp/src
USER 1001

# Install the dependencies
RUN /usr/libexec/s2i/assemble

# Set the default command for the resulting image
CMD /usr/libexec/s2i/run

# Set the working directory within the container
WORKDIR /api-flask

# Copy the necessary files and directories into the container
COPY app.py requirements.txt /api-flask/

# Upgrade pip and install Python dependencies
#RUN pip3 install --upgrade pip
RUN pip3 install pymilvus --extra-index-url https://repo.fury.io/mgiessing --prefer-binary
RUN pip3 install -r requirements.txt
# Expose port 5000 for the Flask application
EXPOSE 5000

# Define the command to run the Flask application using Gunicorn
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000", "-w", "4"]
