"""Pynamodb is similar to most ORMs in nature"""
import boto3
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, BooleanAttribute)

class Backend(Model):
    class Meta:
        # STAGE env always available in Zappa
        table_name = 'Backend'
        region = boto3.Session().region_name
        read_capacity_units = 1
        write_capacity_units = 1

    name = UnicodeAttribute(hash_key=True)
    description = UnicodeAttribute()
    credentials = UnicodeAttribute()
