from Insurance.logger import logging
from Insurance.exception import InsuranceException
from Insurance.utils import get_collection_as_dataframe
import sys, os


if __name__=="__main__":
    try:
        get_collection_as_dataframe(database_name="INSURANCE",collection_name="INSURANCE_PROJECT")
    except Exception as e:
        print(e)