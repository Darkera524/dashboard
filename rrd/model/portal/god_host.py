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


__author__ = 'Dake Wang'
from .bean import Bean
from rrd.store import db

class God_host(Bean):
    _tbl = "god"
    _cols = "id, product, hostname, lev, idc, ips"

    def __init__(self, _id, product, hostname, lev, idc, ips):
        self.id = _id
        self.product = product
        self.hostname = hostname
        self.lev = lev
        self.idc = idc
        self.ips = ips

    def to_json(self):
        return {
            "id": self.id,
            "product": self.product,
            "hostname": self.hostname,
            "lev": self.lev,
            "idc": self.idc,
            "ips": self.ips,
        }

    @classmethod
    def product_host_dict(cls, product):
        sql = "SELECT hostname,ips FROM god WHERE product = '" + product + "'"
        rows = db.query_all(sql)
        ret = {}
        if rows:
            for row in rows:
                ret[row[0]] = row[1].strip()
        return ret

    @classmethod
    def all_product(cls):
        ret = []
        sql = "SELECT distinct product FROM god"
        rows = db.query_all(sql)
        if rows:
            for row in rows:
                ret.append(row[0])
        return ret

    @classmethod
    def lev_host_dict(cls, lev):
        sql = "SELECT hostname,ips FROM god WHERE lev = '" + lev + "'"
        rows = db.query_all(sql)
        ret = {}
        if rows:
            for row in rows:
                ret[row[0]] = row[1].strip()
        return ret

    @classmethod
    def idc_host_dict(cls, idc):
        sql = "SELECT hostname,ips FROM god WHERE idc = '" + idc + "'"
        rows = db.query_all(sql)
        ret = {}
        if rows:
            for row in rows:
                ret[row[0]] = row[1].strip()
        return ret