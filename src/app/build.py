#!/usr/bin/env python3
import os
import pickle

import jsonlines
import numpy as np
import pandas as pd
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from tqdm import tqdm

from indexing import Indexer
from indexing import Preprocessor


class BuildModel(object):

    def __init__(self, file="../../crawlers/stack/data/solr.jsonl"):
        # input jsonlines file
        self.file = file
        # inverted index
        self.index = {}
        self.tfidf_words = {}
        self.dictionary = {}
        self.doc_ids = {}

        self.preprocessor = Preprocessor()
        # the weighted w2v for each sentence is stored in this list
        self.tfidf_w2v_vectors_gensim = []

        self.w2v_words = None
        self.w2v_model = None
        self.data = None

    def document_generator(self, file, type="document"):
        preprocessor = self.preprocessor
        use_stopwords = True
        if type == "string":
            use_stopwords = False

        with jsonlines.open(file) as reader:
            for doc_id, obj in enumerate(reader):
                item = {
                    'doc_id': doc_id,
                    'url': obj['url'],
                    'title': obj['title'],
                    'processed_title': preprocessor.preprocess_text(obj['title'], use_stopwords),
                    'body': preprocessor.preprocess_text(obj['desc'], use_stopwords),
                    'votes': obj['votes'],
                    'date': obj['date'],
                    'answers': obj['answers'],
                    'src': obj['src'],
                    'tags': ", ".join(obj['tags']),
                }
                if type == "document":
                    yield item
                elif type == "word_list":
                    yield (item['processed_title'] + " " + item['body']).split(" ")
                elif type == "string":
                    yield item['processed_title'] + " " + item['body']

    # fullIndex
    def get_index(self):
        inverted = {}
        indexer = Indexer(Preprocessor())

        for doc in self.document_generator(self.file):
            doc_id = doc['doc_id']
            # index both title and description
            text = doc['title'] + " " + doc['body']
            # self.doc_map[doc_id] = (doc['url'], text)
            self.doc_ids[doc_id] = doc['url']
            doc_index = indexer.inverted_index(text)
            indexer.inverted_index_add(inverted, doc_id=doc_id, doc_index=doc_index)

        return inverted

    def get_tfidf(self):
        tfidf = TfidfVectorizer(min_df=10)
        # fit and transform on file content
        tfidf.fit_transform(self.document_generator(self.file, type="string"))
        # get tfidf words
        self.tfidf_words = set(tfidf.get_feature_names())
        # dictionary of tfidf
        self.dictionary = dict(zip(tfidf.get_feature_names(), list(tfidf.idf_)))

    def gensim_vec(self):
        print("Generating word2vec model...")

        # sentences = list(self.document_generator(self.file, type="word_list"))
        data = pd.DataFrame(self.document_generator(self.file, type="document"))
        data["text"] = data['title'] + " " + data['body']
        sentences = [_text.split() for _text in np.array(data.text)]
        if os.path.exists("word2vec.model"):
            w2v_model = Word2Vec.load("word2vec.model")
        else:

            w2v_model = Word2Vec(size=300, window=7, min_count=10, workers=-1)
            # w2v_model = Word2Vec(sentences=sentences, size=300, window=7, min_count=10, workers=-1)

            # Train Word Embeddings
            w2v_model.train(sentences, total_examples=len(sentences), epochs=32)
            # w2v_model.train(sentences, total_examples=len(sentences), epochs=32)
            w2v_model.save("word2vec.model")

        self.w2v_words = list(w2v_model.wv.vocab)
        self.w2v_model = w2v_model
        # get tfidf words and dictionary
        self.get_tfidf()

        print("Generating tfidf...")
        if os.path.exists("tfidf.pkl"):
            pkl_file = open("tfidf.pkl", "rb")
            self.tfidf_w2v_vectors_gensim = pickle.load(pkl_file)
        else:
            for sentence in tqdm(sentences):
                vector = np.zeros(300)  # as word vectors size is 300
                # num of words with a valid vector in the sentence
                tf_idf_weight = 0
                for word in sentence:
                    if (word in self.w2v_words) and (word in self.tfidf_words):
                        # getting the vector for each word
                        vec = w2v_model.wv[word]

                        # multiply idf value of word with tf of word
                        tf_idf = self.dictionary[word] * (sentence.count(word) / len(sentence))
                        vector += (vec * tf_idf)
                        # calculating tfidf weighted w2v
                        tf_idf_weight += tf_idf
                if tf_idf_weight != 0:
                    vector /= tf_idf_weight
                self.tfidf_w2v_vectors_gensim.append(vector)

            # Store
            pkl_file = open("tfidf.pkl", "wb")
            pickle.dump(self.tfidf_w2v_vectors_gensim, pkl_file)

        pkl_file.close()
        self.data = data

    def tag_encoder(self):
        self.data.tags = self.data.tags.apply(lambda x: x.split('|'))
        tag_freq_dict = {}
        for tags in self.data.tags:
            for tag in tags:
                if tag not in tag_freq_dict:
                    tag_freq_dict[tag] = 0
                else:
                    tag_freq_dict[tag] += 1

        tags_to_use = 500
        tag_freq_dict_sorted = dict(sorted(tag_freq_dict.items(), key=lambda x: x[1], reverse=True))
        final_tags = list(tag_freq_dict_sorted.keys())[:tags_to_use]

        final_tag_data = []
        for tags in self.data.tags:
            temp = []
            for tag in tags:
                if tag in final_tags:
                    temp.append(tag)
            final_tag_data.append(temp)

        tag_encoder = MultiLabelBinarizer()
        tags_encoded = tag_encoder.fit_transform(final_tag_data)
        return tag_encoder

    def build(self):

        # self.index = self.get_index()
        self.gensim_vec()
