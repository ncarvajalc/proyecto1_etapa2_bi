import os
from joblib import load
from sklearn.base import BaseEstimator, TransformerMixin
import re, unicodedata
import contractions
import inflect
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer

class Normalizer(BaseEstimator,TransformerMixin):
    
    def init(self):
        pass
    
    def remove_non_ascii(self, words):
        """Remove non-ASCII characters from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
            new_words.append(new_word)
        return new_words

    def to_lowercase(self, words):
        new_words = []
        for word in words:
            if word != word.lower():
                new_words.append(word.lower())
            else:
                new_words.append(word)
        return new_words

    def remove_punctuation(self, words):
        """Remove punctuation from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = re.sub(r'[^\w\s]', '', word)
            if new_word != '':
                new_words.append(new_word)
        return new_words

    def replace_numbers(self, words):
        """Replace all interger occurrences in list of tokenized words with textual representation"""
        p = inflect.engine()
        new_words = []
        for word in words:
            if word.isdigit():
                new_word = p.number_to_words(word)
                new_words.append(new_word)
            else:
                new_words.append(word)
        return new_words

    def remove_stopwords(self, words):
        """Remove stop words from list of tokenized words"""
        sw = set(stopwords.words('english'))

        new_words = []
        for word in words:
            if word not in sw:
                new_words.append(word)
        return new_words
    

    def preprocessing(self, words):
        words = self.to_lowercase(words)
        words = self.replace_numbers(words)
        words = self.remove_punctuation(words)
        words = self.remove_non_ascii(words)
        words = self.remove_stopwords(words)
        return words
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X_copy = X.copy()  
        X_copy['study_and_condition'] = X_copy['study_and_condition'].apply(contractions.fix)
        X_copy['words'] = X_copy['study_and_condition'].apply(word_tokenize).apply(self.preprocessing)
        X_copy['label'].apply(lambda x: int(x[9]))
        return X_copy

class Lemmatizer(BaseEstimator,TransformerMixin):
    def init(self):
        pass
    
    def stem_words(self, words):
        """Stem words in list of tokenized words"""
        stemer = LancasterStemmer()
        stems = []

        for i in words:
            stems.append(stemer.stem(i))

        return stems

    def lemmatize_verbs(self, words):
        """Lemmatize verbs in list of tokenized words"""
        lemmatizer = WordNetLemmatizer()
        lemmas = []

        for i in words:
            lemmas.append(lemmatizer.lemmatize(i))

        return lemmas


    def stem_and_lemmatize(self, words):
        stems = self.stem_words(words)
        lemmas = self.lemmatize_verbs(words)
        return stems + lemmas
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X_copy = X.copy()        
        X_copy['words'] = X_copy['words'].apply(self.stem_and_lemmatize)
        X_copy['words'] = X_copy['words'].apply(lambda x: ' '.join(map(str, x)))
        return X_copy['words']

