import math
import os
import string

import nltk
import sys

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    # root directory
    root = os.path.join(os.getcwd(), directory)

    files = dict()

    for file in os.listdir(root):
        # read the content
        content = open(os.path.join(root, file), encoding="utf8").read()

        # add to the dictionary
        files[file] = content

    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # lower words
    list = nltk.word_tokenize(document.lower())

    # remove stop words and punctuation
    list = [word for word in list if word not in nltk.corpus.stopwords.words("english")
            and word not in string.punctuation]

    return list


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    word_count = dict()

    # iterate over documents
    for d in documents:

        existing_words=[]

        # iterate over words in each document
        for word in documents[d]:
            if word not in existing_words:
                existing_words.append(word)
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1

    # calculate the IDF for each word
    return {word: math.log(len(documents) / word_count[word]) for word in word_count}


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    ranking = dict()

    for file, words in files.items():

        sum = 0

        for word in query:
            sum += idfs[word] * words.count(word)

        ranking[file] = sum

    ranking = sorted(ranking.items(), key=lambda x: x[1], reverse=True)[:n]
    return [r[0] for r in ranking]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    ranking = list()

    for sentence in sentences:

        s = [sentence, 0, 0]

        for word in query:
            if word in sentences[sentence]:
                s[1] += idfs[word]
                s[2] += sentences[sentence].count(word) / len(sentences[sentence])

        ranking.append(s)

    return [sentence for sentence, sum, freq in
            sorted(ranking, key=lambda item: (item[1], item[2]), reverse=True)][:n]


if __name__ == "__main__":
    main()
