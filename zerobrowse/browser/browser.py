import zeroconf
import logging
import datetime
import json
from collections import OrderedDict

logger = logging.getLogger(__name__)

class BrowserListener(object):
    def __init__ (self):
        self.services = []

    def remove_service(self, zeroco, type, name):
        self.services = [s for s in self.services if s[1] != name]
        logger.info("Service {} removed".format (name))

    def add_service(self, zeroco, type, name):
        info = zeroco.get_service_info(type, name)
        self.services += [(type, name, info)]
        logger.info("{} Service {} added, service info: {}".format(datetime.datetime.now().isoformat(),name, info))

    def update_service (self, zeroco, type, name):
        self.services = [s for s in self.services if s[1] != name]
        info = zeroco.get_service_info(type, name)
        self.services += [(type, name, info)]
        logger.info("Service {} updated, service info: {}".format (name, info))


class ZeroconfBrowser ():
    def __init__(self, jsonstr=None):
        self.zero = zeroconf.Zeroconf ()
        self.well_known_services = ["_ssh._tcp.local.", "_http._tcp.local.", "_workstation._tcp.local.", "_smb._tcp.local.", "_ftp._tcp.local.", "_printer._tcp.local.", "_ipp._tcp.local." ]
        self.browser_list = {}
        self.service_browser = {}

        if jsonstr:
            self.load_from_json(jsonstr)
        else:
            for service_type in self.well_known_services:
                self.add_listener (service_type)

    def get_service_dict (self):
        return zeroconf.ZeroconfServiceTypes.find()

    def get_service_stat (self):
        services = sorted (self.browser_list.keys())
        dic = OrderedDict()
        for service in services:
            dic[service] = len(self.get_services_from_type(service))

        return dic

    def get_services_from_type (self, typename):
        if not typename in self.browser_list:
            return []

        host_services = []
        for service in self.browser_list[typename].services:
            adresses = []
            properties = []
            for adr in service[2].addresses:
                if zeroconf._is_v6_address(adr):
                    adresses += [':'.join([str(c.hex()) for c in adr])]
                else:
                    adresses += ['.'.join([str(c) for c in adr])]

            for prop, val in service[2].properties.items():
                properties += ['{}={}'.format(str(prop, 'utf-8'), str(val, 'utf-8'))]

            host_services += [(service[2].server, service[2].port, ','.join(adresses), ','.join(properties))]

        return host_services

    def add_listener (self, service_type):
        if not service_type in self.browser_list:
            self.browser_list[service_type] = BrowserListener()
            self.service_browser[service_type] = zeroconf.ServiceBrowser(self.zero, service_type,
                                                                     self.browser_list[service_type])

    def delete_listener (self, service_type):
        if service_type in self.browser_list:
            self.service_browser.pop(service_type)
            self.browser_list.pop(service_type)

    def dump_to_json (self):
        listeners = [service for service in self.browser_list.keys()]
        print (self.browser_list.keys())
        print(listeners)
        return json.dumps({"listeners":listeners})

    def load_from_json (self, jsonstr):
        list = json.loads(jsonstr)
        self.well_known_services = list
        for service_type in self.well_known_services:
            self.add_listener(service_type)

    def get_well_known (self):
        return self.well_known_services

    def zeroconf_to_ihm_service (self, service):
        return service.split ('.')[0][1:]

    def __delete__(self, instance):
        self.zero.close()
