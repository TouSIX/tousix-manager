#    Copyright 2015 Rémy Lapeyrade <remy at lapeyrade dot net>
#    Copyright 2018 Marc Bruyere <mbruyere ad nc dot u-tokyo dot ac dot jp>
#    Copyright 2015 LAAS-CNRS
#
#
#    This file is part of TouSIX-Manager.
#
#    TouSIX-Manager is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    TouSIX-Manager is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with TouSIX-Manager.  If not, see <http://www.gnu.org/licenses/>.


from tousix_manager.Database.models import Hote, Switchlink, Switch, Port
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString as qs
from django.conf import settings
yaml = YAML()


def HexInt(i):
    ''' function to insert right hexa dpids '''
    stri = "0x" + hex(i)[2:].upper().zfill(1)

    return yaml.load(stri)


def Braket(i):
    ''' function to remove the brackets for the Groupe faiover buckets'''

    return yaml.load(i)

class Manager(object):
    def __init__(self):
        self.vlan_name = settings['FAUCET_SETTINGS']['vlan_name']

# TODO implement link query for yaml script
    def generate_host(self, hote):

        hote = Hote.objects.get(id=1)
        cl = Host
        cl.name = hote.nomhote
        cl.location = hote.idport.idswitch.idpop.nompop
        cl.description = "Machine of member " + hote.idmembre.nommembre + ", location: " + cl.location
        cl.ipv4 = hote.ipv4hote
        cl.ipv6 = hote.ipv6hote
        cl.mac = hote.machote
        cl.port = hote.idport.numport

    def get_next_hop(self, node_src):
        pass

    def convert_table(self):
        list = []
        for host in Hote.objects.all():
            table = {}

        return []


    def triangle(self, list_load = [], def_switches = []):

        data = {'vlans': {'tousix': {'vid': 100, 'description': qs(self.vlan_name)}}, 'dps': {
            'Edge1': {'dp_id': HexInt(Switch.objects.get(nomswitch="Edge1").id), 'hardware': qs(Switch.objects.get(nomswitch="Edge1").faucet_class), 'interfaces': {
                1: {'name': qs('link'), 'description': qs('link'), 'native_vlan': 100, 'acl_in': 1,
                    'opstatus_reconf': False},
                int(settings['FAUCET_SETTINGS']['sw1_portnum_to_sw2']): {'name': qs('link'), 'description': qs('link'), 'native_vlan': 100,
                                          'acl_in': 1, 'opstatus_reconf': False},
                int(settings['FAUCET_SETTINGS']['sw1_portnum_to_sw3']): {'name': qs('link'), 'description': qs('link'), 'native_vlan': 100,
                                          'acl_in': 1, 'opstatus_reconf': False}}
                      }, 'Edge2': {'dp_id': HexInt(Switch.objects.get(nomswitch="Edge2").id), 'hardware': qs(Switch.objects.get(nomswitch="Edge2").faucet_class), 'interfaces': {
                1: {'name': qs('link'), 'description': qs('link'), 'native_vlan': 100, 'acl_in': 2,
                    'opstatus_reconf': False},
                int(settings['FAUCET_SETTINGS']['sw2_portnum_to_sw1']): {'name': qs('link'), 'description': qs('link'), 'native_vlan': 100,
                                          'acl_in': 2, 'opstatus_reconf': False},
                int(settings['FAUCET_SETTINGS']['sw2_portnum_to_sw3']): {'name': qs('link'), 'description': qs('link'), 'native_vlan': 100,
                                          'acl_in': 2, 'opstatus_reconf': False}}},
            'Edge3': {'dp_id': HexInt(Switch.objects.get(nomswitch="Edge3").id), 'hardware': qs(Switch.objects.get(nomswitch="Edge3").faucet_class), 'interfaces': {
                1: {'name': qs('link'), 'description': qs('link'), 'native_vlan': 100, 'acl_in': 3,
                    'opstatus_reconf': False},
                int(settings['FAUCET_SETTINGS']['sw3_portnum_to_sw1']): {'name': qs('link'), 'description': qs('link'), 'native_vlan': 100,
                                          'acl_in': 3, 'opstatus_reconf': False},
                int(settings['FAUCET_SETTINGS']['sw3_portnum_to_sw2']): {'name': qs('link'), 'description': qs('link'), 'native_vlan': 100,
                                          'acl_in': 3, 'opstatus_reconf': False}}}},
                'acls': {}}
        for i in range(len(list_load)):
            if list_load[i]['switch'] == 'Edge1' and list_load[i]['status'] == 'Production':
                data['dps']['Edge1']['interfaces'][int(list_load[i]['port'])] = {'name': qs(list_load[i]['hostname']),
                                                                                 'description': qs(
                                                                                     list_load[i]['hostname']),
                                                                                 'native_vlan': 100, 'acl_in': 1}
                data['acls'][1].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                    'output': {'port': int(list_load[i]['port'])}}}})
                data['acls'][1].append(
                    {'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
                        list_load[i]['addr_ipv6']), 'actions': {'output': {'port': int(list_load[i]['port'])}}}})
                data['acls'][1].append(
                    {'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
                        list_load[i]['addr_ipv4']), 'actions': {'output': {'port': int(list_load[i]['port'])}}}})

                data['acls'][2].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                    'output': {'failover': {'group_id': 1 + i, 'ports': Braket(
                        '[' + settings['FAUCET_SETTINGS']['sw2_portnum_to_sw1'] + ',' + settings['FAUCET_SETTINGS']['sw2_portnum_to_sw3'] + ']')}}}}})
                data['acls'][2].append(
                    {'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
                        list_load[i]['addr_ipv6']), 'actions': {'output': {'failover': {'group_id': 100 + i,
                                                                                        'ports': Braket(
                                                                                            '[' + settings['FAUCET_SETTINGS']['sw2_portnum_to_sw1'] + ',' + settings['FAUCET_SETTINGS']['sw2_portnum_to_sw3'] + ']')}}}}})
                data['acls'][2].append(
                    {'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
                        list_load[i]['addr_ipv4']), 'actions': {'output': {'failover': {'group_id': 200 + i,
                                                                                        'ports': Braket(
                                                                                            '[' + settings['FAUCET_SETTINGS']['sw2_portnum_to_sw1'] + ',' + settings['FAUCET_SETTINGS']['sw2_portnum_to_sw3'] + ']')}}}}})

                data['acls'][3].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                    'output': {'failover': {'group_id': 300 + i, 'ports': Braket(
                        '[' + settings['FAUCET_SETTINGS']['sw3_portnum_to_sw1'] + ',' + settings['FAUCET_SETTINGS'] ['sw3_portnum_to_sw2'] + ']')}}}}})
                data['acls'][3].append(
                    {'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
                        list_load[i]['addr_ipv6']), 'actions': {'output': {'failover': {'group_id': 400 + i,
                                                                                        'ports': Braket(
                                                                                            '[' + settings['FAUCET_SETTINGS']['sw3_portnum_to_sw1'] + ',' + settings['FAUCET_SETTINGS']['sw3_portnum_to_sw2'] + ']')}}}}})
                data['acls'][3].append(
                    {'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
                        list_load[i]['addr_ipv4']), 'actions': {'output': {'failover': {'group_id': 500 + i,
                                                                                        'ports': Braket(
                                                                                            '[' + settings['FAUCET_SETTINGS']['sw3_portnum_to_sw1'] + ',' + settings['FAUCET_SETTINGS']['sw3_portnum_to_sw2'] + ']')}}}}})
            elif list_load[i]['switch'] == 'Edge2' and list_load[i]['status'] == 'Production':
                data['dps']['Edge2']['interfaces'][int(list_load[i]['port'])] = {'name': qs(list_load[i]['hostname']),
                                                                                 'description': qs(
                                                                                     list_load[i]['hostname']),
                                                                                 'native_vlan': 100, 'acl_in': 2}
                data['acls'][1].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                    'output': {'failover': {'group_id': 600 + i, 'ports': Braket(
                        '[' + settings['FAUCET_SETTINGS']['sw1_portnum_to_sw2'] + ',' + settings['FAUCET_SETTINGS']['sw1_portnum_to_sw3'] + ']')}}}}})
                data['acls'][1].append(
                    {'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
                        list_load[i]['addr_ipv6']), 'actions': {'output': {'failover': {'group_id': 700 + i,
                                                                                        'ports': Braket(
                                                                                            '[' + settings['FAUCET_SETTINGS']['sw1_portnum_to_sw2'] + ',' + settings['FAUCET_SETTINGS']['sw1_portnum_to_sw3'] + ']')}}}}})
                data['acls'][1].append(
                    {'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
                        list_load[i]['addr_ipv4']), 'actions': {'output': {'failover': {'group_id': 800 + i,
                                                                                        'ports': Braket(
                                                                                            '[' + settings['FAUCET_SETTINGS']['sw1_portnum_to_sw2'] + ',' + settings['FAUCET_SETTINGS']['sw1_portnum_to_sw3'] + ']')}}}}})

                data['acls'][2].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                    'output': {'port': int(list_load[i]['port'])}}}})
                data['acls'][2].append(
                    {'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
                        list_load[i]['addr_ipv6']), 'actions': {'output': {'port': int(list_load[i]['port'])}}}})
                data['acls'][2].append(
                    {'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
                        list_load[i]['addr_ipv4']), 'actions': {'output': {'port': int(list_load[i]['port'])}}}})

                data['acls'][3].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                    'output': {'failover': {'group_id': 900 + i, 'ports': Braket(
                        '[' + settings['FAUCET_SETTINGS']['sw3_portnum_to_sw2'] + ',' + settings['FAUCET_SETTINGS']['sw3_portnum_to_sw1'] + ']')}}}}})
                data['acls'][3].append(
                    {'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
                        list_load[i]['addr_ipv6']), 'actions': {'output': {'failover': {'group_id': 1000 + i,
                                                                                        'ports': Braket(
                                                                                            '[' + settings['FAUCET_SETTINGS']['sw3_portnum_to_sw2'] + ',' + settings['FAUCET_SETTINGS']['sw3_portnum_to_sw1'] + ']')}}}}})
                data['acls'][3].append(
                    {'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
                        list_load[i]['addr_ipv4']), 'actions': {'output': {'failover': {'group_id': 1100 + i,
                                                                                        'ports': Braket(
                                                                                            '[' + settings['FAUCET_SETTINGS']['sw3_portnum_to_sw2'] + ',' + settings['FAUCET_SETTINGS']['sw3_portnum_to_sw1'] + ']')}}}}})
            elif list_load[i]['switch'] == 'Edge3' and list_load[i]['status'] == 'Production':
                data['dps']['Edge3']['interfaces'][int(list_load[i]['port'])] = {'name': qs(list_load[i]['hostname']),
                                                                                 'description': qs(
                                                                                     list_load[i]['hostname']),
                                                                                 'native_vlan': 100, 'acl_in': 3}
                data['acls'][1].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                    'output': {'failover': {'group_id': 1200 + i, 'ports': Braket(
                        '[' + settings['FAUCET_SETTINGS']['sw1_portnum_to_sw3'] + ',' + settings['FAUCET_SETTINGS']['sw1_portnum_to_sw2'] + ']')}}}}})
                data['acls'][1].append(
                    {'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
                        list_load[i]['addr_ipv6']), 'actions': {'output': {'failover': {'group_id': 1300 + i,
                                                                                        'ports': Braket(
                                                                                            '[' + settings['FAUCET_SETTINGS']['sw1_portnum_to_sw3'] + ',' + settings['FAUCET_SETTINGS']['sw1_portnum_to_sw2'] + ']')}}}}})
                data['acls'][1].append(
                    {'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
                        list_load[i]['addr_ipv4']), 'actions': {'output': {'failover': {'group_id': 1400 + i,
                                                                                        'ports': Braket(
                                                                                            '[' + settings['FAUCET_SETTINGS']['sw1_portnum_to_sw3'] + ',' + settings['FAUCET_SETTINGS']['sw1_portnum_to_sw2'] + ']')}}}}})

                data['acls'][2].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                    'output': {'failover': {'group_id': 1500 + i, 'ports': Braket(
                        '[' + settings['FAUCET_SETTINGS']['sw2_portnum_to_sw3'] + ',' + settings['FAUCET_SETTINGS']['sw2_portnum_to_sw1'] + ']')}}}}})
                data['acls'][2].append(
                    {'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
                        list_load[i]['addr_ipv6']), 'actions': {'output': {'failover': {'group_id': 1600 + i,
                                                                                        'ports': Braket(
                                                                                            '[' + settings['FAUCET_SETTINGS']['sw2_portnum_to_sw3'] + ',' + settings['FAUCET_SETTINGS']['sw2_portnum_to_sw1'] + ']')}}}}})
                data['acls'][2].append(
                    {'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
                        list_load[i]['addr_ipv4']), 'actions': {'output': {'failover': {'group_id': 1700 + i,
                                                                                        'ports': Braket(
                                                                                            '[' + settings['FAUCET_SETTINGS']['sw2_portnum_to_sw3'] + ',' + settings['FAUCET_SETTINGS']['sw2_portnum_to_sw1'] + ']')}}}}})

                data['acls'][3].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                    'output': {'port': int(list_load[i]['port'])}}}})
                data['acls'][3].append(
                    {'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
                        list_load[i]['addr_ipv6']), 'actions': {'output': {'port': int(list_load[i]['port'])}}}})
                data['acls'][3].append(
                    {'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
                        list_load[i]['addr_ipv4']), 'actions': {'output': {'port': int(list_load[i]['port'])}}}})
        data['acls'][1].append({'rule': {'actions': {'allow': 0}}})
        data['acls'][2].append({'rule': {'actions': {'allow': 0}}})
        data['acls'][3].append({'rule': {'actions': {'allow': 0}}})

        return (data)

    def get_interfaces_switch(self, switch):
        pass

    def generate_datapath(self):
        result = {}
        for switch in Switch.objects.all():
            switch_def = {}
            switch_def['dp_id'] = switch.idswitch
            switch_def['hardware'] = switch.faucet_class
            intf = {}
            for port in Port.objects.filter(idswitch=switch.id):
                intf[port.numport] = {'acl_in': switch_def['dp_id'],
                                      'description': Hote.objects.filter(idport=port.id).get(0).nomhote,
                                      'name':  Hote.objects.filter(idport=port.id).get(0).nomhote,
                                      'native_vlan': settings['FAUCET_SETTINGS']['vlan_native_id'],
                                      'opstatus_reconf': False}
            switch_def['interfaces'] = intf
            result[switch.nomswitch] = switch_def
        return {'dps': result}
    def generate_acls(self):
        #TODO include script gen.py
        pass


class Interface(object):
    switch = 0xaaa
    port = 32
    name = "Port name"
    description = "Some port description"
    vlans = {"access": "access",
             "tagged": []}
    acls = []

    def gen_yaml(self):
        object = {self.port: {
            "name": self.name,
            "description": self.description,
            "acls_in": []
        }}
        if len(self.vlans['access']) ==1:
            object[self.port]['native_vlan'] = self.vlans["access"]
        if len(self.vlans['tagged']) >= 1:
            object[self.port]['tagged_vlans'] = self.vlans["tagged"]

        return yaml.dump(object)


class Host(object):

    name = ""
    ipv4 = ""
    ipv6 = ""
    mac = ""
    port = 3
    location = ""
    description = ""
