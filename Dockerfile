FROM python:3.9-alpine

WORKDIR /app

COPY password_gen.py .
COPY create_common_passwords.py .

RUN python create_common_passwords.py && \
    chmod +x password_gen.py

ENTRYPOINT ["python", "password_gen.py"]