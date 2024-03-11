import numpy as np
import pandas as pd
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import PolynomialFeatures

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


class DemandRegression(SolarRegression):
    holidays = country_holidays

    def getX(self, datetime):
        X = pd.DataFrame()
        X = X.assign(holiday=pd.Series(datetime).apply(lambda x: 1 if x in self.holidays else 0))
        X = X.assign(sy1=lambda x: np.sin(2 * np.pi * datetime.dayofyear / 365.25))
        X = X.assign(cy1=lambda x: np.cos(2 * np.pi * datetime.dayofyear / 365.25))
        X = X.join(pd.get_dummies(datetime.hour, prefix='hour'))  # Prefix added for clarity
        X = X.join(pd.get_dummies(datetime.day_name(), prefix='day'))

        # Ensure all column names are strings to avoid the TypeError
        X.columns = X.columns.astype(str)

        return self.poly.fit_transform(X)