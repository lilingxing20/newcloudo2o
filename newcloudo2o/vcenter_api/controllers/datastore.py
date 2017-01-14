# Copyright 2016 OpenStack Foundation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


from pecan import expose
from pecan import request
from pecan import response
from pecan import rest

from oslo_log import log as logging
from oslo_serialization import jsonutils

from newcloudo2o.common import constants as cons
import newcloudo2o.common.context as t_context
from newcloudo2o.common import httpclient as hclient
from newcloudo2o.common.i18n import _
from newcloudo2o.common.i18n import _LE
from newcloudo2o.common import utils
import newcloudo2o.db.api as db_api

LOG = logging.getLogger(__name__)


class DatastoreController(rest.RestController):

    def __init__(self, tenant_id):
        self.tenant_id = tenant_id

    @expose(generic=True, template='json')
    def post(self, **kw):
        print 'post-' * 100, "\n"
        print kw
        return None

    @expose(generic=True, template='json')
    def get_one(self):
        """Get datacenter info."""
        print 'get_one-' * 100, "\n"
        print kw
        return None

    @expose(generic=True, template='json')
    def get_all(self):
        print "get_all-" * 100, "\n"
        print kw
        return None

    @expose(generic=True, template='json')
    def put(self, **kw):
        """Update """
        print 'put-' * 100, "\n"
        return None

    @expose(generic=True, template='json')
    def delete(self, key):
        """Delete the given metadata item from a volume."""
        print 'delete-' * 100, "\n"
        print key, "\n"
        return None


class DcDatastoreController(rest.RestController):

    def __init__(self, tenant_id, dc_name):
        self.tenant_id = tenant_id
        self.dc_name = dc_name

    @expose(generic=True, template='json')
    def post(self, **kw):
        print 'post-' * 100, "\n"
        return None

    @expose(generic=True, template='json')
    def get_one(self):
        """Get datacenter info."""
        print 'get_one-' * 100, "\n"
        return None

    @expose(generic=True, template='json')
    def get_all(self):
        print "get_all-" * 100, "\n"
        return None

    @expose(generic=True, template='json')
    def put(self, **kw):
        """Update """
        print 'put-' * 100, "\n"
        return None

    @expose(generic=True, template='json')
    def delete(self, key):
        """Delete the given metadata item from a volume."""
        print 'delete-' * 100, "\n"
        print key, "\n"
        return None


class HostDatastoreController(rest.RestController):

    def __init__(self, tenant_id, host_name):
        self.tenant_id = tenant_id
        self.host_name = host_name

    @expose(generic=True, template='json')
    def post(self, **kw):
        print 'post-' * 100, "\n"
        return None

    @expose(generic=True, template='json')
    def get_one(self):
        """Get datacenter info."""
        print 'get_one-' * 100, "\n"
        return None

    @expose(generic=True, template='json')
    def get_all(self):
        print "get_all-" * 100, "\n"
        return None

    @expose(generic=True, template='json')
    def put(self, **kw):
        """Update """
        print 'put-' * 100, "\n"
        return None

    @expose(generic=True, template='json')
    def delete(self, key):
        """Delete the given metadata item from a volume."""
        print 'delete-' * 100, "\n"
        print key, "\n"
        return None
