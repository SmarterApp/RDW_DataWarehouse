'''
Created on Mar 31, 2014

@author: tosako
'''
from argparse import ArgumentParser
from edmigrate.utils.constants import Constants
from kombu.connection import Connection
from kombu.entity import Exchange, Queue
from edmigrate.tasks.player import player_task
from edmigrate.edmigrate_celery import setup_celery


settings = {'migrate.celery.CELERY_IMPORTS': '("edmigrate.tasks.player")',
            'migrate.celery.CELERY_QUEUES': "[{'key': 'edmigrate_players', 'name': 'edmigrate_players', 'durable': False, 'exchange': 'fanout'}]",
            'migrate.celery.CELERY_RESULT_BACKEND': 'amqp',
            'migrate.celery.CELERY_ROUTE': "[{'edmigrate.tasks.player': {'queue': 'edmigrate_players'}}]"
            }


def send_command(command, ids=None):
    player_task.apply_async((command, ids), exchange=Constants.BROADCAST_EXCHANGE)  # @UndefinedVariable


def main():
    parser = ArgumentParser(description='EdMigrate test')
    parser.add_argument('command', choices=[Constants.COMMAND_RESET_PLAYERS,
                                            Constants.COMMAND_REGISTER_PLAYER,
                                            Constants.COMMAND_CONNECT_PGPOOL,
                                            Constants.COMMAND_DISCONNECT_PGPOOL,
                                            Constants.COMMAND_START_REPLICATION,
                                            Constants.COMMAND_STOP_REPLICATION])
    parser.add_argument('-i', action='store', dest='id', type=int, default=None, help='id')
    parser.add_argument('-t', type=int, dest='timeout', default=5, help='reponse timeout')
    parser.add_argument('--url', dest='url', default='amqp://edware:edware1234@edwappsrv1.poc.dum.edwdc.net/edmigrate',
                        help='RMQ server, default[amqp://edware:edware1234@edwappsrv1.poc.dum.edwdc.net/edmigrate]')
    args = parser.parse_args()
    command = args.command
    ids = [args.id] if args.id else args.id
    url = args.url
    settings['migrate.celery.BROKER_URL'] = url
    setup_celery(settings)
    connection = Connection(url)
    exchange = Exchange(Constants.CONDUCTOR_EXCHANGE, type='direct')
    queue = Queue(Constants.CONDUCTOR_QUEUE, exchange=exchange, routing_key=Constants.CONDUCTOR_ROUTING_KEY, durable=False)
    simpleQueue = connection.SimpleQueue(queue, no_ack=True)
    simpleQueue.clear()
    timeout = args.timeout
    send_command(command, ids)
    try:
        msg = simpleQueue.get(timeout=timeout)
        message_ack_command = msg.payload[Constants.MESSAGE_ACK_COMMAND]
        node_id = msg.payload[Constants.MESSAGE_NODE_ID]
        print('node_id: ' + str(node_id))
        print('message_ack_command: ' + message_ack_command)
        return message_ack_command, node_id
    except Exception as e:
        print('No response from a player')
        print(e)
    finally:
        simpleQueue.close()
        connection.close()
    return None, None


if __name__ == '__main__':
    main()
