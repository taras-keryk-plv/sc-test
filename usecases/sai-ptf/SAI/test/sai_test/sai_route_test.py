# Copyright (c) 2021 Microsoft Open Technologies, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#    THIS CODE IS PROVIDED ON AN *AS IS* BASIS, WITHOUT WARRANTIES OR
#    CONDITIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT
#    LIMITATION ANY IMPLIED WARRANTIES OR CONDITIONS OF TITLE, FITNESS
#    FOR A PARTICULAR PURPOSE, MERCHANTABILITY OR NON-INFRINGEMENT.
#
#    See the Apache Version 2.0 License for specific language governing
#    permissions and limitations under the License.
#
#    Microsoft would like to thank the following companies for their review and
#    assistance with these files: Intel Corporation, Mellanox Technologies Ltd,
#    Dell Products, L.P., Facebook, Inc., Marvell International Ltd.
#
#

from sai_test_base import T0TestBase
from sai_utils import *
from time import sleep

from data_module.device import Device, DeviceType

class RouteRifTest(T0TestBase):
    """
    Verify route with RIF directly (next hop is RIF)
    """

    def setUp(self):
        """
        Test the basic setup process.
        """
        super().setUp()

    def runTest(self):
        """
        1. Make sure common config for route dest IP within 192.168.12.0/24 through RIF(Nhop is Rif) to LAG2 created
        2. Send packets for DIP:192.168.12.1~8 SIP 192.168.0.1 DMAC: SWITCH_MAC on port5
        3. Verify packet received with SMAC: SWITCH_MAC SIP: 192.168.0.1 DIP:192.168.12.1~8 on one of LAG2 member
        """
        print("RouteRifTest")

        self.recv_dev_port_idxs = self.get_dev_port_indexes(self.servers[12][1].l3_lag_obj.member_port_indexs)
        try:
            for i in range(1, 9):
                pkt = simple_tcp_packet(eth_dst=ROUTER_MAC,
                                        ip_dst=self.servers[12][i].ipv4,
                                        ip_id=105,
                                        ip_ttl=64)
                exp_pkt = simple_tcp_packet(eth_src=ROUTER_MAC,
                                            eth_dst=self.servers[12][i].l3_lag_obj.neighbor_mac,
                                            ip_dst=self.servers[12][i].ipv4,
                                            ip_id=105,
                                            ip_ttl=63)
                send_packet(self, self.dut.port_obj_list[5].dev_port_index, pkt)
                verify_packet_any_port(self, exp_pkt, self.recv_dev_port_idxs)
                print("received packet with dst_ip:{} on one of lag2 member".format(self.servers[12][i].ipv4))
        finally:
            pass
    
    def tearDown(self):
        super().tearDown()


class RouteRifv6Test(T0TestBase):
    """
    Verify v6 route with RIF directly (next hop is RIF)
    """

    def setUp(self):
        """
        Test the basic setup process.
        """
        super().setUp()

    def runTest(self):
        """
        1. Make sure common config for route dest IP within fc02::12:0/112 through RIF(Nhop is Rif) to LAG2 created
        2. Send packets for DIP:fc02::12:1~8 SIP:fc02::0:1 DMAC:SWITCH_MAC on port5
        3. Verify packet received with SMAC:SWITCH_MAC SIP:fc02::0:1 DIP:fc02::12:1~8 on one of LAG2 member
        """
        print("RouteRifv6Test")

        self.recv_dev_port_idxs = self.get_dev_port_indexes(self.servers[12][1].l3_lag_obj.member_port_indexs)
        try:
            for i in range(1, 9):
                pkt_v6 = simple_udpv6_packet(eth_dst=ROUTER_MAC,
                                             ipv6_dst=self.servers[12][i].ipv6,
                                             ipv6_hlim=64)
                exp_pkt_v6 = simple_udpv6_packet(eth_src=ROUTER_MAC,
                                                 eth_dst=self.servers[12][i].l3_lag_obj.neighbor_mac,
                                                 ipv6_dst=self.servers[12][i].ipv6,
                                                 ipv6_hlim=63)
                send_packet(self, self.dut.port_obj_list[5].dev_port_index, pkt_v6)
                verify_packet_any_port(self, exp_pkt_v6, self.recv_dev_port_idxs)
                print("received packet with dst_ip:{} on one of lag2 member".format(self.servers[12][i].ipv6))
        finally:
            pass
    
    def tearDown(self):
        super().tearDown()


