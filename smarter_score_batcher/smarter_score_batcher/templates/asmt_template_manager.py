'''
Created on Sep 19, 2014

@author: agrebneva
'''
from smarter_score_batcher.celery import conf
import os
import json
from smarter_score_batcher.exceptions import MetadataException
from zope import interface, component
from zope.interface.declarations import implementer
from pyramid.threadlocal import get_current_registry


class MetadataTemplate:
    '''
    A single template for an asmt
    '''
    def __init__(self, asmt_data_json):
        self.asmt_data_json = asmt_data_json

    def get_asmt_metadata_template(self):
        return self.asmt_data_json

    def get_asmt_subject(self):
        return self.asmt_data_json['Identification']['Subject']


class IMetadataTemplateManager(interface.Interface):
    def get_template(self, subject):
        pass


@implementer(IMetadataTemplateManager)
class MetadataTemplateManager:
    '''
    Loads and manages asmt templates by asmt SUBJECT
    '''
    def __init__(self):
        self.templates = {}
        # TODO: fix this
        if conf is None or not conf:
            # maybe service is eager mode. If so, read from registry
            settings = get_current_registry().settings
            if settings is not None:
                global conf
                conf = settings
        here = os.path.abspath(os.path.dirname(__file__))
        asmt_meta_location = os.path.join(here, conf.get('smarter_score_batcher.resources.path', '../../resources/'))
        for file in os.listdir(asmt_meta_location):
            if file.endswith(".static_asmt_metadata.json"):
                full_path = os.path.join(asmt_meta_location, file)
                with open(full_path, 'r+') as f:
                    sm = MetadataTemplate(json.load(f))
                    subject = sm.get_asmt_subject()
                    self.templates[subject.lower()] = sm

    def get_template(self, subject):
        sm = self.templates.get(subject.lower())
        if sm is None:
            raise MetadataException("Unable to load metadata for subject {0}".format(subject))
        return sm.asmt_data_json.copy()

component.provideUtility(MetadataTemplateManager(), IMetadataTemplateManager)
