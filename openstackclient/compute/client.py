#   Copyright 2012-2013 OpenStack, LLC.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

import logging

from openstackclient.common import utils

LOG = logging.getLogger(__name__)

API_NAME = 'compute'
API_VERSIONS = {
    '1.1': 'novaclient.v1_1.client.Client',
    '2': 'novaclient.v1_1.client.Client',
}


def make_client(instance):
    """Returns a compute service client."""
    compute_client = utils.get_client_class(
        API_NAME,
        instance._api_version[API_NAME],
        API_VERSIONS)
    LOG.debug('instantiating compute client: %s' % compute_client)
    client = compute_client(
        username=instance._username,
        api_key=instance._password,
        project_id=instance._project_name,
        auth_url=instance._auth_url,
        cacert=instance._cacert,
        insecure=instance._insecure,
        region_name=instance._region_name,
        # FIXME(dhellmann): get endpoint_type from option?
        endpoint_type='publicURL',
        # FIXME(dhellmann): add extension discovery
        extensions=[],
        service_type=API_NAME,
        # FIXME(dhellmann): what is service_name?
        service_name='')

    # Populate the Nova client to skip another auth query to Identity
    if instance._url:
        # token flow
        client.client.management_url = instance._url
    else:
        # password flow
        client.client.management_url = instance.get_endpoint_for_service_type(
            API_NAME)
        client.client.service_catalog = instance._service_catalog
    client.client.auth_token = instance._token
    return client
