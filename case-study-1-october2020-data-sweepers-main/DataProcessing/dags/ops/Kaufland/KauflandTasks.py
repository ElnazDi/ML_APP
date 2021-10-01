
import sys

from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults
from . import getDataKaufland

class ReadKauflandCategories(BaseOperator):
    #ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.kauflandExtractor = getDataKaufland.KauflandExtractor()

    def execute(self, context):
        message = "Reading categories"
        self.kauflandExtractor.etlReadCategories()
        print(message)
        return message


class ReadKauflandBasicData(BaseOperator):
    #ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.kauflandExtractor = getDataKaufland.KauflandExtractor()

    def execute(self, context):
        message = "Reading basic information"
        self.kauflandExtractor.etlBasicInfo()
        print(message)
        return message


class ReadKauflandDetailedData(BaseOperator):
    #ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.kauflandExtractor = getDataKaufland.KauflandExtractor()

    def execute(self, context):
        message = "Reading detailed information"
        self.kauflandExtractor.etlDetailedInfo()
        print(message)
        return message