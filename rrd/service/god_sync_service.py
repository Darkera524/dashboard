#coding=utf-8

__author__ = 'Dake Wang'

import requests
import json
from rrd.store import db
from rrd.utils.logger import logging
log = logging.getLogger(__file__)

def sync_server():
    try:
        cursor = db.execute('delete from god')

        db.commit()
    except Exception, e:
        log.error(e)
        db.rollback()
        return 'delete god %s fail'
    finally:
        cursor and cursor.close()

    urlto = "http://god.gridsum.com/api/v1/assets/server?size=10000&asset_status=正常运行"
    r = requests.get(urlto)
    response = r.text

    all_server = json.loads(response)["items"]
    for item in all_server:
        product = item["_source"]["asset"]["product"]
        hostname = item["_source"]["logical"]["host_name"]
        lev = "product"
        if item["_source"]["asset"]["level"] == "test":
            lev = "test"
        idc = ""
        if item["_source"]["asset"]["idc"] == "TianTan":
            idc = "TianTan"
        elif item["_source"]["asset"]["idc"] == "GuoMao":
            idc = "GuoMao"
        elif item["_source"]["asset"]["idc"] == "YiZhuang":
            idc = "YiZhuang"
        elif item["_source"]["asset"]["idc"] == "ShangHai":
            idc = "ShangHai"
        ip_list = item["_source"]["logical"]["ip_list"]
        ips = []
        for ip in ip_list:
            ips.append(ip["ip_address"])
        ip_str = ",".join(ips)

        try:
            cursor = db.execute("insert into god(product, hostname, lev, idc, ips) values (%s, %s, %s, %s, %s)" , ((product,hostname,lev,idc,ip_str)))
            db.commit()
        except Exception, e:
            log.error(e)
            db.rollback()
            return str(e)
        finally:
            cursor and cursor.close()

    return ""


if __name__ == '__main__':
    sync_server()