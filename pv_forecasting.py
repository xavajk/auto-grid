import numpy as np
import pandas as pd
import keras
# import tensorflow as tf
# import matplotlib.pyplot as plt
# import math
# from keras.models import Sequential
# from keras.layers import Dense
# from keras.layers import LSTM
# from keras.utils import plot_model
from sklearn.preprocessing import MinMaxScaler
from keras.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
# from sklearn.metrics import r2_score

# from keras import regularizers
# from keras.optimizers import RMSprop, Adam, SGD
# import datetime
# import seaborn as sns

# import pydot
# import graphviz
# from opt_einsum.backends import tensorflow

class PVPredict():
    async def run(self):
        # Fix random seed for reproducibility
        np.random.seed(7)
        # Load the dataset
        dataset = pd.read_csv('data_pv.csv')
        X = dataset.iloc[:, :-1].values
        y = dataset.iloc[:, -1].values
        y = np.reshape(y, (-1,1))

        # Splitting Training and Test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
        #print("Train Shape: {} {} \nTest Shape: {} {}".format(X_train.shape, y_train.shape, X_test.shape, y_test.shape))

        # Normalize the dataset
        scaler_x = MinMaxScaler(feature_range=(0, 1))
        X_train = scaler_x.fit_transform(X_train)
        X_test = scaler_x.fit_transform(X_test)

        scaler_y = MinMaxScaler(feature_range=(0, 1))
        y_train = scaler_y.fit_transform(y_train)
        y_test = scaler_y.fit_transform(y_test)

        # model = tf.keras.models.Sequential()
        # for i, nodes in enumerate([32, 64]):
        #     if i == 0:
        #         model.add(Dense(nodes, kernel_initializer='normal', activation='relu', input_dim=X_train.shape[1]))
        #     else:
        #         model.add(Dense(nodes, activation='relu', kernel_initializer='normal'))

        # model.add(Dense(1))
        # model.compile(loss='mse',
        #               optimizer='adam',
        #               metrics=[tf.keras.metrics.RootMeanSquaredError()])

        # model.fit(X_train, y_train, batch_size=32, validation_data=(X_test, y_test), epochs=150, verbose=1)
        # model.save('solar_forecast.keras')

        # plt.plot(hist.history['root_mean_squared_error'])
        # plt.title('Root Mean Squares Error')
        # plt.xlabel('Epochs')
        # plt.ylabel('error')
        # plt.show()

        # model.evaluate(X_train, y_train)
        # y_pred = model.predict(X_test)  # get model predictions (scaled inputs here)
        # y_pred_orig = scaler_y.inverse_transform(y_pred)  # unscale the predictions
        # y_test_orig = scaler_y.inverse_transform(y_test)  # unscale the true test outcomes
        # # RMSE_orig = mean_squared_error(y_pred_orig, y_test_orig, squared=False)

        # train_pred = model.predict(X_train)  # get model predictions (scaled inputs here)
        # train_pred_orig = scaler_y.inverse_transform(train_pred)  # unscale the predictions
        # y_train_orig = scaler_y.inverse_transform(y_train)  # unscale the true train outcomes

        # mean_squared_error(train_pred_orig, y_train_orig, squared=False)
        # r2_score(y_pred_orig, y_test_orig)
        # r2_score(train_pred_orig, y_train_orig)
        # np.concatenate((train_pred_orig, y_train_orig), 1)
        # np.concatenate((y_pred_orig, y_test_orig), 1)

        # plt.figure(figsize=(16, 6))
        # plt.subplot(1, 2, 2)
        # plt.scatter(y_pred_orig, y_test_orig)
        # plt.xlabel('Predicted Generated Power on Test Data')
        # plt.ylabel('Real Generated Power on Test Data')
        # plt.title('Test Predictions vs Real Data')
        # #plt.scatter(y_test_orig, scaler_x.inverse_transform(X_test)[:,2], color='green')
        # plt.subplot(1, 2, 1)
        # plt.scatter(train_pred_orig, y_train_orig)
        # plt.xlabel('Predicted Generated Power on Training Data')
        # plt.ylabel('Real Generated Power on Training Data')
        # plt.title('Training Predictions vs Real Data')
        # plt.show()

        model = keras.models.load_model('solar_forecast.keras')
        y_pred = model.predict(X_test, verbose=0)  # get model predictions (scaled inputs here)
        y_pred_orig = scaler_y.inverse_transform(y_pred)  # unscale the predictions
        y_test_orig = scaler_y.inverse_transform(y_test)  # unscale the true test outcomes
        RMSE_orig = mean_squared_error(y_test_orig, y_pred_orig)
        print(f"[SOLAR] RMSE for current forecasting model: {RMSE_orig}")