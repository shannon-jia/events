# -*- coding: utf-8 -*-

"""Main module."""

import logging
import time
import asyncio
log = logging.getLogger(__name__)


class EventsV1():
    def __init__(self, loop=None, max_list=10):
        self.loop = loop or asyncio.get_event_loop()
        self.actions = {}
        self.cables = []
        self.version = '1.1.0'
        self.id = 1
        self.MAX_EVENT_NUMBER = max_list

    def __str__(self):
        return "Events V1.0"

    def get_info(self):
        return {
            'events': self.actions
        }

    def get_cables(self):
        return self.cables

    def set_publish(self, publish):
        if callable(publish):
            self.publish = publish
        else:
            self.publish = None

    def start(self):
        self._auto_loop()

    def stop(self):
        pass

    def _auto_loop(self):
        self._update_actions()
        log.debug('Actions: {}'.format(self.actions))
        self.loop.call_later(1, self._auto_loop)

    def _register(self, act, status, timeout):
        self.actions[act] = {
            'status': status,
            'timeout': int(timeout),
            'timestamp': self._time_stamp()
        }

    def _update_actions(self):
        for act, val in self.actions.items():
            timeout = val.get('timeout', 0)
            _status = val.get('status')
            _time_stamp = val.get('timestamp')
            if timeout >= 1:
                timeout -= 1
                if timeout <= 1:
                    self._release(act)
                    _status = 'Off/Stop'
                    _time_stamp = self._time_stamp()
                self.actions[act] = {
                    'status': _status,
                    'timeout': int(timeout),
                    'timestamp': _time_stamp
                }

    def _time_stamp(self):
        t = time.localtime()
        time_stamp = '%d-%02d-%02d %02d:%02d:%02d' % (t.tm_year,
                                                      t.tm_mon,
                                                      t.tm_mday,
                                                      t.tm_hour,
                                                      t.tm_min,
                                                      t.tm_sec)
        return time_stamp

    async def got_command(self, mesg):
        try:
            log.debug('Amqp received: {}'.format(mesg))
            return await self._do_action(mesg)
        except Exception as e:
            log.error('do_action() exception: {}'.format(e))

    async def _do_action(self, mesg):
        # raise NotImplementedError
        name = mesg.get('name', '').upper()
        event_type = mesg.get('type', '').upper()
        if ((name == '') or (event_type == '')):
            return False
        detail = mesg.get('detail', 0.5)
        timestamp = mesg.get('time_stamp', '')
        if event_type == 'CABLE ALARM':
            return self._cable_alarm(name, detail, timestamp)

    def _cable_alarm(self, name, detail, timestamp):
        _nx = name.split('_')
        if len(_nx) < 3:
            log.warn('Invalid name: {}'.format(name))
            return False
        system = int(_nx[1])
        segment = int(_nx[2])
        return self._append_cables('alarm',
                                   system,
                                   segment,
                                   int(detail * 1000),
                                   timestamp)

    def _append_cables(self, event_type, system, segment, detail, timestamp):
        for cab in self.cables:
            if (timestamp == cab.get('timestamp') and
                system == cab.get('system') and
                segment == cab.get('segment') and
                detail == cab.get('offset')):
                return False

        if len(self.cables) >= self.MAX_EVENT_NUMBER:
            self.cables.pop(0)

        log.info('Append Alarm: {}_{}_{}@{}'.format(system,
                                                    segment,
                                                    detail,
                                                    timestamp))
        self.id += 1
        self.cables.append({
            'version': self.version,
            'id': self.id,
            'type': event_type,
            'system': system,
            'segment': segment,
            'offset': detail,
            'timestamp': timestamp,
            'remark': 'reserved'
        })
        return True

    def _release(self, act=None, args=None, status=None):
        raise NotImplementedError
