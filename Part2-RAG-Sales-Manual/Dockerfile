FROM registry.fedoraproject.org/f33/python3

# Add application sources with correct permissions for OpenShift
USER 0
ADD app-src .
RUN chown -R 1001:0 ./
USER 1001

# Install the dependencies
RUN pip install -U "pip>=19.3.1" && \
    pip install -r requirements.txt && \
    python manage.py collectstatic --noinput && \
    python manage.py migrate

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
