FROM python
WORKDIR /usr/src/app
COPY . .
RUN apt-get update
RUN apt-get install -y ffmpeg
RUN pip install -r /usr/src/app/requirements.txt
ENTRYPOINT ["python3", "main.py"]
CMD ["token"]