FROM daisukekobayashi/darknet:cpu

EXPOSE 3000

RUN apt-get update -y
RUN apt install -y python3.8 python3-pip
# RUN apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /home/app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

# DARKNET
# WORKDIR /home/darknet
# COPY darknet .
# RUN sed -i 's/OPENCV=0/OPENCV=1/' Makefile
# RUN sed -i 's/GPU=0/GPU=0/' Makefile
# RUN sed -i 's/CUDNN=0/CUDNN=0/' Makefile
# RUN sed -i 's/CUDNN_HALF=0/CUDNN_HALF=0/' Makefile
# RUN make

WORKDIR /home/app/app

COPY app .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]