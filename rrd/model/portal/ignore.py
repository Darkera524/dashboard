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

from .bean import Bean

class Ignore(Bean):
    _tbl = 'ignore'
    _cols = 'id,ignore_name,creator'

    def __init__(self, _id, ignore_name, creator):
        self.id = _id
        self.ignore_name = ignore_name
        self.creator = creator

    def to_json(self):
        return {
            'id': self.id,
            'ignore_name': self.ignore_name,
            'creator': self.creator
        }

    @classmethod
    def query(cls, page, limit, query, me=None):
        where = ''
        params = []

        if me is not None:
            where = 'creator = %s'
            params = [me]

        if query:
            where += ' and ' if where else ''
            where += 'ignore_name like %s'
            params.append('%' + query + '%')

        vs = cls.select_vs(where=where, params=params, page=page, limit=limit, order='ignore_name')
        total = cls.total(where, params)
        return vs, total

    @classmethod
    def create(cls, ignore_name, user_name):
        # check duplicate grp_name
        if cls.column('id', where='ignore_name = %s', params=[ignore_name]):
            return -1

        return cls.insert({'ignore_name': ignore_name, 'create_user': user_name})