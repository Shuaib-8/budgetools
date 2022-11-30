# Official python 3.10 image
FROM python:3.10-slim

# Expose default port for streamlit
EXPOSE 8501

# Set/add 'app' folder as the root of the directory
WORKDIR /app

# Install git to do install codebase remotely
RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Clone the relevant repo
RUN git clone https://github.com/Shuaib-8/budgetools.git . 

# Install requirements consequently
# ~~~~~~~~~~~~~~~~~~ local install notes ~~~~~~~~~~~~~~~~~~~~
# Copy requirements from repo to image file system and then install i.e.:
# COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

# Copying all code/actions to image file system
COPY . . 

# Run app and confiure URL destination
ENTRYPOINT ["streamlit", "run", "app/1_🤑_main_page.py", "--server.port=8501", "--server.address=0.0.0.0"]
