
"""
Adaptation of the code found in the following site to Relion model star file training
https://ahmedbesbes.com/how-to-score-08134-in-titanic-kaggle-challenge.html
"""

import warnings
warnings.filterwarnings('ignore')
warnings.filterwarnings('ignore', category=DeprecationWarning)

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble.gradient_boosting import GradientBoostingClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.preprocessing import normalize

def status(feature):
    print ('Processing', feature, ': ok')

def compute_score(clf, X, y, scoring='accuracy'):
    xval = cross_val_score(clf, X, y, cv = 5, scoring=scoring)
    return np.mean(xval)

def recover_train_test_target():
    global combined

    targets = pd.read_csv('./data/starfiles/train.csv', usecols=['Selection'])[
        'Selection'].values

    train = pd.read_csv('data/starfiles/train.csv')
    train = train.drop(columns=['Class','Selection'])
    train = train/train.max(axis=0) # normailize?

    test = pd.read_csv('data/starfiles/test.csv')
    test = test.drop(columns=['Class','Selection'])
    test = test/test.max(axis=0) # normalize?

    print ('train and text normalized')
    print(train)
    print(test)
    return train, test, targets


train, test, targets = recover_train_test_target()
clf = RandomForestClassifier(n_estimators=50, max_features='sqrt')
clf = clf.fit(train, targets)
print ('Fitted Classifiers')
print (clf)

features = pd.DataFrame()
features['feature'] = train.columns
features['importance'] = clf.feature_importances_
features.sort_values(by=['importance'], ascending=True, inplace=True)
features.set_index('feature', inplace=True)
print ('Features')
print (features)

model = SelectFromModel(clf, prefit=True)
train_reduced = model.transform(train)
test_reduced = model.transform(test)

logreg = LogisticRegression()
logreg_cv = LogisticRegressionCV()
rf = RandomForestClassifier()
gboost = GradientBoostingClassifier()

models = [logreg, logreg_cv, rf, gboost]
for model in models:
    print ('Cross-validation of : {0}'.format(model.__class__))
    score = compute_score(clf=model, X=train_reduced, y=targets, scoring='accuracy')
    print ('CV score = {0}'.format(score))
    print ('****')


# turn run_gs to True if you want to run the gridsearch again.
run_gs = False

if run_gs:
    parameter_grid = {
        'max_depth': [4, 6, 8],
        'n_estimators': [50, 10],
        'max_features': ['sqrt', 'auto', 'log2'],
        'min_samples_split': [2, 3, 10],
        'min_samples_leaf': [1, 3, 10],
        'bootstrap': [True, False],
    }
    forest = RandomForestClassifier()
    cross_validation = StratifiedKFold(n_splits=5)

    grid_search = GridSearchCV(forest,
                               scoring='accuracy',
                               param_grid=parameter_grid,
                               cv=cross_validation,
                               verbose=1
                               )

    grid_search.fit(train, targets)
    model = grid_search
    parameters = grid_search.best_params_

    print('Best score: {}'.format(grid_search.best_score_))
    print('Best parameters: {}'.format(grid_search.best_params_))

else:
    parameters = {'bootstrap': False, 'min_samples_leaf': 3,
                  'n_estimators': 50,
                  'min_samples_split': 10, 'max_features': 'sqrt',
                  'max_depth': 6}

    model = RandomForestClassifier(**parameters)
    model.fit(train, targets)

print ('Model')
print (model)

# prediction


output = model.predict(test).astype(int)
df_output = pd.DataFrame()
aux = pd.read_csv('data/starfiles/test.csv')
df_output['Class'] = aux['Class']
df_output['Selection'] = output
print (df_output)
df_output.to_csv('NNresults.csv')

#trying other models

trained_models = []
for model in models:
    model.fit(train, targets)
    trained_models.append(model)

predictions = []
for model in trained_models:
    predictions.append(model.predict_proba(test)[:, 1])

predictions_df = pd.DataFrame(predictions).T
predictions_df['out'] = predictions_df.mean(axis=1)
predictions_df['Class'] = aux['Class']
predictions_df['out'] = predictions_df['out'].map(lambda s: 1 if s >= 0.5 else 0)

predictions_df = predictions_df[['Class', 'out']]
#predictions_df.columns = ['Class', 'Selection']

print ('New Prediction')
#print (predictions_df['Class'],predictions_df['Selection'])
print (predictions_df)

print ("Are we there yet?")





























