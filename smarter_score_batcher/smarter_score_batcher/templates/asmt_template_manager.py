'''
Created on Sep 19, 2014

@author: agrebneva
'''
from smarter_score_batcher.celery import conf
import os
import json
from zope import interface, component
from zope.interface.declarations import implementer
import fnmatch
from smarter_score_batcher.utils.merge import deep_merge
from smarter_score_batcher.error.exceptions import MetadataException
from smarter_score_batcher.error.error_codes import ErrorSource


class MetadataTemplate:
    '''
    A single template for an asmt
    '''
    def __init__(self, asmt_data_json):
        self.asmt_data_json = asmt_data_json

    def get_asmt_metadata_template(self):
        return self.asmt_data_json.copy()

    def get_asmt_subject(self):
        return self.asmt_data_json['Identification']['Subject']


class IMetadataTemplateManager(interface.Interface):
    def get_template(self, key):
        pass


def get_template_key(year, asmt_type, grade, subject):
    return '_'.join([str(year), asmt_type, str(grade), subject])


class MetadataTemplateManager:
    '''
    Loads and manages asmt templates by asmt SUBJECT
    '''
    def __init__(self, asmt_meta_dir=None):
        self.templates = {}
        self.asmt_meta_location = self._get_template_location(asmt_meta_dir)
        self._load_templates(pattern='*.static_asmt_metadata.json', storer=self._store_by_subject)

    def _load_templates(self, pattern='.static_asmt_metadata.json', storer=None):
        for root, _, filenames in os.walk(self.asmt_meta_location):
            for file in fnmatch.filter(filenames, pattern):
                full_path = os.path.join(root, file)
                with open(full_path, 'r+') as f:
                    storer(root, MetadataTemplate(json.load(f)))

    def _store_by_subject(self, path, metadata_template):
        subject = metadata_template.get_asmt_subject()
        self.templates[subject.lower()] = metadata_template

    def _get_template_location(self, asmt_meta_location=None):
        if not asmt_meta_location is None and os.path.isabs(asmt_meta_location):
            return asmt_meta_location
        here = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(here, self._get_configured_path() if asmt_meta_location is None else asmt_meta_location)

    def _get_configured_path(self):
        return conf.get('smarter_score_batcher.metadata.static', '../../resources/meta/static')

    def get_template(self, key):
        sm = self.templates.get(key.lower())
        if sm is None:
            raise MetadataException("Unable to load metadata for subject {0}".format(key), err_source=ErrorSource.METADATATEMPLATEMANAGER_GET_TEMPLATE)
        return sm.get_asmt_metadata_template()


@implementer(IMetadataTemplateManager)
class PerfMetadataTemplateManager(MetadataTemplateManager):
    '''
    Loads and manages asmt templates by asmt SUBJECT
    '''
    def __init__(self, asmt_meta_dir=None, static_asmt_meta_dir=None):
        self.templates = {}
        self.asmt_meta_location = self._get_template_location(asmt_meta_dir)
        self.meta_template_mgr = MetadataTemplateManager(asmt_meta_dir=static_asmt_meta_dir)
        self._load_templates(pattern='*.json', storer=self._store)

    def _get_configured_path(self):
        return conf.get('smarter_score_batcher.metadata.static', '../../resources/meta/performance')

    def _store(self, path, metadata_template):
        key = path[len(self.asmt_meta_location) + 1:].replace(os.path.sep, '_')
        key = key + '_' + metadata_template.get_asmt_subject()
        self.templates[key.lower()] = MetadataTemplate(deep_merge(self.meta_template_mgr.get_template(metadata_template.get_asmt_subject()), metadata_template.get_asmt_metadata_template()))

component.provideUtility(PerfMetadataTemplateManager(), IMetadataTemplateManager)
