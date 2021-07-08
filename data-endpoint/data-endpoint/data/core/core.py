from ..collector.collector import Collector
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import pandas as pd


class Core:

    ondemand: bool
    params: tuple
    collector: Collector

    def __init__(self):
        self.collector = Collector()
        params = self.collector.getExternalDataCached()
        ondemand = params[0]
        if ondemand:
            self.params = params[1:]
        # TODO:  <08-07-21, Mario> Implement not ondemand mode

        # return averageCursoNotasDf, averageCursoRepDf, averageCountPastDf, countCurrentDf
    def getProjection(self, cod_curso: str):
        countCurrentDf = self.params[3].rename(
            columns={'count', {'countCurrent'}})  # type: ignore
        averageCursoNotasDf = self.params[0].rename(
            columns={'average', 'averageScore'})
        averageCursoRepDf = self.params[1].rename(
            columns={'average', 'averageRep'})
        averageCountPastDf = self.params[2].rename(
            columns={'count', 'countPast'})

        final = pd.concat(
            [averageCursoNotasDf, averageCursoRepDf], axis=1, join='inner')
        final = pd.concat([final, averageCountPastDf], axis=1, join='inner')
        final = final.loc[:, ~final.columns.duplicated()]

        final = final.set_index('cod_curso')
        countCurrentDf = countCurrentDf.set_index('cod_curso')

        regression = pd.concat([final, countCurrentDf], axis=1, join='inner')

        regression_independent = regression[[
            'averageScore', 'averageRep', 'countPast']]
        regression_dependent = regression[['countCurrent']]

        X_train, X_test, y_train, y_test = train_test_split(
            regression_independent, regression_dependent, test_size=0.2, random_state=42)
        lin_model = LinearRegression()
        lin_model.fit(X_train,y_train)

        y_train_predict = lin_model.predict(X_train)
        r2 = r2_score(y_train,y_train_predict)

        return 1