class LagMultipleRouteTest(T0TestBase):
    """
    Verify multi-route to the same nhop.
    """

    def setUp(self):
        """
        Test the basic setup process.
        """
        super().setUp()
    
    def runTest(self):
        """
        1. Make sure common config created for IP within in 192.168.21.0/24, through next-hop: IP 10.1.1.100 LAG1
        2. Check vlan interfaces(svi added)
        3. Send packet with SIP:192.168.0.1 DIP:192.168.21.1 DMAC:SWITCH_MAC on port5
        4. Verify packet received with SMAC: SWITCH_MAC SIP 192.168.0.1 DIP:192.168.21.1 on one of LAG1 member
        5. Send packet with SIP:192.168.0.1 DIP:192.168.11.1 DMAC:SWITCH_MAC on port5
        6. Verify packet received with SMAC: SWITCH_MAC SIP:192.168.0.1 DIP:192.168.11.1 on one of LAG1 member
        """
        print("LagMultipleRouteTest")

        self.recv_dev_port_idxs = self.get_dev_port_indexes(self.servers[11][1].l3_lag_obj.member_port_indexs)
        pkt1 = simple_tcp_packet(eth_dst=ROUTER_MAC,
                                 ip_dst=self.servers[21][1].ipv4,
                                 ip_id=105,
                                 ip_ttl=64)
        exp_pkt1 = simple_tcp_packet(eth_src=ROUTER_MAC,
                                     eth_dst=self.t1_list[1][100].mac,
                                     ip_dst=self.servers[21][1].ipv4,
                                     ip_id=105,
                                     ip_ttl=63)

        pkt2 = simple_tcp_packet(eth_dst=ROUTER_MAC,
                                 ip_dst=self.servers[11][1].ipv4,
                                 ip_id=105,
                                 ip_ttl=64)
        exp_pkt2 = simple_tcp_packet(eth_src=ROUTER_MAC,
                                     eth_dst=self.servers[11][1].l3_lag_obj.neighbor_mac,
                                     ip_dst=self.servers[11][1].ipv4,
                                     ip_id=105,
                                     ip_ttl=63)          

        try:
            send_packet(self, self.dut.port_obj_list[5].dev_port_index, pkt1)
            verify_packet_any_port(self, exp_pkt1, self.recv_dev_port_idxs)
            print("receive packet with dst_ip:{} from one of lag1 member".format(self.servers[21][1].ipv4))

            send_packet(self, self.dut.port_obj_list[5].dev_port_index, pkt2)
            verify_packet_any_port(self, exp_pkt2, self.recv_dev_port_idxs)
            print("receive packet with dst_ip:{} from one of lag1 member".format(self.servers[11][1].ipv4))
        finally:
            pass

    def tearDown(self):
        super().tearDown()


class LagMultipleRoutev6Test(T0TestBase):
    """
    Verify v6 multi-route to the same nhop.
    """

    def setUp(self):
        """
        Test the basic setup process.
        """
        super().setUp()
    
    def runTest(self):
        """
        1. Make sure common config created for IP within in fc02::21:0/112, through next-hop: IP fc02::1:10 LAG1
        2. Check vlan interfaces(svi added)
        3. Send packet with SIP:fc02::0:1 DIP:fc02::21:1 DMAC:SWITCH_MAC on port5
        4. Verify packet received with SMAC: SWITCH_MAC SIP fc02::0:1 DIP:fc02::21:1 on one of LAG1 member
        5. Send packet with SIP:fc02::0:1 DIP:fc02::11:1 DMAC:SWITCH_MAC on port5
        6. Verify packet received with SMAC:SWITCH_MAC SIP:fc02::0:1 DIP:fc02::11:1 on one of LAG1 member
        """
        print("LagMultipleRoutev6Test")

        self.recv_dev_port_idxs = self.get_dev_port_indexes(self.servers[11][1].l3_lag_obj.member_port_indexs)
        pkt1_v6 = simple_tcpv6_packet(eth_dst=ROUTER_MAC,
                                      ipv6_dst=self.servers[21][1].ipv6,
                                      ipv6_hlim=64)
        exp_pkt1_v6 = simple_tcpv6_packet(eth_src=ROUTER_MAC,
                                          eth_dst=self.t1_list[1][100].mac,
                                          ipv6_dst=self.servers[21][1].ipv6,
                                          ipv6_hlim=63)

        pkt2_v6 = simple_tcpv6_packet(eth_dst=ROUTER_MAC,
                                      ipv6_dst=self.servers[11][1].ipv6,
                                      ipv6_hlim=64)
        exp_pkt2_v6 = simple_tcpv6_packet(eth_src=ROUTER_MAC,
                                          eth_dst=self.servers[11][1].l3_lag_obj.neighbor_mac,
                                          ipv6_dst=self.servers[11][1].ipv6,
                                          ipv6_hlim=63)

        try:
            send_packet(self, self.dut.port_obj_list[5].dev_port_index, pkt1_v6)
            verify_packet_any_port(self, exp_pkt1_v6, self.recv_dev_port_idxs)
            print("receive packet with dst_ip:{} from one of lag1 member".format(self.servers[21][1].ipv6))

            send_packet(self, self.dut.port_obj_list[5].dev_port_index, pkt2_v6)
            verify_packet_any_port(self, exp_pkt2_v6, self.recv_dev_port_idxs)
            print("receive packet with dst_ip:{} from one of lag1 member".format(self.servers[11][1].ipv6))
        finally:
            pass

    def tearDown(self):
        super().tearDown()


class DropRouteTest(T0TestBase):
    """
    Verify drop the packet when SAI_PACKET_ACTION_DROP
    """

    def setUp(self):
        """
        Test the basic setup process.
        """
        super().setUp()
    
    def runTest(self):
        """
        1. Create new route. Dest_IP:10.1.1.10 with SAI_PACKET_ACTION_DROP, through an already existing next-hop: IP 10.1.1.100 LAG1
        2. Send packet with SIP:192.168.0.1 DIP:10.1.1.10 DMAC:SWITCH_MAC on port5
        3. Verify no packet on any of the LAG1 members
        4. Check the packet drop counter
        """
        print("DropRouteTest...")

        self.t1_list[1][10].ip_prefix = '24'
        self.t1_list[1][10].ip_prefix_v6 = '112'
        self.new_routev4, self.new_routev6 = self.route_configer.create_route_by_nexthop(
            dest_device=self.t1_list[1][0],
            nexthopv4=self.dut.lag_list[0].nexthopv4_list[0],
            nexthopv6=self.dut.lag_list[0].nexthopv6_list[0])
        sai_thrift_set_route_entry_attribute(self.client, self.new_routev4, packet_action=SAI_PACKET_ACTION_DROP)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        print("create new route with SAI_PACKET_ACTION_DROP")
        
        pkt = simple_tcp_packet(eth_dst=ROUTER_MAC,
                                ip_dst=self.t1_list[1][10].ipv4,
                                ip_id=105,
                                ip_ttl=64)
        try:
            send_packet(self, self.dut.port_obj_list[5].dev_port_index, pkt)
            verify_no_other_packets(self)
            print("no other packets")
            #TODO check packet drop counter
        finally:
            self.dut.routev4_list.remove(self.new_routev4)
            self.dut.routev6_list.remove(self.new_routev6)
            sai_thrift_remove_route_entry(self.client, self.new_routev4)
            self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
            sai_thrift_remove_route_entry(self.client, self.new_routev6)
            self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
            pass

    def tearDown(self):
        super().tearDown()


