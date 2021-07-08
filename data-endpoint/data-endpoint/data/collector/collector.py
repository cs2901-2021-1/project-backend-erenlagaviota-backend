import os
import sys
from sqlalchemy import create_engine, text
import pandas as pd


class Collector:
    """
    Get and merge external and requested data

    Attributes
    ----------
    connectionString : str
        string used to connect to the database

    Methods
    -------
    getConnection():
        Gets the connection to the database
    """

    connectionString: str
    periodLimit: str

    def __init__(self):
        """
        Initialize Collector with connectionString
        """
        connection = os.getenv('DB_CONNECTION')
        if connection is not None:
            self.connectionString = connection
            self.periodLimit = '2020-2'
        else:
            sys.exit()

    def getConnection(self):
        engine = create_engine(self.connectionString)
        return engine

    def getPeriodInfo(self):
        periodosDf = pd.read_sql(text("""
        SELECT descripcionlarga as periodo, codperiodo FROM PROGRAMACION.PRO_PERIODO
        """), con=self.getConnection())
        if periodosDf['periodo'] is not None:
            periodosDf['periodo'] = periodosDf['periodo'].str.replace(
                ' ', '')
            periodosDf = periodosDf[(periodosDf['periodo'].str.startswith(
                '20')) & (periodosDf['periodo'] < self.periodLimit)]
            if periodosDf is not None:
                periodosDf = periodosDf.sort_values(
                    by='periodo')  # type: ignore
                periodosDf.reset_index(  # type: ignore
                    drop=True, inplace=True)
        else:
            sys.exit()
        return periodosDf

    def getExternalData(self):
        connection = self.getConnection()
        periodosDf = self.getPeriodInfo()

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
        GROUP BY ACT.IDACTIVIDAD, AMT.CODPERIODORANGO"
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

        if periodosDf is not None:

            if averageCursoNotasDf['codperiodorango'] is not None:
                averageCursoNotasDf = averageCursoNotasDf[averageCursoNotasDf['codperiodorango'].isin(
                    periodosDf['codperiodo'])]
                if averageCursoNotasDf is not None:
                    averageCursoNotasDf = averageCursoNotasDf.drop(
                        columns='codperiodorango')
                    if averageCursoNotasDf is not None:
                        averageCursoNotasDf = averageCursoNotasDf.groupby(
                            by=['cod_curso'], as_index=False).mean()
                    else:
                        sys.exit()
                else:
                    sys.exit()
            else:
                sys.exit()
                

        else:
            sys.exit()
