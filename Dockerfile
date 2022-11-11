# For more information, please refer to https://aka.ms/vscode-docker-python
FROM continuumio/miniconda3

EXPOSE 8501

WORKDIR /app

# Create the environment:
COPY env.yml .
RUN conda env create -f env.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "finance_app", "/bin/bash", "-c"]

# Demonstrate the environment is activated:
RUN echo "Make sure streamlit is installed:"
RUN python -c "import streamlit"

# WORKDIR /app
# COPY . /app

# # During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["gunicorn", "--bind", "0.0.0.0:8501", "-k", "uvicorn.workers.UvicornWorker", "app.1_🤑_main_page:app"]
