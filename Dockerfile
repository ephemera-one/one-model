FROM python:3.9

WORKDIR /app

# Installing Blender native dependencies
RUN apt-get update && apt-get install -y \
  libxxf86vm1 libxfixes3 libgl1 \
  && rm -rf /var/lib/apt/lists/*

# Installing python libraries
COPY requirements.txt ./
RUN pip install -r requirements.txt && rm requirements.txt

# COPY Blender build from ./env/
COPY ./env/lib/python3.9/site-packages/bpy.so /usr/local/lib/python3.9/site-packages
COPY ./env/lib/python3.9/site-packages/3.0 /usr/local/lib/python3.9/site-packages/3.0

# Installing sverchok
COPY install_sverchok ./install_sverchok
RUN cd install_sverchok && python install_sverchok.py && rm -rf /app/install_sverchok

COPY ./src /app/

CMD ["gunicorn", "--bind=0.0.0.0", "--workers=4", "--log-file=-", "--access-logfile=-", "one_model.wsgi"]

