# -*- coding: utf-8 -*-

"""Console script for rps."""

import click
from .log import get_log
from .routermq import RouterMQ
from .events import EventsV1 as Events
from . import api_server
import asyncio


def validate_url(ctx, param, value):
    try:
        return value
    except ValueError:
        raise click.BadParameter('url need to be format: tcp://ipv4:port')


@click.command()
@click.option('--max_list', default=100,
              envvar='MAX_LIST',
              help='maxium list number, default=10, ENV: MAX_LIST')
@click.option('--amqp', default='amqp://guest:guest@rabbit:5672//',
              callback=validate_url,
              envvar='SVC_AMQP',
              help='Amqp url, also ENV: SVC_AMQP')
@click.option('--port', default=80,
              envvar='SVC_PORT',
              help='Api port, default=80, ENV: SVC_PORT')
@click.option('--qid', default=0,
              envvar='SVC_QID',
              help='ID for amqp queue name, default=0, ENV: SVC_QID')
@click.option('--username', default='admin',
              envvar='SVC_USERNAME',
              help='Api auth username, ENV: SVC_USERNAME')
@click.option('--password', default='admin',
              envvar='SVC_PASSWORD',
              help='Api auth password, ENV: SVC_PASSWORD')
@click.option('--debug', is_flag=True)
def main(max_list, amqp, port, qid, username, password, debug):
    """Events V1.0 Output for SAV V1.0"""

    click.echo("See more documentation at http://www.mingvale.com")

    info = {
        'api_port': port,
        'amqp': amqp,
        'max list': max_list,
    }
    log = get_log(debug)
    log.info('Basic Information: {}'.format(info))

    loop = asyncio.get_event_loop()
    loop.set_debug(0)

    # main process
    try:
        site = Events(loop, max_list)
        router = RouterMQ(outgoing_key='Events.third',
                          routing_keys=['Alarms.keeper'],
                          queue_name='third_'+str(qid),
                          url=amqp)
        router.set_callback(site.got_command)
        site.set_publish(router.publish)
        site.start()
        amqp_task = loop.create_task(router.reconnector())
        api_task = loop.create_task(api_server.start(port=port,
                                                     site=site,
                                                     username=username,
                                                     password=password))
        loop.run_forever()
    except KeyboardInterrupt:
        if amqp_task:
            amqp_task.cancel()
            loop.run_until_complete(amqp_task)
        if api_task:
            api_task.cancel()
            loop.run_until_complete(api_task)
        site.stop()
    finally:
        loop.stop()
        loop.close()
