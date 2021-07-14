import os
import sys
from sqlalchemy import create_engine, text
import pandas as pd
from ...exception.exception import *


class Collector:
    """
    Get and merge external and requested data

    Attributes
    ----------
    connectionString : str
        string used to connect to the database

    periodLimit : str
        target period

    Methods
    -------
    getConnection():
        Gets the connection to the database

    getPeriodInfo():
        Gets the period data available in the database

    getExternalData():
        Gets the data needed to make the projection

    getExternalDataCached():
        Gets the data used by core, it could be cached or on demand
    """

    connectionString: str
    periodLimit: str
    cursoNota: pd.DataFrame
    cursoRep: pd.DataFrame
    countPast: pd.DataFrame
    periodInfo: list

    def __init__(self):
        """
        Initialize Collector with connectionString
         TODO:  <08-07-21, Mario> Function to get the periodLimit
        """
        connection = os.getenv('DB_CONNECTION')
        if connection is not None:
            self.connectionString = connection
            self.periodLimit = '2020-2'
            self.periodInfo = []
        else:
            raise Exception("error")

    def getConnection(self):
        engine = create_engine(self.connectionString)
        return engine

    def getPeriodInfo(self):
        """
        A period is considered only if its `name` (descripcionlarga) starts with `20`
        """
        codPeriodlimit: int
        periodosDf = pd.read_sql(text("""
        SELECT descripcionlarga as periodo, codperiodo FROM PROGRAMACION.PRO_PERIODO
        """), con=self.getConnection())
        if periodosDf['periodo'] is not None:
            periodosDf['periodo'] = periodosDf['periodo'].str.replace(
                ' ', '')
            codPeriodlimit = int(
                periodosDf[periodosDf['periodo'] == self.periodLimit]['codperiodo'])  # type: ignore
            periodosDf = periodosDf[(periodosDf['periodo'].str.startswith(
                '20')) & (periodosDf['periodo'] < self.periodLimit)]
            if periodosDf is not None:
                periodosDf = periodosDf.sort_values(
                    by='periodo')  # type: ignore
                periodosDf.reset_index(  # type: ignore
                    drop=True, inplace=True)
        else:
            raise PeriodError()
        self.periodInfo = [periodosDf, codPeriodlimit]

    def getExternalData(self):
        """
        The following data is used and collected from the database:

        `averageCursoNotasDf` = average score of courses just before periodLimit

        `averageCursoRepDf` = average number of times the course has been taken just before periodLimit

        `averageCountPastDf` = average number of participants of courses just before periodLimit

        `countCurrentDf` = count of students for each course to be used as target. (periodLimit)
        """
        connection = self.getConnection()
        if len(self.periodInfo) == 0:
            self.getPeriodInfo()
        periodosDf = self.periodInfo[0]
        codPeriodlimit = self.periodInfo[1]

        averageCursoNotasDf = pd.read_sql(text("""
        SELECT  ACT.IDACTIVIDAD AS cod_curso,
        AVG(AMC.PROMEDIOFINAL) as average,
        AMT.CODPERIODORANGO
        FROM ACADEMICO.ACA_ALUMNO_MATRICULA_CURSO AMC
        INNER JOIN ACADEMICO.ACA_ALUMNO_MATRICULA AMT ON AMT.CODALUMNOMATRICULA = AMC.CODALUMNOMATRICULA AND AMT.ISDELETED = 'N'
        INNER JOIN ACADEMICO.ACA_ALUMNO_MALLA AM ON AM.CODALUMNOMALLA = AMT.CODALUMNOMALLA AND AM.ISDELETED = 'N'
        INNER JOIN CONFIGURACION.CON_MALLA MA ON MA.CODMALLA = AM.CODMALLA  AND MA.ISDELETED = 'N'
        INNER JOIN CONFIGURACION.CON_CURSO_VERSION CV ON CV.CODCURSOVERSION = AMC.CODCURSOVERSION AND CV.ISDELETED = 'N'
        INNER JOIN CONFIGURACION.CON_PRODUCTO PROD ON PROD.CODPRODUCTO = MA.CODPRODUCTO AND PROD.ISDELETED = 'N'
        INNER JOIN PROGRAMACION.PRO_PERIODORANGO PR ON PR.CODPERIODORANGO = AMT.CODPERIODORANGO AND PR.ISDELETED = 'N'
        INNER JOIN PROGRAMACION.PRO_PERIODO PER ON PER.CODPERIODO = PR.CODPERIODO AND PER.ISDELETED = 'N'
        INNER JOIN CONFIGURACION.CON_ACTIVIDAD ACT ON ACT.CODACTIVIDAD = CV.CODCURSO AND ACT.ISDELETED = 'N'
        INNER JOIN GENERAL.GEN_AREA_FUNCIONAL AF ON AF.CODAREAFUNCIONAL = ACT.CODAREAFUNCIONAL AND AF.ISDELETED='N'
        INNER JOIN GENERAL.GEN_ALUMNO GA ON GA.CODALUMNO = AM.CODALUMNO AND GA.ISDELETED = 'N'
        INNER JOIN GENERAL.GEN_PERSONA PERS ON PERS.CODPERSONA = GA.CODALUMNO AND PERS.ISDELETED = 'N'
        LEFT JOIN ACADEMICO.ACA_ALUMNO_AVANCE_ACADEMICO AVAN ON AVAN.CODALUMNOAVANCEACADEMICO = AMT.CODALUMNOMATRICULA AND AVAN.ISDELETED = 'N'
        WHERE AMC.ISDELETED = 'N'
        GROUP BY ACT.IDACTIVIDAD, AMT.CODPERIODORANGO
        """), con=connection)

        averageCursoRepDf = pd.read_sql(text("""
        SELECT  ACT.IDACTIVIDAD AS cod_curso,
        AVG(AMC.NROVECESMATRICULADO) as average,
        AMT.CODPERIODORANGO
        FROM ACADEMICO.ACA_ALUMNO_MATRICULA_CURSO AMC
        INNER JOIN ACADEMICO.ACA_ALUMNO_MATRICULA AMT ON AMT.CODALUMNOMATRICULA = AMC.CODALUMNOMATRICULA AND AMT.ISDELETED = 'N'
        INNER JOIN ACADEMICO.ACA_ALUMNO_MALLA AM ON AM.CODALUMNOMALLA = AMT.CODALUMNOMALLA AND AM.ISDELETED = 'N'
        INNER JOIN CONFIGURACION.CON_MALLA MA ON MA.CODMALLA = AM.CODMALLA  AND MA.ISDELETED = 'N'
        INNER JOIN CONFIGURACION.CON_CURSO_VERSION CV ON CV.CODCURSOVERSION = AMC.CODCURSOVERSION AND CV.ISDELETED = 'N'
        INNER JOIN CONFIGURACION.CON_PRODUCTO PROD ON PROD.CODPRODUCTO = MA.CODPRODUCTO AND PROD.ISDELETED = 'N'
        INNER JOIN PROGRAMACION.PRO_PERIODORANGO PR ON PR.CODPERIODORANGO = AMT.CODPERIODORANGO AND PR.ISDELETED = 'N'
        INNER JOIN PROGRAMACION.PRO_PERIODO PER ON PER.CODPERIODO = PR.CODPERIODO AND PER.ISDELETED = 'N'
        INNER JOIN CONFIGURACION.CON_ACTIVIDAD ACT ON ACT.CODACTIVIDAD = CV.CODCURSO AND ACT.ISDELETED = 'N'
        INNER JOIN GENERAL.GEN_AREA_FUNCIONAL AF ON AF.CODAREAFUNCIONAL = ACT.CODAREAFUNCIONAL AND AF.ISDELETED='N'
        INNER JOIN GENERAL.GEN_ALUMNO GA ON GA.CODALUMNO = AM.CODALUMNO AND GA.ISDELETED = 'N'
        INNER JOIN GENERAL.GEN_PERSONA PERS ON PERS.CODPERSONA = GA.CODALUMNO AND PERS.ISDELETED = 'N'
        LEFT JOIN ACADEMICO.ACA_ALUMNO_AVANCE_ACADEMICO AVAN ON AVAN.CODALUMNOAVANCEACADEMICO = AMT.CODALUMNOMATRICULA AND AVAN.ISDELETED = 'N'
        WHERE AMC.ISDELETED = 'N'
        GROUP BY ACT.IDACTIVIDAD, AMT.CODPERIODORANGO
        """), con=connection)

        averageCountPastDf = pd.read_sql(text("""
        SELECT  ACT.IDACTIVIDAD AS cod_curso,
        COUNT(ACT.IDACTIVIDAD) as count,
        AMT.CODPERIODORANGO
        FROM ACADEMICO.ACA_ALUMNO_MATRICULA_CURSO AMC
        INNER JOIN ACADEMICO.ACA_ALUMNO_MATRICULA AMT ON AMT.CODALUMNOMATRICULA = AMC.CODALUMNOMATRICULA AND AMT.ISDELETED = 'N'
        INNER JOIN ACADEMICO.ACA_ALUMNO_MALLA AM ON AM.CODALUMNOMALLA = AMT.CODALUMNOMALLA AND AM.ISDELETED = 'N'
        INNER JOIN CONFIGURACION.CON_MALLA MA ON MA.CODMALLA = AM.CODMALLA  AND MA.ISDELETED = 'N'
        INNER JOIN CONFIGURACION.CON_CURSO_VERSION CV ON CV.CODCURSOVERSION = AMC.CODCURSOVERSION AND CV.ISDELETED = 'N'
        INNER JOIN CONFIGURACION.CON_PRODUCTO PROD ON PROD.CODPRODUCTO = MA.CODPRODUCTO AND PROD.ISDELETED = 'N'
        INNER JOIN PROGRAMACION.PRO_PERIODORANGO PR ON PR.CODPERIODORANGO = AMT.CODPERIODORANGO AND PR.ISDELETED = 'N'
        INNER JOIN PROGRAMACION.PRO_PERIODO PER ON PER.CODPERIODO = PR.CODPERIODO AND PER.ISDELETED = 'N'
        INNER JOIN CONFIGURACION.CON_ACTIVIDAD ACT ON ACT.CODACTIVIDAD = CV.CODCURSO AND ACT.ISDELETED = 'N'
        INNER JOIN GENERAL.GEN_AREA_FUNCIONAL AF ON AF.CODAREAFUNCIONAL = ACT.CODAREAFUNCIONAL AND AF.ISDELETED='N'
        INNER JOIN GENERAL.GEN_ALUMNO GA ON GA.CODALUMNO = AM.CODALUMNO AND GA.ISDELETED = 'N'
        INNER JOIN GENERAL.GEN_PERSONA PERS ON PERS.CODPERSONA = GA.CODALUMNO AND PERS.ISDELETED = 'N'
        LEFT JOIN ACADEMICO.ACA_ALUMNO_AVANCE_ACADEMICO AVAN ON AVAN.CODALUMNOAVANCEACADEMICO = AMT.CODALUMNOMATRICULA AND AVAN.ISDELETED = 'N'
        WHERE AMC.ISDELETED = 'N'
        GROUP BY ACT.IDACTIVIDAD, AMT.CODPERIODORANGO
        """), con=connection)

        countCurrentDf = pd.read_sql(text("""
        SELECT  ACT.IDACTIVIDAD AS cod_curso,
        COUNT(ACT.IDACTIVIDAD) as count,
        AMT.CODPERIODORANGO
        FROM ACADEMICO.ACA_ALUMNO_MATRICULA_CURSO AMC
        INNER JOIN ACADEMICO.ACA_ALUMNO_MATRICULA AMT ON AMT.CODALUMNOMATRICULA = AMC.CODALUMNOMATRICULA AND AMT.ISDELETED = 'N'
        INNER JOIN ACADEMICO.ACA_ALUMNO_MALLA AM ON AM.CODALUMNOMALLA = AMT.CODALUMNOMALLA AND AM.ISDELETED = 'N'
        INNER JOIN CONFIGURACION.CON_MALLA MA ON MA.CODMALLA = AM.CODMALLA  AND MA.ISDELETED = 'N' 
        INNER JOIN CONFIGURACION.CON_CURSO_VERSION CV ON CV.CODCURSOVERSION = AMC.CODCURSOVERSION AND CV.ISDELETED = 'N' 
        INNER JOIN CONFIGURACION.CON_PRODUCTO PROD ON PROD.CODPRODUCTO = MA.CODPRODUCTO AND PROD.ISDELETED = 'N' 
        INNER JOIN PROGRAMACION.PRO_PERIODORANGO PR ON PR.CODPERIODORANGO = AMT.CODPERIODORANGO AND PR.ISDELETED = 'N'
        INNER JOIN PROGRAMACION.PRO_PERIODO PER ON PER.CODPERIODO = PR.CODPERIODO AND PER.ISDELETED = 'N'
        INNER JOIN CONFIGURACION.CON_ACTIVIDAD ACT ON ACT.CODACTIVIDAD = CV.CODCURSO AND ACT.ISDELETED = 'N' 
        INNER JOIN GENERAL.GEN_AREA_FUNCIONAL AF ON AF.CODAREAFUNCIONAL = ACT.CODAREAFUNCIONAL AND AF.ISDELETED='N'
        INNER JOIN GENERAL.GEN_ALUMNO GA ON GA.CODALUMNO = AM.CODALUMNO AND GA.ISDELETED = 'N'
        INNER JOIN GENERAL.GEN_PERSONA PERS ON PERS.CODPERSONA = GA.CODALUMNO AND PERS.ISDELETED = 'N'
        LEFT JOIN ACADEMICO.ACA_ALUMNO_AVANCE_ACADEMICO AVAN ON AVAN.CODALUMNOAVANCEACADEMICO = AMT.CODALUMNOMATRICULA AND AVAN.ISDELETED = 'N'
        WHERE AMC.ISDELETED = 'N'
        GROUP BY ACT.IDACTIVIDAD, AMT.CODPERIODORANGO
        """), con=connection)

        self.cursoNota = averageCursoNotasDf[averageCursoNotasDf['codperiodorango'] # type: ignore
                                             == codPeriodlimit]
        self.cursoRep = averageCursoRepDf[averageCursoRepDf['codperiodorango'] # type: ignore
                                          == codPeriodlimit]
        self.countPast = averageCountPastDf[averageCountPastDf['codperiodorango'] # type: ignore
                                            == codPeriodlimit]

        if averageCursoNotasDf['codperiodorango'] is not None and averageCursoRepDf['codperiodorango'] is not None and averageCountPastDf['codperiodorango'] is not None and periodosDf is not None:
            averageCursoNotasDf = averageCursoNotasDf[averageCursoNotasDf['codperiodorango'].isin(
                periodosDf['codperiodo'])]
            averageCursoRepDf = averageCursoRepDf[averageCursoRepDf['codperiodorango'].isin(
                periodosDf['codperiodo'])]
            averageCountPastDf = averageCountPastDf[averageCountPastDf['codperiodorango'].isin(
                periodosDf['codperiodo'])]
            if averageCursoNotasDf is not None and averageCursoRepDf is not None and averageCountPastDf is not None:
                averageCursoNotasDf = averageCursoNotasDf.drop(
                    columns='codperiodorango')
                averageCursoRepDf = averageCursoRepDf.drop(
                    columns='codperiodorango')
                averageCountPastDf = averageCountPastDf.drop(
                    columns='codperiodorango')
                if averageCursoNotasDf is not None and averageCursoRepDf is not None and averageCountPastDf is not None:
                    averageCursoNotasDf = averageCursoNotasDf.groupby(
                        by=['cod_curso'], as_index=False).mean()
                    averageCursoRepDf = averageCursoRepDf.groupby(
                        by=['cod_curso'], as_index=False).mean()
                    averageCountPastDf = averageCountPastDf.groupby(
                        by=['cod_curso'], as_index=False).mean()
                else:
                    raise PeriodError()
            else:
                raise PeriodError()
        else:
            raise PeriodRangeError()

        if countCurrentDf['codperiodorango'] is not None:
            countCurrentDf = countCurrentDf[countCurrentDf['codperiodorango']
                                            == codPeriodlimit]
            if countCurrentDf is not None:
                countCurrentDf = countCurrentDf.drop(columns='codperiodorango')
                countCurrentDf = countCurrentDf.groupby( # type: ignore
                    by=['cod_curso'], as_index=False).mean()  
            else:
                raise PeriodRangeError()

        return averageCursoNotasDf, averageCursoRepDf, averageCountPastDf, countCurrentDf

    def getExternalDataCached(self):
        if (True):
            return True, self.getExternalData()
        # TODO:  <08-07-21, Mario> Define when it is needed to fetch data or use a cached version

    def getCursos(self):
        connection = self.getConnection()
        if len(self.periodInfo) == 0:
            self.getPeriodInfo()
        periodosDf = self.periodInfo[0]
        codPeriodlimit = self.periodInfo[1]

        cursosMetaInfo = pd.read_sql(text(f"""
        SELECT DISTINCT ACT.IDACTIVIDAD AS codCurso,
        ACT.DESCRIPCIONCORTA as name,
        AF.DESCRIPLARGA as department
        FROM ACADEMICO.ACA_ALUMNO_MATRICULA_CURSO AMC
        INNER JOIN ACADEMICO.ACA_ALUMNO_MATRICULA AMT ON AMT.CODALUMNOMATRICULA = AMC.CODALUMNOMATRICULA AND AMT.ISDELETED = 'N'
        INNER JOIN ACADEMICO.ACA_ALUMNO_MALLA AM ON AM.CODALUMNOMALLA = AMT.CODALUMNOMALLA AND AM.ISDELETED = 'N'
        INNER JOIN CONFIGURACION.CON_MALLA MA ON MA.CODMALLA = AM.CODMALLA  AND MA.ISDELETED = 'N' 
        INNER JOIN CONFIGURACION.CON_CURSO_VERSION CV ON CV.CODCURSOVERSION = AMC.CODCURSOVERSION AND CV.ISDELETED = 'N' 
        INNER JOIN CONFIGURACION.CON_PRODUCTO PROD ON PROD.CODPRODUCTO = MA.CODPRODUCTO AND PROD.ISDELETED = 'N' 
        INNER JOIN PROGRAMACION.PRO_PERIODORANGO PR ON PR.CODPERIODORANGO = AMT.CODPERIODORANGO AND PR.ISDELETED = 'N'
        INNER JOIN PROGRAMACION.PRO_PERIODO PER ON PER.CODPERIODO = PR.CODPERIODO AND PER.ISDELETED = 'N'
        INNER JOIN CONFIGURACION.CON_ACTIVIDAD ACT ON ACT.CODACTIVIDAD = CV.CODCURSO AND ACT.ISDELETED = 'N' 
        INNER JOIN GENERAL.GEN_AREA_FUNCIONAL AF ON AF.CODAREAFUNCIONAL = ACT.CODAREAFUNCIONAL AND AF.ISDELETED='N'
        INNER JOIN GENERAL.GEN_ALUMNO GA ON GA.CODALUMNO = AM.CODALUMNO AND GA.ISDELETED = 'N'
        INNER JOIN GENERAL.GEN_PERSONA PERS ON PERS.CODPERSONA = GA.CODALUMNO AND PERS.ISDELETED = 'N'
        LEFT JOIN ACADEMICO.ACA_ALUMNO_AVANCE_ACADEMICO AVAN ON AVAN.CODALUMNOAVANCEACADEMICO = AMT.CODALUMNOMATRICULA AND AVAN.ISDELETED = 'N'
        WHERE AMC.ISDELETED = 'N' AND ACT.IDACTIVIDAD IN 
(
        SELECT ACT.IDACTIVIDAD
        FROM ACADEMICO.ACA_ALUMNO_MATRICULA_CURSO AMC
        INNER JOIN ACADEMICO.ACA_ALUMNO_MATRICULA AMT ON AMT.CODALUMNOMATRICULA = AMC.CODALUMNOMATRICULA AND AMT.ISDELETED = 'N'
        INNER JOIN ACADEMICO.ACA_ALUMNO_MALLA AM ON AM.CODALUMNOMALLA = AMT.CODALUMNOMALLA AND AM.ISDELETED = 'N'
        INNER JOIN CONFIGURACION.CON_MALLA MA ON MA.CODMALLA = AM.CODMALLA  AND MA.ISDELETED = 'N' 
        INNER JOIN CONFIGURACION.CON_CURSO_VERSION CV ON CV.CODCURSOVERSION = AMC.CODCURSOVERSION AND CV.ISDELETED = 'N' 
        INNER JOIN CONFIGURACION.CON_PRODUCTO PROD ON PROD.CODPRODUCTO = MA.CODPRODUCTO AND PROD.ISDELETED = 'N' 
        INNER JOIN PROGRAMACION.PRO_PERIODORANGO PR ON PR.CODPERIODORANGO = AMT.CODPERIODORANGO AND PR.ISDELETED = 'N'
        INNER JOIN PROGRAMACION.PRO_PERIODO PER ON PER.CODPERIODO = PR.CODPERIODO AND PER.ISDELETED = 'N'
        INNER JOIN CONFIGURACION.CON_ACTIVIDAD ACT ON ACT.CODACTIVIDAD = CV.CODCURSO AND ACT.ISDELETED = 'N' 
        INNER JOIN GENERAL.GEN_AREA_FUNCIONAL AF ON AF.CODAREAFUNCIONAL = ACT.CODAREAFUNCIONAL AND AF.ISDELETED='N'
        INNER JOIN GENERAL.GEN_ALUMNO GA ON GA.CODALUMNO = AM.CODALUMNO AND GA.ISDELETED = 'N'
        INNER JOIN GENERAL.GEN_PERSONA PERS ON PERS.CODPERSONA = GA.CODALUMNO AND PERS.ISDELETED = 'N'
        LEFT JOIN ACADEMICO.ACA_ALUMNO_AVANCE_ACADEMICO AVAN ON AVAN.CODALUMNOAVANCEACADEMICO = AMT.CODALUMNOMATRICULA AND AVAN.ISDELETED = 'N'
        WHERE AMC.ISDELETED = 'N' AND AMT.CODPERIODORANGO = :periodLimit
) AND AMT.CODPERIODORANGO IN ({str(list(periodosDf['codperiodo'])).replace('[','').replace(']','')})
        """).bindparams(periodLimit=codPeriodlimit), con=connection)

        if cursosMetaInfo is not None:
            return cursosMetaInfo.to_json(orient='records',force_ascii=False)
        else:
            raise PeriodError()
