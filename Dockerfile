FROM tensorflow/tensorflow

WORKDIR /project

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

EXPOSE 5000

COPY . /project

RUN chmod +x ./run.sh

ENTRYPOINT ["/bin/bash", "./run.sh"]