import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def recommend(isbn, df, n):
    """
    Recommend a number of titles based on the chosen ISBN.
    This function may behave strangely if n is too high.
    :param isbn: ISBN-13 of the chosen book
    :param df: the variable storing clustered_df.csv
    :param n: number of books to recommend
    :return: List of indices, of the recommended books.
    """
    # Get the indices of the book and its cluster
    isbn_ind = isbnToIndx(isbn, df)
    # Cluster matches are all books in the same cluster as the target book
    cluster_matches = matchCluster(isbn_ind, df)
    # Compute cosine similarities of all books in the cluster to the target book
    similarities = computeSims(isbn_ind, cluster_matches, df)
    # Get the top n indices based on the cosine similarities
    rec_inds = getTopInds(similarities, cluster_matches, n)
    print("rec_inds", rec_inds)
    return rec_inds

# Helper functions

def isbnToIndx(isbn, df):
    """
    Assumes the DataFrame has a column "isbn13".
    :param isbn: the ISBN-13 of the book
    :param df: clustered_df.csv
    :return: the index of the book in the DataFrame
    """
    return df.index[df['isbn13'] == isbn].tolist()[0]

def matchCluster(indx, df):
    """
    Assumes the DataFrame has columns "isbn13" & "cluster"
    :param indx: the index of the book
    :param df: clustered_df.csv
    :return: the indices of the other books in the cluster
    """
    # Find the target cluster
    target_cluster = df.loc[indx, 'cluster']
    return df.index[df['cluster'] == target_cluster].tolist()

def computeSims(isbn_ind, cluster_matches, df):
    """
    Computes the cosine similarity of all books in the cluster to the target book.
    :param isbn_ind: the index of the book
    :param cluster_matches: all books in the cluster
    :param df: clustered_df.csv
    :return: unsorted cosine similarities of all books to the target
    """
    feature_matrix = (df.drop(['isbn13', 'title_x', 'author(s)_x', 'publication_date_x', 'cluster'], axis=1)).to_numpy()
    target_vec = feature_matrix[isbn_ind].reshape(1, -1)
    cluster_vecs = feature_matrix[cluster_matches]
    similarities = cosine_similarity(target_vec, cluster_vecs)[0]
    return similarities

def getTopInds(similarities, cluster_matches, n):
    """
    Gets the top n indices based on the cosine similarities.
    :param similarities: nsorted cosine similarities of all books to the target
    :param cluster_matches: all books in the cluster
    :param n: number of matches to return; n being too high may cause strange behaviors
    :return: order of indices that would sort the similarities in descending order
    """
    # Sort similarities from highest to lowest
    sorted_local_idxs = np.argsort(similarities)[::-1]  # e.g. [self, most similar, ... ]

    # The first index in sorted_local_idxs should correspond to the target book itself
    # (similarity 1). Skip it and take the next n.
    top_local_idxs = sorted_local_idxs[1:n+1]

    # Map local cluster positions back to dataframe indices
    rec_inds = [cluster_matches[i] for i in top_local_idxs]

    return rec_inds