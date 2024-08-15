FROM python

# Set the working directory within the container
WORKDIR /api-flask

# Copy the necessary files and directories into the container
# COPY app.py requirements.txt /api-flask/
COPY app.py /api-flask

# Upgrade pip and install Python dependencies
#RUN pip3 install --upgrade pip
#RUN pip3 install -r requirements.txt

RUN conda install conda-forge::pymilvus

# Expose port 5000 for the Flask application
EXPOSE 5000

# Define the command to run the Flask application using Gunicorn
CMD ["gunicorn", "application:app", "-b", "0.0.0.0:5000", "-w", "4"]
