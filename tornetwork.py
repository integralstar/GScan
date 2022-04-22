import socks
import socket
import time
from stem.control import Controller
from stem import Signal
import requests
from bs4 import BeautifulSoup


def use_tornetwork():

    with Controller.from_port(port=9151) as controller:
        try:
            controller.authenticate()
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150)
            socket.socket = socks.socksocket

            r = requests.get("http://checkip.dyn.com")
            soup = BeautifulSoup(r.content, "lxml")
            print(soup.find("body").text)

            # wait till next identity will be available
            controller.signal(Signal.NEWNYM)
            time.sleep(controller.get_newnym_wait())

        except requests.HTTPError:
            print("Could not reach URL")

        controller.close()
