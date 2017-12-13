# -*- coding:utf-8 -*-
# Copyright 2017 Gridsum, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


__author__ = "Dake Wang"

from rrd import app
from rrd import config
from flask import render_template,request,g,jsonify
from rrd.model.portal.ignore import Ignore
from rrd.model.portal.ign_host import Ign_host
from rrd.model.portal.ign_group import Ign_group
from rrd.service import ignore_service

from rrd.utils.logger import logging
log = logging.getLogger(__file__)

@app.route('/portal/ignore', methods=["GET"])
def ignore_get():
    page = int(request.args.get('p', 1))
    limit = int(request.args.get('limit', 10))
    query = request.args.get('q', '').strip()
    mine = request.args.get('mine', '1')
    me = g.user.name if mine == '1' else None
    vs, total = Ignore.query(page, limit, query, me)
    log.debug(vs)
    return render_template(
        'portal/ignore/index.html',
        data={
            'vs': vs,
            'total': total,
            'query': query,
            'limit': limit,
            'page': page,
            'mine': mine,
            'is_root': g.user.name in config.MAINTAINERS,
        }
    )

@app.route('/portal/ignore/add', methods = ['POST'])
def add_ignore():
    metric = request.form['ignore_name'].strip()
    if not metric:
        return jsonify(msg="metric is blank")

    ignore_id = Ignore.create(metric, g.user.name)
    if ignore_id > 0:
        return jsonify(msg='')
    else:
        return jsonify(msg='ignore_name has already existent')

@app.route('/portal/ignore/delete/<ignore_id>')
def del_ignore(ignore_id):
    ignore_id = int(ignore_id)
    metric = Ignore.read(where='id = %s', params=[ignore_id])
    if not metric:
        return jsonify(msg='no such ignore expression')

    if not metric.writable(g.user):
        return jsonify(msg='no permission')

    return jsonify(msg=ignore_service.delete_ignore(ignore_id))

@app.route('/portal/ignore/update/<ignore_id>',methods=['POST'])
def upd_ignore(ignore_id):
    ignore_id = int(ignore_id)
    new_name = request.form['new_name'].strip()
    if not new_name:
        return jsonify(msg='new expression is blank')

    ignore = Ignore.read(where='id = %s', params=[ignore_id])
    if not ignore:
        return jsonify(msg='no such ignore expression')

    if not ignore.writable(g.user):
        return jsonify(msg='no permission')

    Ignore.update_dict({'ignore_name': new_name}, 'id=%s', [ignore_id])
    return jsonify(msg='')

@app.route('/portal/ignore/host/<ignore_id>')
def ignore_host_list(ignore_id):
    ignore_id = int(ignore_id)
    ignore = Ignore.read(where='id = %s',params=[ignore_id])

    if not ignore:
        return jsonify(msg="no such ignore metric expression")

    ts = Ign_host.host_list(ignore_id)

    return render_template('portal/ignore/hosts.html', ignore=ignore, ts=ts)

@app.route('/portal/ignore/group/<ignore_id>')
def ignore_group_list(ignore_id):
    ignore_id = int(ignore_id)
    ignore = Ignore.read(where='id = %s', params=[ignore_id])

    if not ignore:
        return jsonify(msg="no such ignore metric expression")

    ts = Ign_group.group_list(ignore_id)

    return render_template('portal/ignore/groups.html', ignore=ignore, ts=ts)

@app.route('/portal/ignore/unbind/host')
def ignore_unbind_host():
    ignore_id = request.args.get('ignore_id','')
    host_id = request.args.get('host_id','')
    if not ignore_id:
        return jsonify(msg='ignore_id is blank')

    if not host_id:
        return jsonify(msg='host_id is blank')

    Ign_host.unbind_host(ignore_id, host_id)
    return jsonify(msg='')

@app.route('/portal/ignore/bind/host')
def ignore_bind_host():
    ignore_id = request.args.get('ignore_id','').strip()
    host_id = request.args.get('host_id','').strip()
    if not ignore_id:
        return jsonify(msg='ignore_id is blank')

    if not host_id:
        return jsonify(msg='host_id is blank')

    Ign_host.bind_host(ignore_id, host_id, g.user.name)
    return jsonify(msg='')

@app.route('/portal/ignore/unbind/group')
def ignore_unbind_group():
    ignore_id = request.args.get('ignore_id','')
    group_id = request.args.get('group_id','')
    if not ignore_id:
        return jsonify(msg='ignore_id is blank')

    if not group_id:
        return jsonify(msg='group_id is blank')

    Ign_group.unbind_group(ignore_id, group_id)
    return jsonify(msg='')

@app.route('/portal/ignore/bind/group')
def ignore_bind_group():
    ignore_id = request.args.get('ignore_id','').strip()
    group_id = request.args.get('group_id','').strip()
    if not ignore_id:
        return jsonify(msg='ignore_id is blank')

    if not group_id:
        return jsonify(msg='group_id is blank')

    Ign_group.bind_group(ignore_id, group_id, g.user.name)
    return jsonify(msg='')




