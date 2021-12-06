import tensorflow as tf # type: ignore[import]
from numpy import array # type: ignore[import]
from numpy import split
from sklearn.metrics import mean_squared_error # type: ignore[import]
from pandas import concat # type: ignore[import]
from pandas import read_csv
from os import path
from typing import List, Any, Tuple
from math import sqrt


class Model:
    def __init__(
        self,
        model_path: str = '1637553032',
        dayInput: str = '2021-9-27',
        dayOutput: str = '2021-9-29'
    ) -> None:
        root_directory = path.dirname(path.dirname(__file__))
        model_path = path.join(root_directory, "../saved_models", model_path)
        self.model = tf.keras.models.load_model(model_path)
        
        URL = 'https://raw.githubusercontent.com/chanelcolgate/hydroelectric-project/master/data/SMP_09112021.csv'
        # load all data
        dataset = read_csv(URL, header=0, infer_datetime_format=True,
                           parse_dates=['datetime'], index_col=['datetime'])
        
        smp = dataset.loc[dayInput]['SMP'].reset_index(drop=True)
        temp = dataset.loc[dayInput]['Temperature'].reset_index(drop=True)
        wind = dataset.loc[dayInput]['Wind Speed'].reset_index(drop=True)
        visi = dataset.loc[dayInput]['Visibility'].reset_index(drop=True)
        cloud = dataset.loc[dayInput]['Cloud Cover'].reset_index(drop=True)
        phuTai = dataset.loc[dayInput]['phuTai'].reset_index(drop=True)
        giaBien = dataset.loc[dayInput]['giaBien'].reset_index(drop=True)
        
        test_x = concat([smp, temp, wind, visi, cloud, phuTai, giaBien], axis=1).values
        self.test_x = array(split(test_x, len(test_x)/48))
        test_y = dataset.loc[dayOutput].values
        self.test_y = array(split(test_y, len(test_y)/48))
        
    # make a forecast
    @classmethod
    def forecast(self, model: Any, history: Any, n_input: int) -> Any:
        # flatten data
        data = array(history)
        data = data.reshape((data.shape[0]*data.shape[1], data.shape[2]))
        # retrieve last observations for input data
        input_x = data[-n_input:, :]
        # reshape into n input arrays
        input_x = [input_x[:,i].reshape((1,input_x.shape[0],1)) for i in range(input_x.shape[1])]
        # forecast the next week
        yhat = model.predict(input_x, verbose=0)
        # we only want the vector forecast
        yhat = yhat[0]
        return yhat
    
    # evaluate one or more weekly forecasts against expected values
    @classmethod
    def evaluate_forecasts(self, actual: Any, predicted: Any) -> Any:
        scores = list()
        # calculate an RMSE score for each day
        for i in range(actual.shape[1]):
            # calculate mse
            mse = mean_squared_error(actual[:, i], predicted[:, i])
            # calculate rmse
            rmse = sqrt(mse)
            # store
            scores.append(rmse)
        # calculate overall RMSE
        s = 0
        for row in range(actual.shape[0]):
            for col in range(actual.shape[1]):
                s += (actual[row, col] - predicted[row, col])**2
        score = sqrt(s / (actual.shape[0] * actual.shape[1]))
        return score, scores
    
    # summarize scores
    @classmethod
    def summarize_scores(self, name: 'str', score: float, scores: List[float]) -> None:
        s_scores = ', '.join([f'{s:.1f}' for s in scores])
        print(f'{name}: [{score:.3f}] {s_scores}')
    
# model = Model()
# predictions = model.forecast(model.model, model.test_x, 48)
# score, scores = model.evaluate_forecasts(model.test_y[:, :, 0], array(predictions).reshape(1, 48))
# model.summarize_scores('cnn', score, scores)