import os
from configparser import ConfigParser

from enum import Enum


class PreferencesException(Exception):
    pass


class Config(object):
    def __init__(self, section, option):
        self._section = section
        self._option = option

    @property
    def section(self):
        return self._section

    @property
    def option(self):
        return self._option


class ConfigLoader(object):
    def __init__(self, file_path):
        self._config = ConfigParser()
        test_config_path = os.path.abspath(file_path)

        if not os.path.exists(test_config_path):
            raise PreferencesException(test_config_path, " file not found")
        self._config.read(test_config_path)

    def get(self, config, section=None, option=None):
        if isinstance(config, Enum):
            return self._config.get(config.value.section, config.value.option)
        elif section and option:
            self._config.get(section, option)
        else:
            raise PreferencesException(
                "Unable to read data for provided input: config = {c}, section = {s}, option = {o}".format(c=config,
                                                                                                           s=section,
                                                                                                           o=option))


_section_default = "DEFAULT"
_section_url = "URL"
_section_hpz = "HPZ"
_section_uat = "UAT"
_section_edware = "EDWARE"
_section_tsb = "TSB"

_preferences = ConfigLoader("test.ini")


def preferences(config):
    return _preferences.get(config)


class Edware(Enum):
    report_dir = Config(_section_edware, "report_dir")
    db_schema_name = Config(_section_edware, "db_schema_name")
    db_edauth_schema_name = Config(_section_edware, "db_edauth_schema_name")
    db_stats_main_url = Config(_section_edware, "db_stats_main_url")
    db_stats_schema = Config(_section_edware, "db_stats_schema")
    db_main_url = Config(_section_edware, "db_main_url")
    db_edauth_main_url = Config(_section_edware, "db_edauth_main_url")


class Default(Enum):
    host = Config(_section_default, "host")
    port = Config(_section_default, "port")

    tbs_host = Config(_section_default, "tsb_host")
    tbs_port = Config(_section_default, "tsb_port")

    hpz_host = Config(_section_default, "hpz_host")
    hpz_port = Config(_section_default, "hpz_port")

    idp = Config(_section_default, "idp")
    idp_host = Config(_section_default, "idp_oauth")

    downloads_path = Config(_section_default, "downloads_path")
    unzipped_path = Config(_section_default, "unzipped_path")


class HPZ(Enum):
    registration_endpoint = Config(_section_hpz, "registration_endpoint")
    files_endpoint = Config(_section_hpz, "files_endpoint")
    config_file_location = Config(_section_hpz, "config_file_location")
    cleanup_script_relative_location = Config(_section_hpz, "cleanup_script_relative_location")
    db_main_url = Config(_section_hpz, "db_main_url")
    db_registration_table = Config(_section_hpz, "db_registration_table")
    db_schema_name = Config(_section_hpz, "db_schema_name")
    uploads_directory = Config(_section_hpz, "uploads_direcory")


class URL(Enum):
    individual_student = Config(_section_url, "individual_student")
    list_of_students = Config(_section_url, "list_of_students")
    list_of_grades = Config(_section_url, "school_view_sds")
    list_of_schools_sds = Config(_section_url, "district_view_sds")
    landing_page = Config(_section_url, "landing_page")
    state_view_vt_tenant = Config(_section_url, "state_view_vt_tenant")
    state_view_ca_tenant = Config(_section_url, "state_view_ca_tenant")
    state_view_sds_public_report = Config(_section_url, "state_view_sds_public_report")
    state_view_sds = Config(_section_url, "state_view_sds")


class TSB(Enum):
    csv = Config(_section_tsb, 'smarter_score_batcher.base_dir.csv')
    staging = Config(_section_tsb, 'smarter_score_batcher.base_dir.staging')
    working = Config(_section_tsb, 'smarter_score_batcher.base_dir.working')
    xml = Config(_section_tsb, 'smarter_score_batcher.base_dir.xml')
