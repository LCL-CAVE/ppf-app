import pandas as pd
import numpy as np
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import PolynomialFeatures
import holidays

class SolarRegression(LassoCV):
    poly = PolynomialFeatures(degree=2, interaction_only=False, include_bias=False)

    def getX(self, datetime):
        X = (pd.DataFrame()
             .assign(sy1=lambda x: np.sin(2 * np.pi * datetime.dayofyear / 365.25))
             .assign(cy1=lambda x: np.cos(2 * np.pi * datetime.dayofyear / 365.25))
             .join(pd.get_dummies(datetime.hour))
             )
        return self.poly.fit_transform(X)

    def fit(self, datetime, y):
        super().fit(self.getX(datetime), y)

    def score(self, datetime, y):
        return super().score(self.getX(datetime), y)

    def predict(self, datetime):
        return super().predict(self.getX(datetime))


class WindRegression(SolarRegression):

    def getX(self, datetime):
        X = (pd.DataFrame(index=datetime)
             .assign(sy1=lambda x: np.sin(2 * np.pi * datetime.dayofyear / 365.25))
             .assign(cy1=lambda x: np.cos(2 * np.pi * datetime.dayofyear / 365.25))
             )
        return self.poly.fit_transform(X)


class TemperatureRegression(SolarRegression):

    def getX(self, datetime):
        X = (pd.DataFrame(index=datetime)
             .assign(sy1=lambda x: np.sin(2 * np.pi * datetime.dayofyear / 365.25))
             .assign(cy1=lambda x: np.cos(2 * np.pi * datetime.dayofyear / 365.25))
             )
        return self.poly.fit_transform(X)

class RorRegression(SolarRegression):

    def getX(self, datetime):
        X = (pd.DataFrame(index=datetime)
             .assign(sy1=lambda x: np.sin(2 * np.pi * datetime.dayofyear / 365.25))
             .assign(cy1=lambda x: np.cos(2 * np.pi * datetime.dayofyear / 365.25))
             )
        return self.poly.fit_transform(X)

class DemandRegression(SolarRegression):
    holidays = holidays.Spain()

    def getX(self, datetime):
        X = (pd.DataFrame()
             .assign(holiday=pd.Series(datetime).apply(lambda x: 1 if x in self.holidays else 0))
             .assign(sy1=lambda x: np.sin(2 * np.pi * datetime.dayofyear / 365.25))
             .assign(cy1=lambda x: np.cos(2 * np.pi * datetime.dayofyear / 365.25))
             .join(pd.get_dummies(datetime.hour))
             .join(pd.get_dummies(datetime.day_name()))
             )
        return self.poly.fit_transform(X)
