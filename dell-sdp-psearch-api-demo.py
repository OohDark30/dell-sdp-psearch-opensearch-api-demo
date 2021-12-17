"""
DELL SDP P-Search API Demo.
"""
import datetime
import json
from configuration.dell_sdp_psearch_demo import DellSDPConfiguration
from logger import sdp_logger
from sdp.sdp import SDPApi
import os
import traceback
import logging
from opensearchpy import OpenSearch
import pprint

# Constants
MODULE_NAME = "SDP_PSEARCH_API_DEMO_Module"  # Module Name
INTERVAL = 30  # In seconds
CONFIG_FILE = 'dell_sdp_psearch_demo.json'  # Default Configuration File

# Globals
_configuration = None
_logger = None
_sdpRestEndpoint = None
_sdpRestCredential = None
_sdpAPI = None


def sdp_config(config, temp_dir):
    global _configuration
    global _logger

    try:
        # Load and validate module configuration
        _configuration = DellSDPConfiguration(config, temp_dir)

        # Grab loggers and log status
        _logger = sdp_logger.get_logger(__name__, _configuration.logging_level)
        _logger.info(MODULE_NAME + '::sdp_config()::We have configured logging level to: '
                     + logging.getLevelName(str(_configuration.logging_level)))
        _logger.info(MODULE_NAME + '::sdp_config()::Configuring DELL SDP P-Search API Demo Module complete.')
        return _logger
    except Exception as e:
        _logger.error(MODULE_NAME + '::sdp_config()::The following unexpected exception occured: ' + str(e) + "\n" + traceback.format_exc())


"""
Main 
"""
if __name__ == "__main__":

    try:
        # Dump out application path
        currentApplicationDirectory = os.getcwd()
        configFilePath = os.path.abspath(os.path.join(currentApplicationDirectory, "configuration", CONFIG_FILE))
        tempFilePath = os.path.abspath(os.path.join(currentApplicationDirectory, "temp"))

        # Create temp directory if it doesn't already exists
        if not os.path.isdir(tempFilePath):
            os.mkdir(tempFilePath)
        else:
            # The directory exists so lets scrub any temp XML files out that may be in there
            files = os.listdir(tempFilePath)
            for file in files:
                if file.endswith(".xml"):
                    os.remove(os.path.join(currentApplicationDirectory, "temp", file))

        print(MODULE_NAME + "::__main__::Current directory is : " + currentApplicationDirectory)
        print(MODULE_NAME + "::__main__::Configuration file path is: " + configFilePath)

        # Initialize configuration and VDC Lookup
        log_it = sdp_config(configFilePath, tempFilePath)

        # Create an OpenSearch Client
        sdp_host = "{0}://{1}@{2}:{3}".format(_configuration.sdp_rest_api_host_protocol, _configuration.sdp_auth_credentials, _configuration.sdp_rest_api_host, _configuration.sdp_rest_api_port)

        openSearchClient = OpenSearch(
            hosts=[sdp_host],
            http_compress=False,
            use_ssl=False
        )

        # Initialize API Instance
        _sdpAPI = SDPApi(openSearchClient,  _logger)

        # Grab cluster information
        info_json = _sdpAPI.get_sdp_cluster_info()
        print(MODULE_NAME + "::__main__::SDP P-Search Cluster Info:\r\n")
        pp1 = pprint.PrettyPrinter(width=41, indent=4, compact=True)
        pp1.pprint(info_json)

        # Get Cluster State
        state_json = _sdpAPI.get_sdp_cluster_state()
        print(MODULE_NAME + "::__main__::SDP P-Search Cluster State:\r\n")
        pp2 = pprint.PrettyPrinter(width=41, indent=4, compact=True)
        pp2.pprint(state_json)

        # Get our index to search
        indices_json = _sdpAPI.get_sdp_indices(_configuration.sdp_index_to_search)
        #print(MODULE_NAME + "::__main__::SDP P-Search Cluster Index Detail for Index: " + _configuration.sdp_index_to_search + "\r\n")
        #pp3 = pprint.PrettyPrinter(width=41, indent=4, compact=True)
        #pp3.pprint(indices_json)

        # Do a search of the index using a date range and a meta-data attribute
        query = {
            "query": {
                "bool": {
                    "must": [],
                    "filter": [
                        {
                            "match_all": {}
                        },
                        {
                            "match_phrase": {
                                "objectMetadata.usrMd.x-amz-meta-instrument": "instrument7"
                            }
                        },
                        {
                            "range": {
                                "objectMetadata.sysMd.size": {
                                    "gte": 400000,
                                    "lt": 699999
                                }
                            }
                        },
                        {
                            "match_phrase": {
                                "objectMetadata.sysMd.createTime": "2021-12-16T22:05:04.000Z"
                            }
                        },
                        {
                            "range": {
                                "objectMetadata.sysMd.createTime": {
                                    "gte": "2021-12-16T16:46:14.733Z",
                                    "lte": "2021-12-17T16:46:14.733Z",
                                    "format": "strict_date_optional_time"
                                }
                            }
                        }
                    ],
                    "should": [],
                    "must_not": []
                }
            }
        }

        search_results = _sdpAPI.search_sdp_index(query, _configuration.sdp_index_to_search)
        print(MODULE_NAME + "::__main__::SDP P-Search Search Results Against Index: " + _configuration.sdp_index_to_search )
        print("\tObject Keys Returned from Index " + _configuration.sdp_index_to_search +": ")

        # Do a little basic parsing to pull out and print the object key names
        search_results_hits = search_results['hits']['hits']
        for hit in search_results_hits:
            print("\t\tObject Key: " + hit['_source']['objectMetadata']['sysMd']['objectName'])

    except Exception as e:
        print(MODULE_NAME + '__main__::The following unexpected error occurred: '
              + str(e) + "\n" + traceback.format_exc())
