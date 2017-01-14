# Copyright (c) 2015 Huawei Tech. Co., Ltd.
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

import pecan
from pecan import hooks

import oslo_log.log as logging
import webob.exc as web_exc

from newcloudo2o.vcenter_api.controllers import datacenter
from newcloudo2o.vcenter_api.controllers import datastore
from newcloudo2o.vcenter_api.controllers import network
from newcloudo2o.vcenter_api.controllers import esxi
from newcloudo2o.vcenter_api.controllers import vm
from newcloudo2o.vcenter_api.controllers import server
from newcloudo2o.vcenter_api.controllers import server_action


LOG = logging.getLogger(__name__)


class ErrorHook(hooks.PecanHook):
    def on_error(self, state, exc):
        if isinstance(exc, web_exc.HTTPException):
            exc.body = ''
            return exc


class RootController(object):

    @pecan.expose()
    def _lookup(self, version, *remainder):
        if version == 'v2':
            return V2Controller(), remainder


class V2Controller(object):

    _media_type1 = "application/vnd.openstack.volume+xml;version=1"
    _media_type2 = "application/vnd.openstack.volume+json;version=1"

    def __init__(self):

        self.resource_controller = {
            'datacenters': datacenter.DatacenterController,
            'datastores': datastore.DatastoreController,
            'hosts': esxi.EsxiController,
            'networks': network.NetworkController,
            'vms': vm.VmController,
            'servers': server.ServerController
        }

        self.datacenters_sub_controller = {
            'datastores': datastore.DcDatastoreController,
            'hosts': esxi.DcEsxiController,
            'networks': network.DcNetworkController,
            'vms': vm.DcVmController
        }
        self.datastores_sub_controller = {
            'hosts': esxi.DsEsxiController,
            'vms': vm.DsVmController
        }
        self.hosts_sub_controller = {
            'datastores': datastore.HostDatastoreController,
            'networks': network.HostNetworkController,
            'vms': vm.HostVmController
        }
        self.server_sub_controller = {
            'action': server_action.ServerActionController
        }


    @pecan.expose()
    def _lookup(self, tenant_id, *remainder):
        if not remainder:
            pecan.abort(404)
            return
        resource = remainder[0]
        if resource not in self.resource_controller:
            pecan.abort(404)
            return
        if resource == 'datacenters' and len(remainder) >= 3:
            dc_name = remainder[1]
            sub_resource = remainder[2]
            if sub_resource not in self.datacenters_sub_controller:
                pecan.abort(404)
                return
            return self.datacenters_sub_controller[sub_resource](
                tenant_id, dc_name), remainder[3:]
        elif resource == 'datastores' and len(remainder) >= 3:
            ds_name = remainder[1]
            sub_resource = remainder[2]
            if sub_resource not in self.datastores_sub_controller:
                pecan.abort(404)
                return
            return self.datastores_sub_controller[sub_resource](
                tenant_id, ds_name), remainder[3:]
        elif resource == 'hosts' and len(remainder) >= 3:
            host_name = remainder[1]
            sub_resource = remainder[2]
            if sub_resource not in self.hosts_sub_controller:
                pecan.abort(404)
                return
            return self.hosts_sub_controller[sub_resource](
                tenant_id, host_name), remainder[3:]
        elif resource == 'servers' and len(remainder) >= 3:
            server_id = remainder[1]
            sub_resource = remainder[2]
            if sub_resource not in self.server_sub_controller:
                pecan.abort(404)
                return
            return self.server_sub_controller[sub_resource](
                tenant_id, server_id), remainder[3:]
        return self.resource_controller[resource](tenant_id), remainder[1:]

    @pecan.expose(generic=True, template='json')
    def index(self):
        return {
            "version": {
                "status": "CURRENT",
                "updated": "2012-11-21T11:33:21Z",
                "media-types": [
                    {
                        "base": "application/xml",
                        "type": self._media_type1
                    },
                    {
                        "base": "application/json",
                        "type": self._media_type2
                    }
                ],
                "id": "v2.0",
                "links": [
                    {
                        "href": pecan.request.application_url + "/v2/",
                        "rel": "self"
                    },
                    {
                        "href": "http://docs.openstack.org/",
                        "type": "text/html",
                        "rel": "describedby"
                    }
                ]
            }
        }

    @index.when(method='POST')
    @index.when(method='PUT')
    @index.when(method='DELETE')
    @index.when(method='HEAD')
    @index.when(method='PATCH')
    def not_supported(self):
        pecan.abort(405)
