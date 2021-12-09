"""
DELL SDP P-Search API Demo.
"""
import logging
import os
import json

# Constants
BASE_CONFIG = 'BASE'                                          # Base Configuration Section
SDP_REST_HEAD_CONFIGURATION = 'SDP_REST_HEAD'                 # SDP Configuration Section


class InvalidConfigurationException(Exception):
    pass


class DellSDPConfiguration(object):
    def __init__(self, config, tempdir):

        if config is None:
            raise InvalidConfigurationException("No file path to the DELL SDP P-Search DEMO configuration provided")

        if not os.path.exists(config):
            raise InvalidConfigurationException("The DELL SDP P-Search DEMO configuration "
                                                "file path does not exist: " + config)
        if tempdir is None:
            raise InvalidConfigurationException("No path for temporary file storage provided")

        # Store temp file storage path to the configuration object
        self.tempfilepath = tempdir

        # Attempt to open configuration file
        try:
            with open(config, 'r') as f:
                parser = json.load(f)
        except Exception as e:
            raise InvalidConfigurationException("The following unexpected exception occurred in the "
                                                "DELL SDP P-Search DEMO Module attempting to parse "
                                                "the configuration file: " + e.message)

        # Set logging level
        logging_level_raw = parser[BASE_CONFIG]['logging_level']
        self.logging_level = logging.getLevelName(logging_level_raw.upper())

        # Grab SDP settings and validate
        self.sdp_rest_api_host_protocol = parser[SDP_REST_HEAD_CONFIGURATION]['sdp_rest_api_host_protocol']
        self.sdp_rest_api_host = parser[SDP_REST_HEAD_CONFIGURATION]['sdp_rest_api_host']
        self.sdp_rest_api_port = parser[SDP_REST_HEAD_CONFIGURATION]['sdp_rest_api_port']
        self.sdp_rest_api_key = parser[SDP_REST_HEAD_CONFIGURATION]['sdp_rest_api_key']
        self.sdp_auth_credentials = parser[SDP_REST_HEAD_CONFIGURATION]['sdp_auth_credentials']
        self.sdp_index_to_search = parser[SDP_REST_HEAD_CONFIGURATION]['sdp_index_to_search']

        # Validate SDP settings
        if not self.sdp_rest_api_host_protocol:
            raise InvalidConfigurationException("The DELL SDP Rest API Endpoint Protocol is not configured in the module configuration")
        else:
            if self.sdp_rest_api_host_protocol not in ['http', 'https']:
                raise InvalidConfigurationException(
                "The DELL SDP Rest API Endpoint Protocol can be only one of ['http', 'https']")
        if not self.sdp_rest_api_host:
            raise InvalidConfigurationException("The DELL SDP Rest API Endpoint Host is not configured in the module configuration")
        if not self.sdp_rest_api_port:
            raise InvalidConfigurationException("The DELL SDP Rest API Endpoint Port is not configured in the module configuration")
        if not self.sdp_rest_api_key:
            raise InvalidConfigurationException("The DELL SDP Rest API key is not configured in the module configuration")
        if not self.sdp_auth_credentials:
            raise InvalidConfigurationException("The DELL SDP Rest API credentials are not configured in the module configuration")
        if not self.sdp_index_to_search:
            raise InvalidConfigurationException("The DELL SDP Rest API index to search is not configured in the module configuration")

        # Validate logging level
        if logging_level_raw not in ['debug', 'info', 'warning', 'error']:
            raise InvalidConfigurationException(
                "Logging level can be only one of ['debug', 'info', 'warning', 'error']")

