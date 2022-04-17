FROM chungil987/python
WORKDIR /usr/src/app
COPY . .
ENTRYPOINT ["python3", "main.py"]
CMD ["token"]