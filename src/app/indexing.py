import re
from functools import reduce

import nltk
import spacy


class Preprocessor(object):
    """
    Cleans, removes stopwords and tokenizes lines
    """

    def __init__(self):
        # Stopwords
        nltk.download('stopwords', quiet=True, raise_on_error=True)
        # Sentence Tokenizer
        nltk.download('punkt', quiet=True, raise_on_error=True)

        self._tokenized_stop_words = nltk.word_tokenize(' '.join(nltk.corpus.stopwords.words('english')))
        self._stop_words = set(nltk.corpus.stopwords.words('english'))

        # Porter stemmer
        self.stemmer = nltk.stem.PorterStemmer()

        # spacy
        # python -m spacy download en_core_web_sm
        self.EN = spacy.load('en_core_web_sm')

    def stem_word(self, word):
        return self.stemmer.stem(word)

    def tokenize_string(self, line):
        tokens = nltk.word_tokenize(line)
        tokens = (self.stem_word(token) for token in tokens)
        tokens = [token for token in tokens if token.isalnum()]
        return list(tokens)

    @staticmethod
    def word_split(text):
        """
        Split a text in words. Returns a list of tuple that contains
        (word, location) location is the starting byte position of the word.
        """
        word_list = []
        w_current = []
        w_index = None

        for i, c in enumerate(text):
            if c.isalnum():
                w_current.append(c)
                w_index = i
            elif w_current:
                word = u''.join(w_current)
                word_list.append((w_index - len(word) + 1, word))
                w_current = []

        if w_current:
            word = u''.join(w_current)
            word_list.append((w_index - len(word) + 1, word))

        return word_list

    def words_cleanup(self, words):
        """
        Stems words and removes
        words with length less then a minimum and stopwords.
        """
        cleaned_words = []
        for index, word in words:

            if len(word) < 3 or word in self._stop_words or word in self._tokenized_stop_words or not str(
                    word).isalnum():
                continue
            word = self.stem_word(word)
            cleaned_words.append((index, word))
        return cleaned_words

    def word_index(self, text):
        """
        Just a helper method to process a text.
        It calls word split, normalize and cleanup.
        """
        words = self.word_split(text)
        words = self.words_cleanup(words)

        return words

    def remove_stopwords(self, text) -> str:
        '''this function will remove stopwords from text '''
        final_text = ''
        for word in text.split():
            if word not in self._stop_words:
                final_text += word + ' '
        return final_text

    def clean_str(self, text, stopwords=True) -> str:
        import re
        text = (text.encode('ascii', 'ignore')).decode("utf-8")
        text = re.sub("&.*?;", "", text)
        text = re.sub("[\]\|\[\@\,\$\%\*\&\\\(\)\":]", "", text)
        text = re.sub("-", " ", text)
        text = re.sub("\.+", "", text)
        text = re.sub("^\s+", "", text)
        text = re.sub("\.+", "", text)

        # text = re.sub("[_]{2,}", "", text)
        text = re.sub("[/]", " ", text)
        # text = re.sub("[0-9\n\t?!]", " ", text)
        text = re.sub("[ ]{2,}", "", text)

        text = text.lower()
        if stopwords:
            text = self.remove_stopwords(text)
        return text

    # ###########################################################################

    @staticmethod
    def to_lowercase(words):
        """Convert all characters to lowercase from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = word.lower()
            new_words.append(new_word)
        return new_words

    @staticmethod
    def remove_punctuation(words):
        """Remove punctuation from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = re.sub(r'[^\w\s]', '', word)
            if new_word != '':
                new_words.append(new_word)
        return new_words

    def remove_stopwords_2(self, words):
        """Remove stop words from list of tokenized words"""
        new_words = []
        for word in words:
            if word not in self._stop_words:
                new_words.append(word)
        return new_words

    def normalize(self, words, stopwords):
        words = self.to_lowercase(words)
        words = self.remove_punctuation(words)
        if stopwords:
            words = self.remove_stopwords_2(words)
        return words

    def tokenize_text(self, text):
        """Apply tokenization using spacy to docstrings."""
        tokens = self.EN.tokenizer(text)
        return [token.text.lower() for token in tokens if not token.is_space]

    def preprocess_text(self, text, stopwords=True) -> str:
        return ' '.join(self.normalize(self.tokenize_text(text), stopwords))


class Indexer(object):

    def __init__(self, preprocessor):
        self.preprocessor = preprocessor

    def inverted_index(self, text):
        """
        Create an Inverted-Index of the specified text document.
            {word:[locations]}
        """
        inverted = {}
        for index, word in self.preprocessor.word_index(text):
            locations = inverted.setdefault(word, [])
            locations.append(index)

        return inverted

    @staticmethod
    def inverted_index_add(inverted, doc_id, doc_index):
        """
        Add Inverted-Index doc_index of the document doc_id to the
        Multi-Document Inverted-Index (inverted),
        using doc_id as document identifier.
            {word:{doc_id:[locations]}}
        """
        for word, locations in doc_index.items():
            indices = inverted.setdefault(word, {})
            indices[doc_id] = locations
        return inverted

    def search(self, inverted, query):
        """
        Returns a set of documents id that contains all the words in your query.
        """
        words = [word for _, word in self.preprocessor.word_index(query) if word in inverted]
        results = [set(inverted[word].keys()) for word in words]
        return reduce(lambda x, y: x & y, results) if results else []
