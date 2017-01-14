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
from pecan import expose
from pecan import rest

from oslo_log import log as logging

import newcloudo2o.common.client as t_client
from newcloudo2o.common import constants
import newcloudo2o.common.context as t_context
from newcloudo2o.common.i18n import _
from newcloudo2o.common import utils
import newcloudo2o.db.api as db_api

LOG = logging.getLogger(__name__)


class ServerActionController(rest.RestController):

    def __init__(self, project_id, server_id):
        self.project_id = project_id
        self.server_id = server_id
        self.clients = {constants.TOP: t_client.Client()}
        self.handle_map = {
            'os-listServerSnapshot': self._handle_list_server_snapshot,
            'os-createServerSnapshot': self._handle_create_server_snapshot,
            'os-deleteServerSnapshot': self._handle_delete_server_snapshot,
            'os-restoreServerSnapshot': self._handle_restore_server_snapshot
        }

    def _handle_list_server_snapshot(self, context, body):
        print body
        return {"status_code": 200}, None

    def _handle_create_server_snapshot(self, context, body):
        print body
        return {"status_code": 200}, None

    def _handle_delete_server_snapshot(self, context, body):
        print body
        return {"status_code": 200}, None

    def _handle_restore_server_snapshot(self, context, body):
        print body
        return {"status_code": 200}, None


    @expose(generic=True, template='json')
    def post(self, **kw):
        print 'post-action_' * 100
        print kw
        context = t_context.extract_context_from_environ()

        action_handle = None
        action_type = None
        for _type in self.handle_map:
            if _type in kw:
                action_handle = self.handle_map[_type]
                action_type = _type
        if not action_handle:
            return utils.format_nova_error(
                400, _('Server action not supported'))

        try:
            resp, body = action_handle(context, kw)
            #pecan.response.status = resp.status_code
            pecan.response.status = resp.get('status_code')
            if not body:
                return pecan.response
            else:
                return body
        except Exception as e:
            code = 500
            message = _('Action %(action)s on server %(server_id)s fails') % {
                'action': action_type,
                'server_id': self.server_id}
            if hasattr(e, 'code'):
                code = e.code
            ex_message = str(e)
            if ex_message:
                message = ex_message
            LOG.error(message)
            return utils.format_nova_error(code, message)

