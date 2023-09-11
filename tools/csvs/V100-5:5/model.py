import numpy as np
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import GridSearchCV, StratifiedKFold, KFold
from sklearn.model_selection import learning_curve
from sklearn.model_selection import train_test_split
from sklearn.metrics import fbeta_score, make_scorer, mean_squared_error, r2_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.multioutput import MultiOutputRegressor

from keras.models import Sequential
from keras.layers.core import Dense, Activation
import tensorflow as tf
import keras
import os
from keras.layers import BatchNormalization
import xgboost as xgb
from xgboost import XGBClassifier, XGBRegressor, plot_importance

def mean_absolute_percentage_error(ground_truth, predictions):
    return np.mean(abs(ground_truth - predictions) / ground_truth)

def nn_fitting(X, y,output_size):
    model = Sequential()
    print("input size (num_samples, feature_dim): (%d, %d)." % (X.shape[0], X.shape[1]))
    model.add(Dense(128, input_shape=(X.shape[1],)))
    model.add(BatchNormalization())
    model.add(Activation('sigmoid'))
    model.add(Dense(128))
    model.add(BatchNormalization())
    model.add(Activation('sigmoid'))
    model.add(Dense(128))
    model.add(BatchNormalization())
    model.add(Activation('sigmoid'))
    model.add(Dense(128))
    model.add(BatchNormalization())
    model.add(Activation('sigmoid'))
    model.add(Dense(128))
    model.add(BatchNormalization())
    model.add(Activation('sigmoid'))
    model.add(Dense(output_size))

    lr_schedule = tf.keras.optimizers.schedules.CosineDecay(
        initial_learning_rate=0.9,
        decay_steps=3000
    )
    # opt = keras.optimizers.Adam(learning_rate=1e-3)
    opt = keras.optimizers.SGD(learning_rate=lr_schedule)
    model.compile(optimizer=opt, loss=tf.keras.losses.MeanAbsoluteError())

    model.summary()

    model.fit(X, y, batch_size=32, epochs=5)   #, steps_per_epoch=3)

    return model


def xg_fitting(X, y):

    # make score function
    loss = make_scorer(mean_absolute_percentage_error, greater_is_better=False)

    # n_estimators = [300, 400]
    # max_depth = [3, 4]
    # learning_rate = [0.3, 0.2, 0,1, 0.05]
    # min_child_weight = [0.1, 0.5, 1, 2]
    n_estimators = [50,75,100,125]
    max_depth = [2,3,4]
    learning_rate = [0.1,0.2]
    min_child_weight = [0.5]
    param_grid = dict(max_depth=max_depth, n_estimators=n_estimators, learning_rate=learning_rate, min_child_weight=min_child_weight)
    
    xg_model = GridSearchCV(XGBRegressor(), cv=3, param_grid=param_grid, scoring='neg_mean_squared_error', n_jobs=-1, verbose=True)
    #xg_model = GridSearchCV(XGBRegressor(verbose=True, early_stopping_rounds=5), cv=10, param_grid=param_grid, scoring='neg_mean_squared_error', n_jobs=-1, verbose=True)
    xg_model.fit(X, y)

    return xg_model
   
    # multi_xg_model = MultiOutputRegressor(xg_model).fit(X, y)

    # return multi_xg_model

def muloutput_xg_fitting(X, y):

    # make score function
    loss = make_scorer(mean_absolute_percentage_error, greater_is_better=False)

    # n_estimators = [300, 400]
    # max_depth = [3, 4]
    # learning_rate = [0.3, 0.2, 0,1, 0.05]
    # min_child_weight = [0.1, 0.5, 1, 2]
    n_estimators = [500,700,900]
    max_depth = [2,3,4]
    learning_rate = [0.3, 0.2, 0,1, 0.05]
    min_child_weight =[0.1, 0.5, 1, 2]
    param_grid = dict(max_depth=max_depth, n_estimators=n_estimators, learning_rate=learning_rate, min_child_weight=min_child_weight)
    
    xg_model = GridSearchCV(XGBRegressor(), cv=3, param_grid=param_grid, scoring='neg_mean_squared_error', n_jobs=-1, verbose=True)
    #xg_model = GridSearchCV(XGBRegressor(verbose=True, early_stopping_rounds=5), cv=10, param_grid=param_grid, scoring='neg_mean_squared_error', n_jobs=-1, verbose=True)

   
    multi_xg_model = MultiOutputRegressor(xg_model).fit(X, y)

    return multi_xg_model