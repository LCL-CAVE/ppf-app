import numpy as np
import pandas as pd
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import PolynomialFeatures


class SolarRegression(LassoCV):
    poly = PolynomialFeatures(degree=2, interaction_only=False, include_bias=False)

    def getX(self, datetime):
        X = pd.DataFrame({
            'sy1': np.sin(2 * np.pi * datetime.dayofyear / 365.25),
            'cy1': np.cos(2 * np.pi * datetime.dayofyear / 365.25),
        })

        # Generate hour dummies without converting to strings
        hour_dummies = pd.get_dummies(datetime.hour, prefix='hour')

        # Join the initial features with hour dummies
        X = pd.concat([X, hour_dummies], axis=1)

        # No need to convert column names to strings here
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


class RorRegression(SolarRegression):

    def getX(self, datetime):
        X = (pd.DataFrame(index=datetime)
             .assign(sy1=lambda x: np.sin(2 * np.pi * datetime.dayofyear / 365.25))
             .assign(cy1=lambda x: np.cos(2 * np.pi * datetime.dayofyear / 365.25))
             )
        return self.poly.fit_transform(X)