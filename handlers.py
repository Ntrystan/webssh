__author__ = 'xsank'

import logging

import tornado.websocket

from daemon import Bridge
from data import ClientData
from utils import check_ip, check_port


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class WSHandler(tornado.websocket.WebSocketHandler):
    clients = dict()

    def get_client(self):
        return self.clients.get(self._id(), None)

    def put_client(self):
        bridge = Bridge(self)
        self.clients[self._id()] = bridge

    def remove_client(self):
        if bridge := self.get_client():
            bridge.destroy()
            del self.clients[self._id()]

    @staticmethod
    def _check_init_param(data):
        return check_ip(data["host"]) and check_port(data["port"])

    @staticmethod
    def _is_init_data(data):
        return data.get_type() == 'init'

    def _id(self):
        return id(self)

    def open(self):
        self.put_client()

    def on_message(self, message):
        bridge = self.get_client()
        client_data = ClientData(message)
        if self._is_init_data(client_data):
            if self._check_init_param(client_data.data):
                bridge.open(client_data.data)
                logging.info(f'connection established from: {self._id()}')
            else:
                self.remove_client()
                logging.warning(f'init param invalid: {client_data.data}')
        elif bridge:
            bridge.trans_forward(client_data.data)

    def on_close(self):
        self.remove_client()
        logging.info(f'client close the connection: {self._id()}')