class DropRoutev6Test(T0TestBase):
    """
    Verify drop the packet when SAI_PACKET_ACTION_DROP
    """

    def setUp(self):
        """
        Test the basic setup process.
        """
        super().setUp()
    
    def runTest(self):
        """
        1. Create new route. Dest_IP:fc02::1:10 with SAI_PACKET_ACTION_DROP, through an already existing next-hop: IP fc02::1:100 LAG1
        2. Send packet with SIP:fc02::0:1 DIP:fc02::1:10 DMAC:SWITCH_MAC on port5
        3. Verify no packet on any of the LAG1 members
        4. Check the packet drop counter
        """
        print("DropRoutev6Test...")

        self.t1_list[1][10].ip_prefix = '24'
        self.t1_list[1][10].ip_prefix_v6 = '112'
        self.new_routev4, self.new_routev6 = self.route_configer.create_route_by_nexthop(
            dest_device=self.t1_list[1][0],
            nexthopv4=self.dut.lag_list[0].nexthopv4_list[0],
            nexthopv6=self.dut.lag_list[0].nexthopv6_list[0])
        sai_thrift_set_route_entry_attribute(self.client, self.new_routev6, packet_action=SAI_PACKET_ACTION_DROP)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        print("create new route with SAI_PACKET_ACTION_DROP")
        
        pkt_v6 = simple_tcpv6_packet(eth_dst=ROUTER_MAC,
                                     ipv6_dst=self.t1_list[1][10].ipv6,
                                     ipv6_hlim=64)
        try:
            send_packet(self, self.dut.port_obj_list[5].dev_port_index, pkt_v6)
            verify_no_other_packets(self)
            print("no other packets")
            #TODO check packet drop counter
        finally:
            self.dut.routev4_list.remove(self.new_routev4)
            self.dut.routev6_list.remove(self.new_routev6)
            sai_thrift_remove_route_entry(self.client, self.new_routev4)
            self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
            sai_thrift_remove_route_entry(self.client, self.new_routev6)
            self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
            pass

    def tearDown(self):
        super().tearDown()


