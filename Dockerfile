FROM python
WORKDIR /usr/src/app
COPY . .
RUN pip install -r /usr/src/app/requirements.txt
CMD ["main.py"]
ENTRYPOINT ["python3"]