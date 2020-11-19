FROM python:3.8.6


RUN apt-get update && apt-get -y install apt-utils\
    && apt-get install --no-install-recommends --no-install-suggests -y curl \
    && apt-get -y install wget

WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#WORKDIR /usr/src/app/src/app

RUN pip install gdown \
    && gdown "https://drive.google.com/uc?id=13HMs8dE9N3eDrYksNz07iAlNQuKIZi8z" -O tag_predictor.h5 \
    && echo "tag predictor model downloaded"

RUN gdown "https://drive.google.com/uc?id=1LM7LzDj59v70rb-qLSvRX7ykInEfZnC7" -O word2vec.model \
    && echo "word2vec model downloaded"

RUN gdown "https://drive.google.com/uc?id=1RBG-lyjK6Qt9uoSJOLuKxOfQRRTnTWpc" -O tfidf.pkl \
    && echo "tfidf model downloaded"

RUN gdown "https://drive.google.com/uc?id=1qz0c_4QCR2alo60kHh-jv1TpcP2JW5NT" -O tokenizer.pickle \
    && echo "tokenizer model downloaded"

# WORKDIR /usr/src/app/crawlers/stack/data
RUN gdown "https://drive.google.com/uc?id=1T2U1xeRUj0ArqanO0CNi9wJ9fuoPY6YB" -O data.jsonl \
    && echo "data downloaded"

RUN python -m spacy download en_core_web_sm
EXPOSE 5000
#CMD ["gunicorn", "-w", "2" , "-b", "0.0.0.0:5000", "app:app"]
