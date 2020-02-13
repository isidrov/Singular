#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from lxml import etree
import zeep.helpers
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport
from zeep.cache import SqliteCache
from zeep import Client
from zeep.exceptions import Fault
import logging
from requests.exceptions import  HTTPError,Timeout
from requests.exceptions import ConnectionError, RetryError
import json
from xml.dom.minidom import parseString
from tabulate import tabulate
import time
from zeep.plugins import HistoryPlugin
from PyQt5.QtWidgets import  QApplication, QTreeWidget, QTreeWidgetItem

class sql_decoder:

    @classmethod
    def serialize_expand(cls,result):
        """
        Serialize result and expand etree Elements
        Zeep may return _Element for SOAP anyType
        :param result: zeep Client response
        :return: serialized results
        """
        # Small helper to recursively return dict of dicts for nested XML
        def recursive_dict(element):
            if len(element) > 0:
                return {element.tag: recursive_dict(child) or element.text for child in element}
            else:
                return {element.tag: element.text}

        serialized_result = zeep.helpers.serialize_object(result)
        if isinstance(serialized_result, etree._Element):
            return recursive_dict(serialized_result)
        elif isinstance(serialized_result, list):
            return [cls.serialize_expand(i) for i in serialized_result]
        elif isinstance(serialized_result, dict):
            return {k:cls.serialize_expand(v) for k,v in serialized_result.items()}
        else:
            return serialized_result

    def decode_all(self):
        pass


    def unnest_list(self,decoded_list):
        """
                convert list of list of dicts resulted by zeep executeSQL
                intolist of dicts which is returned
                """
        n = len(decoded_list)
        p = 0
        final_list = []

        while p < n:
            dicta = dict()
            for i in decoded_list[p]:
                dicta.update(i)
            p = p + 1
            final_list.append(dicta)
        return final_list



def get_ucm_imp_subs(cluster_info):

    sub_info = [d for d in cluster_info if d['type'] != 'cluster.node.type.primary']

    return sub_info





class ViewTree(QTreeWidget):
    def __init__(self, value):
        super().__init__()
        def fill_item(item, value):
            def new_item(parent, text, val=None):
                child = QTreeWidgetItem([text])
                fill_item(child, val)
                parent.addChild(child)
                child.setExpanded(True)
            if value is None: return
            elif isinstance(value, dict):
                for key, val in sorted(value.items()):
                    new_item(item, str(key), val)
            elif isinstance(value, (list, tuple)):
                for val in value:
                    text = (str(val) if not isinstance(val, (dict, list, tuple))
                            else '[%s]' % type(val).__name__)
                    new_item(item, text, val)
            else:
                new_item(item, str(value))

        fill_item(self.invisibleRootItem(), value)



def calc_sha512(file_path):

    import hashlib


    # Open,close, read file and calculate SHA512 on its contents

    with open(file_path, 'rb') as file_to_check:
        # read contents of the file
        data = file_to_check.read()
        # pipe contents of the file through
        sha512 = hashlib.sha512(data).hexdigest()

    # Finally return hash
    return sha512