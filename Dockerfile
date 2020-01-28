FROM python:3.8 AS build
WORKDIR /src
COPY requirements.txt .
# install app dependencies
RUN pip install --user -r requirements.txt

FROM python:3.8 AS release
WORKDIR /src
COPY --from=build /root/.local /root/.local
# Copy all needed files to container's root directory
COPY delivery.py /
ADD /src /src
# Run app with this command.
CMD ["python", "/delivery.py", "--db_host", "mongodb"]
