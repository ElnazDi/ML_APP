
import sys

from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults
from . import getDataAldi

class ReadAldiCategories(BaseOperator):
    #ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.aldiExtractor = getDataAldi.AldiExtractor()

    def execute(self, context):
        message = "Reading categories"
        self.aldiExtractor.etlReadCategories()
        print(message)
        return message


class ReadAldiBasicData(BaseOperator):
    #ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.aldiExtractor = getDataAldi.AldiExtractor()

    def execute(self, context):
        message = "Reading basic information"
        self.aldiExtractor.etlBasicInfo()
        print(message)
        return message


class ReadAldiDetailedData(BaseOperator):
    #ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.aldiExtractor = getDataAldi.AldiExtractor()

    def execute(self, context):
        message = "Reading detailed information"
        self.aldiExtractor.etlDetailedInfo()
        print(message)
        return message