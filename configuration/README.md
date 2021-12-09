# dell-sdp-psearch-demo configuration
----------------------------------------------------------------------------------------------
dell-sdp-psearch-demo is a PYTHON application that demonstrates using DELL's
Streaming Data Platform (SDP) P-Search API to query object in a searchable stream
----------------------------------------------------------------------------------------------

The demo uses a configuration file that allows the user to pre-configure:
- The REST API Endpoint for the SDP cluster
- The BASE64 encoded credential used to perform Basic authentication with each API call

the ECS where the STS API calls will be made

We've provided a sample configuration file:

- ecs_saml_demo_config.sample: Change file suffix from .sample to .json and configure as needed
  This contains the tool configuration for ECS and database connection, logging level, etc. Here
  is the sample configuration:
  
  `BASE`:
  
      logging_level - The default is "info" but it can be set to "debug" to generate a LOT of details

  `SDP_REST_HEAD`:
      
      sdp_rest_api_host_protocol = This is the protocol of the SDP P-search API (http or https)
      sdp_rest_api_host = This is the FQDN of the SDP P-search API endpoint
      sdp_rest_api_port = This is the Port of the SDP P-search API endpoint
      sdp_rest_api_key = This is the API Key of the SDP P-search API endpoint
      sdp_auth_credentials = This is the credentials for the SDP P-search API endpoint (user:password
      sdp_index_to_search = This is the index of the SDP P-search searchable stream to search on
