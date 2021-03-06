import sys
import pandas as pd
import numpy as np
import itertools
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import AdaBoostClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.pipeline import make_pipeline

dataset = sys.argv[1]

# Read the data set into memory
input_data = pd.read_csv(dataset, compression='gzip', sep='\t')

for (learning_rate, n_estimators) in itertools.product([0.01, 0.1, 0.5, 1.0, 10.0, 50.0, 100.0],
                                                       [10, 50, 100, 500, 1000]):
    features = input_data.drop('class', axis=1).values.astype(float)
    labels = input_data['class'].values

    try:
        # Create the pipeline for the model
        clf = make_pipeline(StandardScaler(),
                            AdaBoostClassifier(learning_rate=learning_rate,
                                               n_estimators=n_estimators,
                                               random_state=324089))
        # 10-fold CV scores for the pipeline
        cv_scores = cross_val_score(estimator=clf, X=features, y=labels, cv=10)
    except KeyboardInterrupt:
        sys.exit(1)
    except:
        continue

    param_string = ''
    param_string += 'learning_rate={},'.format(learning_rate)
    param_string += 'n_estimators={}'.format(n_estimators)

    for cv_score in cv_scores:
        out_text = '\t'.join([dataset.split('/')[-1][:-7],
                              'AdaBoostClassifier',
                              param_string,
                              str(cv_score)])

        print(out_text)
        sys.stdout.flush()
