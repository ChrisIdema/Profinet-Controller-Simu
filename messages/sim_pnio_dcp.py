from types import FrameType
from scapy.all import *
from scapy.contrib.pnio_dcp import *
from scapy.contrib.pnio import *
import time

load_contrib("pnio_dcp")
load_contrib("pnio")


def get_ident_msg(src, dst, name_of_station):
    ether = Ether(dst=dst, src=src, type=0x8892)
    pnio_msg = ProfinetIO(frameID=DCP_IDENTIFY_REQUEST_FRAME_ID)
    pnio_dcp_ident = ProfinetDCP(
        service_id=DCP_SERVICE_ID_IDENTIFY,
        service_type=DCP_REQUEST,
        xid=0x9a,
        reserved=1,
        dcp_data_length=len(name_of_station) + (5 if len(name_of_station) % 2 == 1 else 4),
        option=0x02,
        sub_option=0x02,
        dcp_block_length=len(name_of_station),
        name_of_station=name_of_station
    )
    return ether / pnio_msg / pnio_dcp_ident


def get_set_ip_msg(src, dst, ip, netmask="255.255.255.0", gateway="0.0.0.0"):
    ether = Ether(dst=dst, src=src, type=0x8892)

    pnio_msg = ProfinetIO(frameID=0xFEFD)

    pnio_dcp_set_ip = ProfinetDCP(
        service_id=0x04,
        service_type=DCP_REQUEST,
        xid=0x04,
        reserved=0,
        dcp_data_length=18,
        option=0x01,
        sub_option=0x02,
        dcp_block_length=14,
        block_qualifier=0x0000,
        ip=ip,
        netmask=netmask,
        gateway=gateway,
    )

    return ether / pnio_msg / pnio_dcp_set_ip



