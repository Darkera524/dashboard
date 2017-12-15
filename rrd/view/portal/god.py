# -*- coding:utf-8 -*-

import requests
from rrd.service import god_sync_service
from rrd import app
from rrd.utils.logger import logging
from rrd.model.portal.host import Host
log = logging.getLogger(__file__)

from flask import jsonify,render_template

class God():
    def __init__(self,hostname,status):
        self.hostname = hostname
        self.status = status

@app.route('/god/god_sync', methods=["GET"])
def god_sync():
    result = god_sync_service.sync_server()
    return jsonify(msg=result)

@app.route("/god/server_status")
def server_info():
    ret = []
    dict = Host.all_host_dict()
    for i in dict:
        status = detect_status(dict[i])
        ins = God(i,status)
        ret.append(ins)
    return render_template(
        'portal/god/index.html',
        data={
            'vs': ret,
        }
    )

def detect_status(ip):
    agent_api = "http://" + ip + ":1988/health"
    try:
        r = requests.get(agent_api)
        response = r.text
        if response == "ok":
            return "active"
    except Exception,e:
        log.error(e)
        return "dead"
    return "active"