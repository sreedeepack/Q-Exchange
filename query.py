#!/usr/bin/env python3
import time
from functools import reduce

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from build import BuildModel


class Query:

    def __init__(self, file="crawlers/stack/data/solr.jsonl"):
        self.model = BuildModel(file)
        self.model.build()
        self.df = pd.DataFrame(self.model.document_generator(file, type="document"))

    def search_index(self, query):
        """
        Returns a set of documents id that contains all the words in your query.
        """
        inverted = self.model.index
        preprocessor = self.model.preprocessor
        words = [word for _, word in preprocessor.word_index(query) if word in inverted]
        results = [set(inverted[word].keys()) for word in words]
        return reduce(lambda x, y: x & y, results) if results else []

    def search(self, query, top_n):
        """
        Search top n results for given query
        """
        start = time.time()
        preprocessor = self.model.preprocessor
        dictionary = self.model.dictionary

        # same as size given in Word2Vec in build.py
        main_vec = np.zeros(100)
        # initialize tfidf weight
        weight_sum = 0

        # preprocess question
        text = preprocessor.clean_str(query)
        text_list = list(text.split())

        for word in text_list:
            if word in self.model.tfidf_words and word in self.model.w2v_words:
                vect = self.model.w2v_model[word]
                # compute tfidf
                tf_idf = dictionary[word] * (text_list.count(word) / len(text_list))
                main_vec += (vect * tf_idf)
                weight_sum += tf_idf

        if weight_sum != 0:
            main_vec /= weight_sum

        # find cosine similarity
        similarities = cosine_similarity(main_vec.reshape(1, -1), Y=self.model.tfidf_w2v_vectors_gensim,
                                         dense_output=True)
        # sort similarities
        sort = np.argsort(similarities[0])
        # sort indices in descending order
        similarity_index = np.array(list(reversed(sort)))
        # find top n similar
        top_similarity_index = similarity_index[:top_n]

        print(f'Top{top_n} cosine similarities are \t', similarities[0][top_similarity_index])

        results = self.df[['title', 'url']][top_similarity_index]

        total_time = (time.time() - start)
        print(f'Time taken = {total_time} ms')
        return results


if __name__ == "__main__":
    q = Query("crawlers/stack/data/solr.jsonl")
    inp = ""
    while True:
        inp = input("Enter query...or type 'exit':\n")
        if inp == "exit":
            exit(0)
        result = q.search(inp, 10)
        print(result)
