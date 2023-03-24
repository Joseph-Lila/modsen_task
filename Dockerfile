# For testing
FROM python:3.10-alpine
WORKDIR /code
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
RUN python -m src.entrypoints.fastapi_app --drop_create_tables True --drop_create_indices True --init_with_csv True --init_elastic_with_db True --initial_csv_path assets/task/posts.csv
