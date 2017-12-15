# -*- coding:utf-8 -*-

import requests
from rrd.service import god_sync_service
from rrd import app
from rrd.utils.logger import logging
from rrd.model.portal.host import Host
from rrd.model.portal.god_host import God_host
log = logging.getLogger(__file__)

from flask import jsonify,render_template,request

class God():
    def __init__(self,hostname,ip,ips,status):
        self.hostname = hostname
        self.ip = ip
        self.ips = ips
        self.status = status

@app.route('/god/god_sync', methods=["GET"])
def god_sync():
    result = god_sync_service.sync_server()
    return jsonify(msg=result)

@app.route("/god/server_status")
def server_info():
    product = request.args.get('product','OPS')
    ret = []
    dict = Host.all_host_ip_dict()
    product_host_dict = God_host.product_host_dict(product)
    products = product_list()
    for i in product_host_dict:
        if i in dict:
            status = detect_status(dict[i])
            ins = God(i, dict[i], product_host_dict[i], status)
            ret.append(ins)
        else:
            status = "not be installed"
            ins = God(i, "", product_host_dict[i], status)
            ret.append(ins)

    return render_template(
        'portal/god/index.html',
        data={
            'products': products,
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
    return "dead"

def product_list():
    product = God_host.all_product()
    return product