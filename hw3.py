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

    def fit_transform(self, documents):
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
        for doc in documents:
            words = doc.split()
            words = [word.lower() for word in words]
            for word in words:
                if word not in self.vocab:
                    self.vocab[word] = len(self.vocab)
                    self.feature_names.append(word)
        result = []
        for doc in documents:
            vector = [0] * len(self.vocab)
            words = doc.split()
            words = [word.lower() for word in words]
            for word in words:
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


if __name__ == '__main__':
    pass
