FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN echo "#!/usr/bin/env bash" > start.sh
RUN echo "sleep 40" >> start.sh
RUN echo "python ./app.py" >> start.sh
RUN chmod +x start.sh

CMD [ "./start.sh" ]
