import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

from ..collector.collector import Collector


class Core:

    ondemand: bool
    params: tuple
    collector: Collector
    projection: LinearRegression
    r2: float
    correlationMatrix: pd.DataFrame

    def __init__(self):
        self.collector = Collector()
        params = self.collector.getExternalDataCached()
        ondemand = params[0]
        if ondemand:
            self.params = params[1:]
            self.getModel()
        # TODO:  <08-07-21, Mario> Implement not ondemand mode

        # return averageCursoNotasDf, averageCursoRepDf, averageCountPastDf, countCurrentDf
    def getModel(self):
        countCurrentDf = self.params[3].rename(
            columns={'count', {'countCurrent'}})  # type: ignore
        averageCursoNotasDf = self.params[0].rename(
            columns={'average', 'averageScore'})
        averageCursoRepDf = self.params[1].rename(
            columns={'average', 'averageRep'})
        averageCountPastDf = self.params[2].rename(
            columns={'count', 'countPast'})

        mergedDf = pd.concat( [averageCursoNotasDf, averageCursoRepDf], axis=1, join='inner')
        mergedDf = pd.concat([mergedDf, averageCountPastDf], axis=1, join='inner')
        mergedDf = mergedDf.loc[:, ~mergedDf.columns.duplicated()]

        mergedDf = mergedDf.set_index('cod_curso')
        countCurrentDf = countCurrentDf.set_index('cod_curso')

        regression = pd.concat([mergedDf, countCurrentDf], axis=1, join='inner')

        regression_independent = regression[[
            'averageScore', 'averageRep', 'countPast']]
        regression_dependent = regression[['countCurrent']]

        X_train, X_test, y_train, y_test = train_test_split(
            regression_independent, regression_dependent, test_size=0.2, random_state=42)
        lin_model = LinearRegression()
        lin_model.fit(X_train,y_train)

        y_train_predict = lin_model.predict(X_train)
        r2 = r2_score(y_train,y_train_predict)

        self.r2 = r2  # type: ignore
        self.projection = lin_model
        self.correlationMatrix = mergedDf.corr().round(2)

    def getProjection(self, cod_curso: str):
        if self.ondemand:
            return self.projection.predict(np.array[[self.collector.cursoNota,self.collector.cursoRep,self.collector.countPast]])[0][0]  # type: ignore
        
