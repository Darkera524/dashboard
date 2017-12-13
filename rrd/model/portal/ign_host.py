

from .bean import Bean
from .ignore import Ignore
from .host import Host

class Ign_host(Bean):
    _tbl = 'ignore_host'
    _cols = 'ignore_id, host_id, bind_user'
    _id = ''

    def __init__(self, ignore_id, host_id, bind_user):
        self.ignore_id = ignore_id
        self.host_id = host_id
        self.bind_user = bind_user

    @classmethod
    def host_list(cls, ignore_ids = None):
        if not ignore_ids:
            return []

        host_ids = cls.column('host_id', where='ignore_id=%s',params=[ignore_ids])
        if not host_ids:
            return []

        host_ids = ['%s' % i for i in host_ids]
        ids = ','.join(host_ids)

        return Host.select_vs(where='id in (%s)' % ids)

    @classmethod
    def bind_host(cls, ignore_id, host_id, bind_user):
        if cls.exists('ignore_id=%s and host_id=%s',[ignore_id, host_id]):
            return

        cls.insert(
            {
                'ignore_id': ignore_id,
                'host_id': host_id,
                'bind_user': bind_user
            }

        )

    @classmethod
    def unbind_host(cls, ignore_id, host_id):
        return cls.delete('ignore_id = %s and host_id = %s', [ignore_id, host_id])

