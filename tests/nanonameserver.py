# Copyright (C) Dnspython Contributors, see LICENSE for text of ISC license

import logging
import logging.config

import trio
import trio.testing

from tests.server import Server

if __name__ == "__main__":
    import sys
    import time

    logger = logging.getLogger(__name__)
    format = "%(asctime)s %(levelname)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO)
    logging.config.dictConfig(
        {
            "version": 1,
            "incremental": True,
            "loggers": {
                "quart.app": {
                    "level": "INFO",
                },
                "quart.serving": {
                    "propagate": False,
                    "level": "ERROR",
                },
                "quic": {
                    "level": "CRITICAL",
                },
            },
        }
    )

    async def trio_main():
        try:
            with Server(
                port=5354, dot_port=5355, doh_port=5356, use_thread=False
            ) as server:
                print("Trio mode")
                for proto, address in server.addresses.items():
                    print(f"  listening on {proto.name}: {address}")
                async with trio.open_nursery() as nursery:
                    nursery.start_soon(server.main)
        except Exception as e:
            print("trio_main caught", type(e), e)

    def threaded_main():
        with Server(port=5354, dot_port=5355, doh_port=5356) as server:
            print("Thread mode")
            for proto, address in server.addresses.items():
                print(f"  listening on {proto.name}: {address}")
            time.sleep(300)

    if len(sys.argv) > 1 and sys.argv[1] == "trio":
        trio.run(trio_main)
    else:
        threaded_main()
