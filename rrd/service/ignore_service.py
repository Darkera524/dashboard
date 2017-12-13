from rrd.store import db

from rrd.utils.logger import logging
log = logging.getLogger(__file__)

def delete_ignore(ignore_id=None):
    try:
        cursor = db.execute('delete from `ignore` where id = %s', [ignore_id])
        db.execute('delete from ignore_host where ignore_id = %s', [ignore_id], cursor=cursor)
        db.execute('delete from ignore_group where ignore_id = %s', [ignore_id], cursor=cursor)
        db.commit()
        return ''
    except Exception, e:
        log.error(e)
        db.rollback()
        return 'delete ignore metric %s fail' % ignore_id
    finally:
        cursor and cursor.close()