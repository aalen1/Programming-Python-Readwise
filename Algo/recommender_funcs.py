##################################################################################
# This file contains functions used for the recommendation system.
##################################################################################

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def recommend(isbn, df, n):
    """
    Recommend a number of titles based on the chosen ISBN.
    This function may behave strangely if n is too high.

    Args:
        isbn (int): ISBN-13 of the chosen book
        df (DataFrame): the variable storing clustered_df.csv
        n (int): number of books to recommend

    Returns:
        rec_list (List of ints): List of indices of the recommended books.
    """

    isbn_ind = isbnToIndx(isbn, df)
    cluster_matches = matchCluster(isbn_ind, df)
    similarities = computeSims(isbn_ind, cluster_matches, df)
    rec_inds = getTopInds(similarities, cluster_matches, n)

    return rec_inds

# HELPERS vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv    

def isbnToIndx(isbn, df):
    """
    Assumes the DataFrame has a column "isbn13".
    Args:
        isbn (int): the ISBN-13 of the book
        df (DataFrame): clustered_df.csv
    Returns:
        indx (int): the index of the book in the DataFrame      
    """
    return df.index[df['isbn13'] == isbn].tolist()[0]

def matchCluster(indx, df):  
    """
    Assumes the DataFrame has columns "isbn13" & "cluster"
    Args:
        indx (int): the index of the book
        df (DataFrame): clustered_df.csv
    Returns:
        cluster (List): the indices of the other books in the cluster
    """
    target_cluster = df.loc[indx, 'cluster'] # find cluster of target isbn
    return df.index[df['cluster'] == target_cluster].tolist()

def computeSims(isbn_ind, cluster_matches, df):
    """
    Args:
        isbn_ind (int): the index of the book
        cluster_matches (List of ints): all books in the cluster
        df (DataFrame): clustered_df.csv
    Returns:
        similarities (ndarray): unsorted cosine similarities of all books to the target
    """
    feature_matrix = (df.drop(['isbn13', 'title_x', 'author(s)_x', 'publication_date_x', 'cluster'], axis=1)).to_numpy()
    target_vec = feature_matrix[isbn_ind].reshape(1, -1)
    cluster_vecs = feature_matrix[cluster_matches]
    similarities = cosine_similarity(target_vec, cluster_vecs)[0]
    return similarities

def getTopInds(similarities, cluster_matches, n):
    """
    Args:
        similarities (ndarray): unsorted cosine similarities of all books to the target
        cluster_matches (List of ints): all books in the cluster
        n (int): number of matches to return; n being too high may cause strange behaviors
    Returns:
        top_n (List of indices): order of indices that would sort the similarities in descending order
    """
    sorted_inds = np.argsort(similarities)[(-1)*n+1:-1] # cutting out last index as it will always be 1
    rec_inds = [cluster_matches[i] for i in sorted_inds]
    top_n = rec_inds.reverse()
    return top_n