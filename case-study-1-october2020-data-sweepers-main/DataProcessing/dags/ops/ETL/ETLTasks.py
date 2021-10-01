
import sys

sys.path.append('/opt/airflow')

from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults
from . import etl


class MergingDataSTG(BaseOperator):
    #ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.etl = etl.ETLProcess()

    def execute(self, context):
        message = "Merging data from vendors"
        self.etl.mergeData()
        print(message)
        return message


class DataCleaning(BaseOperator):
    #ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.etl = etl.ETLProcess()

    def execute(self, context):
        message = "Data Cleaning Process"
        self.etl.removeProductsWithoutPrice()
        self.etl.dataCleaning()
        print(message)
        return message




class CurrentProducts(BaseOperator):
    #ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.etl = etl.ETLProcess()

    def execute(self, context):
        message = "Moving Current Products"
        self.etl.moveCurrentProducts()
        print(message)
        return message


class MoveHistoricalData(BaseOperator):
    #ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.etl = etl.ETLProcess()

    def execute(self, context):
        message = "Move Historical Data"
        self.etl.moveHistoricalData()
        print(message)
        return message