class RouteUpdateTest(T0TestBase):
    """
    Verify route action gets updated when set attribute from SAI_PACKET_ACTION_DROP to SAI_PACKET_ACTION_FORWARD
    """

    def setUp(self):
        """
        Test the basic setup process.
        """
        super().setUp()
    
    def runTest(self):
        """
        1. Set Existing Route on DIP:192.168.11.0/24 with packet action as SAI_PACKET_ACTION_DROP
        2. Send packet with SIP:192.168.0.1 DIP:192.168.11.1 DMAC:SWITCH_MAC on port5
        3. Verify no packet on any of the LAG1 members
        4. Set Route packet action as SAI_PACKET_ACTION_FORWARD
        5. Send packet with SIP:192.168.0.1 DIP:192.168.11.1 DMAC: SWITCH_MAC on port5
        6. Verify packet received with SMAC: SWITCH_MAC SIP 192.168.0.1 DIP:192.168.11.1 on one of LAG1 member
        """
        print("RouteUpdateTest...")
        
        self.recv_dev_port_idxs = self.get_dev_port_indexes(self.servers[11][1].l3_lag_obj.member_port_indexs)
        pkt = simple_tcp_packet(eth_dst=ROUTER_MAC,
                                ip_dst=self.servers[11][1].ipv4,
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(eth_src=ROUTER_MAC,
                                    eth_dst=self.t1_list[1][100].mac,
                                    ip_dst=self.servers[11][1].ipv4,
                                    ip_id=105,
                                    ip_ttl=63)
        try:
            sai_thrift_set_route_entry_attribute(self.client, self.servers[11][0].routev4, packet_action=SAI_PACKET_ACTION_DROP)
            self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
            print("set route on 192.168.11.0/24 with action SAI_PACKET_ACTION_DROP")

            send_packet(self, self.dut.port_obj_list[5].dev_port_index, pkt)
            verify_no_other_packets(self)
            print("no packets received after set packet action to DROP")

            sai_thrift_set_route_entry_attribute(self.client, self.servers[11][0].routev4, packet_action=SAI_PACKET_ACTION_FORWARD)
            self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
            print("Update route action to forward")

            send_packet(self, self.dut.port_obj_list[5].dev_port_index, pkt)
            verify_packet_any_port(self, exp_pkt, self.recv_dev_port_idxs)
            print("packet received on one of lag1 member after set packet action to FORWARD")
        finally:
            pass

    def tearDown(self):
        super().tearDown()


class RouteUpdatev6Test(T0TestBase):
    """
    Verify v6 route action gets updated when set attribute from SAI_PACKET_ACTION_DROP to SAI_PACKET_ACTION_FORWARD
    """

    def setUp(self):
        """
        Test the basic setup process.
        """
        super().setUp()
    
    def runTest(self):
        """
        1. Set Existing Route on DIP:fc02::11:0/112 with packet action as SAI_PACKET_ACTION_DROP
        2. Send packet with SIP:fc02::0:1 DIP:fc02::11:1 DMAC:SWITCH_MAC on port5
        3. Verify no packet on any of the LAG1 members
        4. Set Route packet action as SAI_PACKET_ACTION_FORWARD
        5. Send packet with SIP:fc02::0:1 DIP:fc02::11:1 DMAC: SWITCH_MAC on port5
        6. Verify packet received with SMAC: SWITCH_MAC SIP:fc02::0:1 DIP:fc02::11:1 on one of LAG1 member
        """
        print("RouteUpdatev6Test...")
        
        self.recv_dev_port_idxs = self.get_dev_port_indexes(self.servers[11][1].l3_lag_obj.member_port_indexs)
        pkt_v6 = simple_tcpv6_packet(eth_dst=ROUTER_MAC,
                                     ipv6_dst=self.servers[11][1].ipv6,
                                     ipv6_hlim=64)
        exp_pkt_v6 = simple_tcpv6_packet(eth_src=ROUTER_MAC,
                                         eth_dst=self.t1_list[1][100].mac,
                                         ipv6_dst=self.servers[11][1].ipv6,
                                         ipv6_hlim=63)
        try:
            sai_thrift_set_route_entry_attribute(self.client, self.servers[11][0].routev6, packet_action=SAI_PACKET_ACTION_DROP)
            self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
            print("set route on fc02::11:0/112 with action SAI_PACKET_ACTION_DROP")

            send_packet(self, self.dut.port_obj_list[5].dev_port_index, pkt_v6)
            verify_no_other_packets(self)
            print("no packets received after set packet action to DROP")

            sai_thrift_set_route_entry_attribute(self.client, self.servers[11][0].routev6, packet_action=SAI_PACKET_ACTION_FORWARD)
            self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
            print("Update route action to forward")

            send_packet(self, self.dut.port_obj_list[5].dev_port_index, pkt_v6)
            verify_packet_any_port(self, exp_pkt_v6, self.recv_dev_port_idxs)
            print("packet received on one of lag1 member after set packet action to FORWARD")
        finally:
            pass

    def tearDown(self):
        super().tearDown()


class RouteLPMRouteNexthopTest(T0TestBase):
    """
    Verify lpm route path (with next-hop), route path will be alter to the more accurate one
    """

    def setUp(self):
        """
        Test the basic setup process.
        """
        super().setUp()

        self.dst_ip = '192.168.1.200'
        self.dmac1 = '00:11:22:33:44:55'
        self.dmac2 = '00:11:22:33:44:66'
    
    def runTest(self):
        """
        1. Make sure the route for DIP:192.168.1.0/24 is already configured (the route through the next hop)
        2. Add a neighbor with IP:192.168.1.200 on Port2 with DMAC1
        3. Send packet with DMAC: SWITCH_MAC and DIP:192.168.1.200 on port5
        4. Received packet with the DMAC1, SMAC: SWITCH_MAC and DIP:192.168.1.200 on port2
        5. Add a new route for DIP:192.168.1.200/32 with a next-hop on port1
        6. Add a neighbor with IP:192.168.1.200 on Port1 with DMAC2
        7. Send packet with DMAC: SWITCH_MAC and DIP:192.168.1.200 on port5
        8. Received packet with the DMAC2, SMAC: SWITCH_MAC and DIP:192.168.1.200 on port1
        """
        print("RouteLPMRouteNexthopTest")
        self.port1_rif = sai_thrift_create_router_interface(self.client,
                                                            virtual_router_id=self.dut.default_vrf,
                                                            type=SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                            port_id=self.dut.port_obj_list[1].oid)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

        self.port2_rif = sai_thrift_create_router_interface(self.client,
                                                            virtual_router_id=self.dut.default_vrf,
                                                            type=SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                            port_id=self.dut.port_obj_list[2].oid)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        # Add a neighbor with IP:192.168.1.200 on Port2 with DMAC1
        self.port2_nbr_entry = sai_thrift_neighbor_entry_t(rif_id=self.port2_rif,
                                                           ip_address=sai_ipaddress(self.dst_ip))
        status = sai_thrift_create_neighbor_entry(self.client,
                                                  self.port2_nbr_entry,
                                                  dst_mac_address=self.dmac1)
        self.assertEqual(status, SAI_STATUS_SUCCESS)
        print("Add a neighbor with IP:192.168.1.200 on Port2 with DMAC1")

        pkt = simple_tcp_packet(eth_dst=ROUTER_MAC,
                                ip_dst=self.dst_ip,
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt1 = simple_tcp_packet(eth_src=ROUTER_MAC,
                                     eth_dst=self.dmac1,
                                     ip_dst=self.dst_ip,
                                     ip_id=105,
                                     ip_ttl=63)
        exp_pkt2 = simple_tcp_packet(eth_src=ROUTER_MAC,
                                     eth_dst=self.dmac2,
                                     ip_dst=self.dst_ip,
                                     ip_id=105,
                                     ip_ttl=63)

        try:
            send_packet(self, self.dut.port_obj_list[5].dev_port_index, pkt)
            verify_packet(self, exp_pkt1, self.dut.port_obj_list[2].dev_port_index)
            print("packet with dst_ip:{} sent from port5, received from port2".format(self.dst_ip))

            # Add a neighbor with IP:192.168.1.200 on Port1 with DMAC2
            self.port1_nbr_entry = sai_thrift_neighbor_entry_t(rif_id=self.port1_rif,
                                                               ip_address=sai_ipaddress(self.dst_ip))
            status = sai_thrift_create_neighbor_entry(self.client,
                                                      self.port1_nbr_entry,
                                                      dst_mac_address=self.dmac2)
            print("Add a neighbor with IP:192.168.1.200 on Port1 with DMAC2")

            # Add a new route for DIP:192.168.1.200/32 with a next-hop on port1
            self.port1_nhop = sai_thrift_create_next_hop(self.client,
                                                         ip=sai_ipaddress(self.dst_ip),
                                                         router_interface_id=self.port1_rif,
                                                         type=SAI_NEXT_HOP_TYPE_IP)
            self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
            self.port1_route = sai_thrift_route_entry_t(vr_id=self.dut.default_vrf,
                                                        destination=sai_ipprefix(self.dst_ip+'/32'))
            status = sai_thrift_create_route_entry(self.client, self.port1_route, next_hop_id=self.port1_nhop)
            self.assertEqual(status, SAI_STATUS_SUCCESS)
            print("add a new route DIP:192.168.1.200/32 with next-hop on port1")

            send_packet(self, self.dut.port_obj_list[5].dev_port_index, pkt)
            verify_packet(self, exp_pkt2, self.dut.port_obj_list[1].dev_port_index)
            print("after add new neighbor for port1, packet with dst_ip:{} sent from port5, received from port1".format(self.dst_ip))
        finally:
            pass

    def tearDown(self):
        sai_thrift_remove_route_entry(self.client, self.port1_route)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        sai_thrift_remove_next_hop(self.client, self.port1_nhop)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        sai_thrift_remove_neighbor_entry(self.client, self.port1_nbr_entry)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        sai_thrift_remove_router_interface(self.client, self.port1_rif)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        sai_thrift_remove_router_interface(self.client, self.port2_rif)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        super().tearDown()


class RouteLPMRouteNexthopv6Test(T0TestBase):
    """
    Verify v6 lpm route path (with next-hop), route path will be alter to the more accurate one
    """

    def setUp(self):
        """
        Test the basic setup process.
        """
        super().setUp()

        self.dst_ip = 'fc02::1:200'
        self.dmac1 = '00:11:22:33:44:55'
        self.dmac2 = '00:11:22:33:44:66'
    
    def runTest(self):
        """
        1. Make sure the route for DIP:fc02::1:0/112 is already configured (the route through the next hop)
        2. Add a neighbor with IP:fc02::1:200 on Port2 with DMAC1
        3. Send packet with DMAC: SWITCH_MAC and DIP:fc02::1:200 on port5
        4. Received packet with the DMAC1, SMAC: SWITCH_MAC and DIP:fc02::1:200 on port2
        5. Add a new route for DIP:fc02::1:200/128 with a next-hop on port1
        6. Add a neighbor with IP:fc02::1:200 on Port1 with DMAC2
        7. Send packet with DMAC: SWITCH_MAC and DIP:fc02::1:200 on port5
        8. Received packet with the DMAC2, SMAC: SWITCH_MAC and DIP:fc02::1:200 on port1
        """
        print("RouteLPMRouteNexthopv6Test")
        self.port1_rif = sai_thrift_create_router_interface(self.client,
                                                            virtual_router_id=self.dut.default_vrf,
                                                            type=SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                            port_id=self.dut.port_obj_list[1].oid)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

        self.port2_rif = sai_thrift_create_router_interface(self.client,
                                                            virtual_router_id=self.dut.default_vrf,
                                                            type=SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                            port_id=self.dut.port_obj_list[2].oid)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        # Add a neighbor with IP:fc02::1:200 on Port2 with DMAC1
        self.port2_nbr_entry = sai_thrift_neighbor_entry_t(rif_id=self.port2_rif,
                                                           ip_address=sai_ipaddress(self.dst_ip))
        status = sai_thrift_create_neighbor_entry(self.client,
                                                  self.port2_nbr_entry,
                                                  dst_mac_address=self.dmac1)
        self.assertEqual(status, SAI_STATUS_SUCCESS)
        print("Add a neighbor with IP:fc02::1:200 on Port2 with DMAC1")

        pkt_v6 = simple_tcpv6_packet(eth_dst=ROUTER_MAC,
                                     ipv6_dst=self.dst_ip,
                                     ipv6_hlim=64)
        exp_pkt1_v6 = simple_tcpv6_packet(eth_src=ROUTER_MAC,
                                          eth_dst=self.dmac1,
                                          ipv6_dst=self.dst_ip,
                                          ipv6_hlim=63)
        exp_pkt2_v6 = simple_tcpv6_packet(eth_src=ROUTER_MAC,
                                          eth_dst=self.dmac2,
                                          ipv6_dst=self.dst_ip,
                                          ipv6_hlim=63)

        try:
            send_packet(self, self.dut.port_obj_list[5].dev_port_index, pkt_v6)
            verify_packet(self, exp_pkt1_v6, self.dut.port_obj_list[2].dev_port_index)
            print("packet with dst_ip:{} sent from port5, received from port2".format(self.dst_ip))

            # Add a neighbor with IP:fc02::1:200 on Port1 with DMAC2
            self.port1_nbr_entry = sai_thrift_neighbor_entry_t(rif_id=self.port1_rif,
                                                               ip_address=sai_ipaddress(self.dst_ip))
            status = sai_thrift_create_neighbor_entry(self.client,
                                                      self.port1_nbr_entry,
                                                      dst_mac_address=self.dmac2)
            print("Add a neighbor with IP:fc02::1:200 on Port1 with DMAC2")

            # Add a new route for DIP:fc02::1:200/128 with a next-hop on port1
            self.port1_nhop = sai_thrift_create_next_hop(self.client,
                                                         ip=sai_ipaddress(self.dst_ip),
                                                         router_interface_id=self.port1_rif,
                                                         type=SAI_NEXT_HOP_TYPE_IP)
            self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
            self.port1_route = sai_thrift_route_entry_t(vr_id=self.dut.default_vrf,
                                                        destination=sai_ipprefix(self.dst_ip+'/128'))
            status = sai_thrift_create_route_entry(self.client, self.port1_route, next_hop_id=self.port1_nhop)
            self.assertEqual(status, SAI_STATUS_SUCCESS)
            print("add a new route DIP:fc02::1:200/128 with next-hop on port1")

            send_packet(self, self.dut.port_obj_list[5].dev_port_index, pkt_v6)
            verify_packet(self, exp_pkt2_v6, self.dut.port_obj_list[1].dev_port_index)
            print("after add new neighbor for port1, packet with dst_ip:{} sent from port5, received from port1".format(self.dst_ip))
        finally:
            pass

    def tearDown(self):
        sai_thrift_remove_route_entry(self.client, self.port1_route)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        sai_thrift_remove_next_hop(self.client, self.port1_nhop)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        sai_thrift_remove_neighbor_entry(self.client, self.port1_nbr_entry)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        sai_thrift_remove_router_interface(self.client, self.port1_rif)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        sai_thrift_remove_router_interface(self.client, self.port2_rif)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        super().tearDown()


class RouteLPMRouteRifTest(T0TestBase):
    """
    Verify lpm route path (with rif as next hop), route path will be alter to the more accurate one
    """

    def setUp(self):
        """
        Test the basic setup process.
        """
        super().setUp()

        self.dst_ip = '192.168.1.200'
        self.dmac1 = '00:11:22:33:44:55'
        self.dmac2 = '00:11:22:33:44:66'
    
    def runTest(self):
        """
        1. Make sure the route for DIP:192.168.1.0/24 is already configured (the route through next hop)
        2. Add a neighbor with IP:192.168.1.200 on Port2 with DMAC1
        3. Send packet with DMAC: SWITCH_MAC and DIP: IP:192.168.1.200 on port5
        4. Received packet with the DMAC1, SMAC: SWITCH_MAC and DIP: IP:192.168.1.200 on port2
        5. Add a new route for DIP: IP:192.168.1.200/32 and bind to port1 rif directly
        6. Add a neighbor with IP:192.168.1.200 on Port1 with DMAC2
        7. Send packet with DMAC: SWITCH_MAC and DIP: IP:192.168.1.200 on port5
        8. Received packet with the DMAC2, SMAC: SWITCH_MAC and DIP: IP:192.168.1.200 on port1
        """
        print("RouteLPMRouteRifTest")

        self.port1_rif = sai_thrift_create_router_interface(self.client,
                                                            virtual_router_id=self.dut.default_vrf,
                                                            type=SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                            port_id=self.dut.port_obj_list[1].oid)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

        self.port2_rif = sai_thrift_create_router_interface(self.client,
                                                            virtual_router_id=self.dut.default_vrf,
                                                            type=SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                            port_id=self.dut.port_obj_list[2].oid)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

        # Add a neighbor with IP:192.168.1.200 on Port2 with DMAC1
        self.port2_nbr_entry = sai_thrift_neighbor_entry_t(rif_id=self.port2_rif,
                                                           ip_address=sai_ipaddress(self.dst_ip))
        status = sai_thrift_create_neighbor_entry(self.client,
                                                  self.port2_nbr_entry,
                                                  dst_mac_address=self.dmac1)
        self.assertEqual(status, SAI_STATUS_SUCCESS)
        print("Add a neighbor with IP:192.168.1.200 on Port2 with DMAC1")

        pkt = simple_tcp_packet(eth_dst=ROUTER_MAC,
                                ip_dst=self.dst_ip,
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt1 = simple_tcp_packet(eth_src=ROUTER_MAC,
                                     eth_dst=self.dmac1,
                                     ip_dst=self.dst_ip,
                                     ip_id=105,
                                     ip_ttl=63)
        exp_pkt2 = simple_tcp_packet(eth_src=ROUTER_MAC,
                                     eth_dst=self.dmac2,
                                     ip_dst=self.dst_ip,
                                     ip_id=105,
                                     ip_ttl=63)

        try:
            send_packet(self, self.dut.port_obj_list[5].dev_port_index, pkt)
            verify_packet(self, exp_pkt1, self.dut.port_obj_list[2].dev_port_index)
            print("packet with dst_ip:{} sent from port5, received from port2".format(self.dst_ip))

            # Add a neighbor with IP:192.168.1.200 on Port1 with DMAC2
            self.port1_nbr_entry = sai_thrift_neighbor_entry_t(rif_id=self.port1_rif,
                                                               ip_address=sai_ipaddress(self.dst_ip))
            status = sai_thrift_create_neighbor_entry(self.client,
                                                      self.port1_nbr_entry,
                                                      dst_mac_address=self.dmac2)
            print("Add a neighbor with IP:192.168.1.200 on Port1 with DMAC2")

            # Add a new route for DIP: IP:192.168.1.200/32 and bind to port1 rif directly
            self.port1_route = sai_thrift_route_entry_t(vr_id=self.dut.default_vrf,
                                                        destination=sai_ipprefix(self.dst_ip+'/32'))
            status = sai_thrift_create_route_entry(self.client, self.port1_route, next_hop_id=self.port1_rif)
            self.assertEqual(status, SAI_STATUS_SUCCESS)
            print("add a new route DIP:192.168.1.200/32 and bind to port1 rif directly")

            send_packet(self, self.dut.port_obj_list[5].dev_port_index, pkt)
            verify_packet(self, exp_pkt2, self.dut.port_obj_list[1].dev_port_index)
            print("after add new neighbor for port1, packet with dst_ip:{} sent from port5, received from port1".format(self.dst_ip))
        finally:
            pass

    def tearDown(self):
        sai_thrift_remove_route_entry(self.client, self.port1_route)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        sai_thrift_remove_neighbor_entry(self.client, self.port1_nbr_entry)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        sai_thrift_remove_router_interface(self.client, self.port1_rif)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        sai_thrift_remove_router_interface(self.client, self.port2_rif)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        super().tearDown()


class RouteLPMRouteRifv6Test(T0TestBase):
    """
    Verify v6 lpm route path (with rif as next hop), route path will be alter to the more accurate one
    """

    def setUp(self):
        """
        Test the basic setup process.
        """
        super().setUp()

        self.dst_ip = 'fc02::1:200'
        self.dmac1 = '00:11:22:33:44:55'
        self.dmac2 = '00:11:22:33:44:66'
    
    def runTest(self):
        """
        1. Make sure the route for DIP:fc02::1:0/112 is already configured (the route through next hop)
        2. Add a neighbor with IP:fc02::1:200 on Port2 with DMAC1
        3. Send packet with DMAC: SWITCH_MAC and DIP:fc02::1:200 on port5
        4. Received packet with the DMAC1, SMAC: SWITCH_MAC and DIP:fc02::1:200 on port2
        5. Add a new route for DIP:fc02::1:200/128 and bind to port1 rif directly
        6. Add a neighbor with IP:fc02::1:200 on Port1 with DMAC2
        7. Send packet with DMAC: SWITCH_MAC and DIP:fc02::1:200 on port5
        8. Received packet with the DMAC2, SMAC: SWITCH_MAC and DIP:fc02::1:200 on port1
        """
        print("RouteLPMRouteRifv6Test")

        self.port1_rif = sai_thrift_create_router_interface(self.client,
                                                            virtual_router_id=self.dut.default_vrf,
                                                            type=SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                            port_id=self.dut.port_obj_list[1].oid)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

        self.port2_rif = sai_thrift_create_router_interface(self.client,
                                                            virtual_router_id=self.dut.default_vrf,
                                                            type=SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                            port_id=self.dut.port_obj_list[2].oid)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

        # Add a neighbor with IP:fc02::1:200 on Port2 with DMAC1
        self.port2_nbr_entry = sai_thrift_neighbor_entry_t(rif_id=self.port2_rif,
                                                           ip_address=sai_ipaddress(self.dst_ip))
        status = sai_thrift_create_neighbor_entry(self.client,
                                                  self.port2_nbr_entry,
                                                  dst_mac_address=self.dmac1)
        self.assertEqual(status, SAI_STATUS_SUCCESS)
        print("Add a neighbor with IP:fc02::1:200 on Port2 with DMAC1")

        pkt_v6 = simple_tcpv6_packet(eth_dst=ROUTER_MAC,
                                     ipv6_dst=self.dst_ip,
                                     ipv6_hlim=64)
        exp_pkt1_v6 = simple_tcpv6_packet(eth_src=ROUTER_MAC,
                                          eth_dst=self.dmac1,
                                          ipv6_dst=self.dst_ip,
                                          ipv6_hlim=63)
        exp_pkt2_v6 = simple_tcpv6_packet(eth_src=ROUTER_MAC,
                                          eth_dst=self.dmac2,
                                          ipv6_dst=self.dst_ip,
                                          ipv6_hlim=63)

        try:
            send_packet(self, self.dut.port_obj_list[5].dev_port_index, pkt_v6)
            verify_packet(self, exp_pkt1_v6, self.dut.port_obj_list[2].dev_port_index)
            print("packet with dst_ip:{} sent from port5, received from port2".format(self.dst_ip))

            # Add a neighbor with IP:fc02::1:200 on Port1 with DMAC2
            self.port1_nbr_entry = sai_thrift_neighbor_entry_t(rif_id=self.port1_rif,
                                                               ip_address=sai_ipaddress(self.dst_ip))
            status = sai_thrift_create_neighbor_entry(self.client,
                                                      self.port1_nbr_entry,
                                                      dst_mac_address=self.dmac2)
            print("Add a neighbor with IP:fc02::1:200 on Port1 with DMAC2")

            # Add a new route for DIP: IP:fc02::1:200/128 and bind to port1 rif directly
            self.port1_route = sai_thrift_route_entry_t(vr_id=self.dut.default_vrf,
                                                        destination=sai_ipprefix(self.dst_ip+'/128'))
            status = sai_thrift_create_route_entry(self.client, self.port1_route, next_hop_id=self.port1_rif)
            self.assertEqual(status, SAI_STATUS_SUCCESS)
            print("add a new route DIP:fc02::1:200/128 and bind to port1 rif directly")

            send_packet(self, self.dut.port_obj_list[5].dev_port_index, pkt_v6)
            verify_packet(self, exp_pkt2_v6, self.dut.port_obj_list[1].dev_port_index)
            print("after add new neighbor for port1, packet with dst_ip:{} sent from port5, received from port1".format(self.dst_ip))
        finally:
            pass

    def tearDown(self):
        sai_thrift_remove_route_entry(self.client, self.port1_route)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        sai_thrift_remove_neighbor_entry(self.client, self.port1_nbr_entry)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        sai_thrift_remove_router_interface(self.client, self.port1_rif)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        sai_thrift_remove_router_interface(self.client, self.port2_rif)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        super().tearDown()


class SviMacFloodingTest(T0TestBase):
    """
    Verify route to svi and flooding
    """

    def setUp(self):
        """
        Test the basic setup process.
        """
        super().setUp()
    
    def sviMacFloodingTest(self):
        """
        1. Check config for mac for port1~8 already exist
        2. Check vlan interfaces(svi added)
        3. Check already created route and neighbor as, route subnet fc02::1:0/112 next hop to VLAN10 SVI, neighbor for Port2-4 with IP DIP:fc02::1:92-94 bind to VLAN10 SVI
        4. Create neighbor for DIP:192.168.1.94 with new DMAC:Mac4 on VLAN10 route interface
        5. Send packet with DMAC:SWITCH_MAC, SMAC:00:01:01:99:01:92 and DIP:192.168.1.94 on port10
        6. No packet or flooding on VLAN10 member port
        """
        print("SviMacFloodingTest")

        # create neighbor for DIP:192.168.1.94 with new DMAC:Mac4 on VLAN10 route interface
        dmac4 = '00:11:22:33:44:55'
        self.servers[1][94].mac = dmac4
        self.port4_nbr_v4, self.port4_nbr_v6 = self.route_configer.create_neighbor_by_rif(nexthop_device=self.servers[1][94], rif=self.dut.vlans[10].rif_list[0])
        print("Create neighbor for DIP:192.168.1.94 with new DMAC:{} on vlan10 route interface".format(dmac4))
        
        pkt = simple_tcp_packet(eth_dst=ROUTER_MAC,
                                eth_src=self.servers[1][92].mac,
                                ip_dst=self.servers[1][94].ipv4)
        
        send_packet(self, self.dut.port_obj_list[10].dev_port_index, pkt)
        verify_no_other_packets(self)
        print("No packet on vlan10 member")

    def runTest(self):
        try:
            self.sviMacFloodingTest()
        finally:
            pass
    
    def tearDown(self):
        self.dut.neighborv4_list.remove(self.port4_nbr_v4)
        self.dut.neighborv6_list.remove(self.port4_nbr_v6)
        sai_thrift_remove_neighbor_entry(self.client, self.port4_nbr_v4)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        sai_thrift_remove_neighbor_entry(self.client, self.port4_nbr_v6)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        super().tearDown()


class SviMacFloodingv6Test(T0TestBase):
    """
    Verify v6 route to svi and flooding
    """

    def setUp(self):
        """
        Test the basic setup process.
        """
        super().setUp()
    
    def sviMacFloodingv6Test(self):
        """
        1. Check config for mac for port1~8 already exist
        2. Check vlan interfaces(svi added)
        3. Check already created route and neighbor as, route subnet 192.168.1.0/24 next hop to VLAN10 SVI, neighbor for Port2-4 with IP DIP:192.168.1.92-94 bind to VLAN10 SVI
        4. Create neighbor for DIP:fc01::1:94 with new DMAC:Mac4 on VLAN10 route interface
        5. Send packet with DMAC:SWITCH_MAC, SMAC:00:01:01:99:01:92 and DIP:fc01::1:94 on port10
        6. No packet or flooding on VLAN10 member port
        """
        print("SviMacFloodingv6Test")

        # create neighbor for DIP:fc01::1:94 with new DMAC:Mac4 on VLAN10 route interface
        dmac4 = '00:11:22:33:44:55'
        self.servers[1][94].mac = dmac4
        self.port4_nbr_v4, self.port4_nbr_v6 = self.route_configer.create_neighbor_by_rif(nexthop_device=self.servers[1][94], rif=self.dut.vlans[10].rif_list[0])
        print("Create neighbor for DIP:fc01::1:94 with new DMAC:{} on vlan10 route interface".format(dmac4))
        
        pkt_v6 = simple_tcpv6_packet(eth_dst=ROUTER_MAC,
                                     eth_src=self.servers[1][92].mac,
                                     ipv6_dst=self.servers[1][94].ipv6)
        
        send_packet(self, self.dut.port_obj_list[10].dev_port_index, pkt_v6)
        verify_no_other_packets(self)
        print("No packet on vlan10 member")

    def runTest(self):
        try:
            self.sviMacFloodingv6Test()
        finally:
            pass
    
    def tearDown(self):
        self.dut.neighborv4_list.remove(self.port4_nbr_v4)
        self.dut.neighborv6_list.remove(self.port4_nbr_v6)
        sai_thrift_remove_neighbor_entry(self.client, self.port4_nbr_v4)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        sai_thrift_remove_neighbor_entry(self.client, self.port4_nbr_v6)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        super().tearDown()


class SviDirectBroadcastTest(T0TestBase):
    """
    Verify svi direct broadcast
    """
    def setUp(self):
        """
        Test the basic setup process.
        """
        super().setUp()
    
    def runTest(self):
        """
        1. Make sure route interface, neighbor, and route already exist in the config for VLAN20 SVI.
        2. Make sure Broadcast neighbor already exists in config within VLAN20 subnet (broadcast IP and DMAC is broadcast address)
        3. send packet with DMAC: SWITCH_MAC DIP: IP:192.168.2.255 on port5
        4. Verify packet received on port9-16
        """
        print("SviDirectBroadcastTest")
        recv_dev_ports = self.get_dev_port_indexes(
            list(self.dut.vlans[20].port_idx_list))
        pkt = simple_tcp_packet(eth_dst=ROUTER_MAC,
                                ip_dst=self.dut.vlans[20].broadcast_neighbor_device.ipv4,
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(eth_dst=BROADCAST_MAC,
                                    eth_src=ROUTER_MAC,
                                    ip_dst=self.dut.vlans[20].broadcast_neighbor_device.ipv4,
                                    ip_id=105,
                                    ip_ttl=63)
        try:
            send_packet(self, self.dut.port_obj_list[5].dev_port_index, pkt)
            verify_each_packet_on_multiple_port_lists(self, [exp_pkt], [recv_dev_ports])
        finally:
            pass

    def tearDown(self):
        super().tearDown()
