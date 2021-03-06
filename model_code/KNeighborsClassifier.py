import sys
import pandas as pd
import numpy as np
import itertools
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.pipeline import make_pipeline
import itertools

dataset = sys.argv[1]

# Read the data set into memory
input_data = pd.read_csv(dataset, compression='gzip', sep='\t')

for (n_neighbors, weights) in itertools.product(list(range(1, 26)) + [50, 100],
                                                ['uniform', 'distance']):
    features = input_data.drop('class', axis=1).values.astype(float)
    labels = input_data['class'].values

    try:
        # Create the pipeline for the model
        clf = make_pipeline(StandardScaler(),
                            KNeighborsClassifier(n_neighbors=n_neighbors,
                                                 weights=weights))
        # 10-fold CV scores for the pipeline
        cv_scores = cross_val_score(estimator=clf, X=features, y=labels, cv=10)
    except KeyboardInterrupt:
        sys.exit(1)
    except:
        continue

    param_string = ''
    param_string += 'n_neighbors={},'.format(n_neighbors)
    param_string += 'weights={}'.format(weights)

    for cv_score in cv_scores:
        out_text = '\t'.join([dataset.split('/')[-1][:-7],
                              'KNeighborsClassifier',
                              param_string,
                              str(cv_score)])

        print(out_text)
        sys.stdout.flush()
