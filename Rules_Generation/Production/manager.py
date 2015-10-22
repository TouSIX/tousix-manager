#    Copyright 2015 Rémy Lapeyrade <remy at lapeyrade dot net>
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

from Rules_Generation.Production.Dataflow.manager import Manager as Dataflow
from Rules_Generation.Production.Umbrella.manager import Manager as Umbrella
from Rules_Generation.configuration import configuration as conf

class Manager(object):
    """
    Manager class for creating production rules.
    """
    def create_rules_members(self, dpid, peers):
        """
        Create all the production rules needed for the members.
        :param dpid: Target DPID
        :type dpid: int
        :param members: Peer object array
        :type members: list(Peer)
        :return: flows rules array
        """
        rules = []
        dataflow = Dataflow()
        umbrella = Umbrella()
        for peer in peers:
            if conf.enabled["Production"].get('Dataflow') is True:
                rules.extend(dataflow.create_rules(dpid, peer))
            if (conf.enabled["Production"].get('Umbrella').get('IPv4') |
                    conf.enabled["Production"].get('Umbrella').get('IPv6')) is True:
                rules.extend(umbrella.create_rules(dpid, peer))
        return rules
