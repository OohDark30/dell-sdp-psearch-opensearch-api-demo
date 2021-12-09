"""
DELL SDP P-Search API
"""

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class SDPException(Exception):
    pass


class SDPApi(object):
    """
    SDP API Calls
    """

    def __init__(self, sdpclient, logger, response_json=None):
        self.ecs_authentication_failure = int('497')
        self.response_json = response_json
        self.logger = logger
        self.sdp_pravega_api_client = sdpclient
        self.response_xml_file = None

    def get_sdp_cluster_info(self):

        while True:
            r = self.sdp_pravega_api_client.info()

            # If we didn't get anything back there was a problem
            if r is None:
                self.logger.debug('SDPApi::get_sdp_cluster_info()::/ call did not return any data.')
                break
            else:
                self.response_json = r

                if type(self.response_json) is list:
                    self.logger.debug('SDPApi::get_sdp_cluster_info()::r.json() returned a list. ')
                elif type(self.response_json) is dict:
                    self.logger.debug('SDPApi::get_sdp_cluster_info()::r.json() returned a dictionary. ')
                else:
                    self.logger.debug('SDPApi::get_sdp_cluster_info()::r.json() returned unknown. ')

                break

        return self.response_json

    def get_sdp_cluster_state(self):

        while True:
            r = self.sdp_pravega_api_client.cluster.state()

            # If we didn't get anything back there was a problem
            if r is None:
                self.logger.debug('SDPApi::get_sdp_cluster_state()::/ call did not return any data.')
                break
            else:
                self.response_json = r

                if type(self.response_json) is list:
                    self.logger.debug('SDPApi::get_sdp_cluster_state()::r.json() returned a list. ')
                elif type(self.response_json) is dict:
                    self.logger.debug('SDPApi::get_sdp_cluster_state()::r.json() returned a dictionary. ')
                else:
                    self.logger.debug('SDPApi::get_sdp_cluster_state()::r.json() returned unknown. ')

                break

        return self.response_json

    def get_sdp_indices(self, index):

        while True:
            r = self.sdp_pravega_api_client.indices.get(index)

            # If we didn't get anything back there was a problem
            if r is None:
                self.logger.debug('SDPApi::get_sdp_indices()::/ call did not return any data.')
                break
            else:
                self.response_json = r

                if type(self.response_json) is list:
                    self.logger.debug('SDPApi::get_sdp_indices()::r.json() returned a list. ')
                elif type(self.response_json) is dict:
                    self.logger.debug('SDPApi::get_sdp_indices()::r.json() returned a dictionary. ')
                else:
                    self.logger.debug('SDPApi::get_sdp_indices()::r.json() returned unknown. ')

                break

        return self.response_json

    def search_sdp_index(self, query, index_name):

        while True:
            r = self.sdp_pravega_api_client.search(body=query, index=index_name)

            # If we didn't get anything back there was a problem
            if r is None:
                self.logger.debug('SDPApi::get_sdp_indices()::/ call did not return any data.')
                break
            else:
                self.response_json = r

                if type(self.response_json) is list:
                    self.logger.debug('SDPApi::get_sdp_indices()::r.json() returned a list. ')
                elif type(self.response_json) is dict:
                    self.logger.debug('SDPApi::get_sdp_indices()::r.json() returned a dictionary. ')
                else:
                    self.logger.debug('SDPApi::get_sdp_indices()::r.json() returned unknown. ')

                break

        return self.response_json

