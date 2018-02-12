import pandas as pd
import numpy as np
from src.com.fwk.business.util.logging import comlogging
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from gensim.models import word2vec

import matplotlib.pyplot as plt
import seaborn as sns

def measurePCA() :
    # Eating, exercise habbit and their body shape
    df = pd.DataFrame(columns=['calory', 'breakfast', 'lunch', 'dinner', 'exercise', 'body_shape'])
    df.loc[0] = [1200, 1, 0, 0, 2, 'Skinny']
    df.loc[1] = [2800, 1, 1, 1, 1, 'Normal']
    df.loc[2] = [3500, 2, 2, 1, 0, 'Fat']
    df.loc[3] = [1400, 0, 1, 0, 3, 'Skinny']
    df.loc[4] = [5000, 2, 2, 2, 0, 'Fat']
    df.loc[5] = [1300, 0, 0, 1, 2, 'Skinny']
    df.loc[6] = [3000, 1, 0, 1, 1, 'Normal']
    df.loc[7] = [4000, 2, 2, 2, 0, 'Fat']
    df.loc[8] = [2600, 0, 2, 0, 0, 'Normal']
    df.loc[9] = [3000, 1, 2, 1, 1, 'Fat']

    print(df.head())

    # Split feature vectors and labels
    # X is feature vectors
    X = df[['calory', 'breakfast', 'lunch', 'dinner', 'exercise']]
    print(X.head(9))

    Y = df[['body_shape']]
    print(Y.head(10))

    # 3. rescaling feature vectors to all have the same scale
    x_std = StandardScaler().fit_transform(X)
    print(x_std)

    # features are columns from x_std
    features = x_std.T
    covariance_matrix = np.cov(features)
    print(covariance_matrix)

    # Eigen Vectors and Eigen Values from Covariance Matrix
    eig_vals, eig_vecs = np.linalg.eig(covariance_matrix)

    eig_vals[0] / sum(eig_vals)
    projected_X = x_std.dot(eig_vecs.T[0])
    result = pd.DataFrame(projected_X, columns=['PC1'])
    result['y-axis'] = 0.0
    result['label'] = Y

    sns.lmplot('PC1', 'y-axis', data=result, fit_reg=False,  # x-axis, y-axis, data, no line
               scatter_kws={"s": 50}, # marker size
               hue="label") # color

    # title
    plt.title('PCA result')
    plt.show()


def mesureKMEAN():
    df = pd.DataFrame(columns=['x', 'y'])

    df.loc[0] = [3, 1]
    df.loc[1] = [4, 1]
    df.loc[2] = [3, 2]
    df.loc[3] = [4, 2]
    df.loc[4] = [10, 5]
    df.loc[5] = [10, 6]
    df.loc[6] = [11, 5]
    df.loc[7] = [11, 6]
    df.loc[8] = [15, 1]
    df.loc[9] = [15, 2]
    df.loc[10] = [16, 1]
    df.loc[11] = [16, 2]

    print(df.head(20))

    # visualize data point
    sns.lmplot('x', 'y', data=df, fit_reg=False, scatter_kws={"s": 200})  # x-axis, y-axis, data, no line, marker size

    # title
    plt.title('kmean plot')

    # x-axis label
    plt.xlabel('x')

    # y-axis label
    plt.ylabel('y')
    plt.show()

    # convert dataframe to numpy array
    data_points = df.values
    kmeans = KMeans(n_clusters=3).fit(data_points)
    print( kmeans.labels_)
    print(kmeans.cluster_centers_)

    df['cluster_id'] = kmeans.labels_
    print(df.head(12))

    sns.lmplot('x', 'y', data=df, fit_reg=False,  # x-axis, y-axis, data, no line
              scatter_kws={"s": 150},  # marker size
              hue="cluster_id")  # color

    # title
    plt.title('after kmean clustering')
    plt.show()


