import asyncio
import logging

from hbmqtt.broker import Broker
from hbmqtt.utils import read_yaml_config


def main():
    formatter = "[%(asctime)s] :: %(levelname)s - %(message)s"

    logging.basicConfig(level=logging.DEBUG, format=formatter)

    try:
        config = read_yaml_config('config.yaml')
    except FileNotFoundError:
        config = read_yaml_config('default_config.yaml')

    loop = asyncio.get_event_loop()
    broker = Broker(config)
    try:
        loop.run_until_complete(broker.start())
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(broker.shutdown())
    finally:
        loop.close()


if __name__ == "__main__":
    main()
