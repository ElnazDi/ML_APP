
import sys
from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults
from . import getDataNetto

class ReadNettoCategories(BaseOperator):
    #ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.nettoExtractor = getDataNetto.NettoExtractor()

    def execute(self, context):
        message = "Reading categories"
        self.nettoExtractor.etlReadCategories()
        print(message)
        return message


class ReadNettoBasicData(BaseOperator):
    #ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.nettoExtractor = getDataNetto.NettoExtractor()

    def execute(self, context):
        message = "Reading basic information"
        self.nettoExtractor.etlBasicInfo()
        print(message)
        return message


class ReadNettoDetailedData(BaseOperator):
    #ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.nettoExtractor = getDataNetto.NettoExtractor()

    def execute(self, context):
        message = "Reading detailed information"
        self.nettoExtractor.etlDetailedInfo()
        print(message)
        return message