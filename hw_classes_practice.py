from typing import List
import math


class CountVectorizer:
    """
    A class for converting a collection of text documents
    to a matrix of token counts.

    Attributes:
        vocab (dict): A dictionary that maps each unique word
        in the documents to an integer index.
        feature_names (list): A list of the unique words in the documents.
    """

    def __init__(self):
        """
        Initializes a CountVectorizer object with
        an empty vocabulary and feature_names list.
        """
        self.vocab = {}
        self.feature_names = []

    def fit_transform(self, documents: List[str]) -> List[List[int]]:
        """
        Fits the CountVectorizer object to the given collection
        of documents and returns a matrix of token counts.

        Args:
            documents (list): A list of strings representing
            the text documents.

        Returns:
            result (list): A list of lists representing
            the matrix of token counts for each document.
        """
        docs = []
        for doc in documents:
            words = doc.split()
            words = [word.lower() for word in words]
            docs.append(words)

        for doc in docs:
            for word in doc:
                if word not in self.vocab:
                    self.vocab[word] = len(self.vocab)
                    self.feature_names.append(word)
        result = []
        for doc in docs:
            vector = [0] * len(self.vocab)
            for word in doc:
                if word in self.vocab:
                    vector[self.vocab[word]] += 1
            result.append(vector)
        return result

    def get_feature_names(self):
        """
        Returns the list of unique words in the documents.

        Returns:
            feature_names (list): A list of the unique words in the documents.
        """
        return self.feature_names


def tf_transform(count_matrix: List[List[int]]) -> List[List[float]]:
    """
    Данная функция нормализует значения в count_matrix.

    Args:
        count_matrix (list): Матрица количества слов в каждом документе

    Returns:
        tf_matrix (list): Матрица частоты встречаемости
        каждого слова в документе.
    """
    tf_matrix = count_matrix.copy()
    for ind_doc, doc in enumerate(tf_matrix):
        length_doc = sum(doc)
        for ind_word, word in enumerate(doc):
            tf_matrix[ind_doc][ind_word] = word / length_doc
    return tf_matrix


def idf_transform(count_matrix: List[List[int]]) -> List[float]:
    """
    Calculate the Inverse Document Frequency (IDF)
    for each term in the count_matrix.

    Args:
    count_matrix (list): The count matrix where each row represents
    a document and each column represents a term.

    Returns:
    idf_matrix: A list containing the IDF value for each term
    in the count_matrix.
    """

    total_documents = len(count_matrix)
    idf_matrix = []

    for ind_word, word_count in enumerate(count_matrix[0]):
        all_count_word = sum([1 for ind_doc, doc in enumerate(count_matrix)
                              if count_matrix[ind_doc][ind_word] > 0])
        idf = math.log((total_documents + 1) / (all_count_word + 1)) + 1
        idf_matrix.append(idf)
    return idf_matrix


class TfidfTransformer(CountVectorizer):
    """
    A class for transforming a count matrix into a TF-IDF matrix.

    Args:
    CountVectorizer: The base class for transforming a collection
    of text documents into a matrix of token counts.

    Methods:
    fit_transform: Transform the count matrix into a TF-IDF matrix.
    """

    def fit_transform(self, raw_documents: List[List[str]]) \
            -> List[List[float]]:
        """
        Learn the vocabulary and idf from the count_matrix
        and return the TF-IDF matrix.

        Args:
        raw_documents (list): A list of strings
        where each string represents a document.

        Returns:
        tfidf_matrix (list): The TF-IDF matrix representing
        the input documents.
        """

        count_matrix = super().fit_transform(raw_documents)
        idf_matrix = idf_transform(count_matrix)
        tf_matrix = tf_transform(count_matrix)

        tfidf_matrix = tf_matrix.copy()

        for ind_doc, doc in enumerate(tf_matrix):
            for ind_word, word in enumerate(doc):
                tfidf_matrix[ind_doc][ind_word] = \
                    tf_matrix[ind_doc][ind_word] * idf_matrix[ind_word]
        return tfidf_matrix


class TfidfVectorizer:
    """
    A class for transforming a collection of text documents
    into a TF-IDF matrix.

    Args:
    None

    Methods:
    fit_transform: Transform the input documents into a TF-IDF matrix.
    """

    def __init__(self):
        self.transformer = TfidfTransformer()

    def fit_transform(self, raw_documents: List[List[str]]) \
            -> List[List[float]]:
        """
        Transform the input documents into a TF-IDF matrix.

        Args:
        raw_documents (list): A list of strings where each
        string represents a document.

        Returns:
        np.array: The TF-IDF matrix representing the input documents.
        """
        return self.transformer.fit_transform(raw_documents)

    def get_feature_names(self):
        """
        Get the feature names from the CountVectorizer.

        Returns:
        list: The feature names extracted from the CountVectorizer.
        """

        return self.transformer.get_feature_names()


if __name__ == '__main__':
    corpus = ['Crock Pot Pasta Never boil pasta again',
              'Pasta Pomodoro Fresh ingredients Parmesan to taste']

    vectorizer = CountVectorizer()
    count_matrix = vectorizer.fit_transform(corpus)
    true_count_matrix = [[1, 1, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                         [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1]]
    print(count_matrix)

    tf_matrix = tf_transform(count_matrix)
    print(tf_matrix)

    idf_matrix = idf_transform(count_matrix)
    print(idf_matrix)

    transformer = TfidfTransformer()
    tfidf_matrix = transformer.fit_transform(corpus)
    print(tfidf_matrix)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    print(vectorizer.get_feature_names())
    print(tfidf_matrix)
