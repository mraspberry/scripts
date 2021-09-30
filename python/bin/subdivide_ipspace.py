#!/usr/bin/env python3

import argparse
import netaddr


def subdivide(ipnet, prefixlen):
    return ipnet.subnet(prefixlen)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "ip_network",
        metavar="NETWORK",
        type=netaddr.IPNetwork,
        help="Network to subdivide",
    )
    parser.add_argument(
        "prefix_len",
        metavar="PREFIX",
        type=int,
        help="Prefix length to divide network into",
    )
    args = parser.parse_args()

    for net in subdivide(args.ip_network, args.prefix_len):
        print(net)


if __name__ == "__main__":
    main()
