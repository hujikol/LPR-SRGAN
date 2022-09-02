FROM python:3.8

EXPOSE 3000

RUN apt-get update \
    && apt-get install -y \
        wget \
        build-essential \ 
        cmake \
        pkg-config \
        python-dev \ 
        python-opencv \ 
        libopencv-dev \       
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/app

COPY requirements.txt .
RUN pip install -r requirements.txt

# DARKNET
WORKDIR /home/darknet
COPY darknet .
RUN sed -i 's/OPENCV=0/OPENCV=1/' Makefile
RUN sed -i 's/GPU=0/GPU=0/' Makefile
RUN sed -i 's/CUDNN=0/CUDNN=0/' Makefile
RUN sed -i 's/CUDNN_HALF=0/CUDNN_HALF=0/' Makefile
RUN make

WORKDIR /home/app/app

COPY app .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]