from .bean import Bean
from .ignore import Ignore
from .host_group import HostGroup

class Ign_group(Bean):
    _tbl = 'ignore_group'
    _cols = 'ignore_id, group_id, bind_user'
    _id = ''

    def __init__(self, ignore_id, group_id, bind_user):
        self.ignore_id = ignore_id
        self.group_id = group_id
        self.bind_user = bind_user

    @classmethod
    def group_list(cls, ignore_ids = None):
        if not ignore_ids:
            return []

        group_ids = cls.column('group_id', where='ignore_id=%s',params=[ignore_ids])
        if not group_ids:
            return []

        group_ids = ['%s' % i for i in group_ids]
        ids = ','.join(group_ids)

        return HostGroup.select_vs(where='id in (%s)' % ids)

    @classmethod
    def bind_group(cls, ignore_id, group_id, bind_user):
        if cls.exists('ignore_id=%s and group_id=%s',[ignore_id, group_id]):
            return

        cls.insert(
            {
                'ignore_id': ignore_id,
                'group_id': group_id,
                'bind_user': bind_user
            }

        )

    @classmethod
    def unbind_group(cls, ignore_id, group_id):
        return cls.delete('ignore_id = %s and group_id = %s', [ignore_id, group_id])

