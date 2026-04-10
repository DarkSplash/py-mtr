import socket
import struct
import time
from scapy.all import sr1, IP, UDP
import argparse

def traceroute(destination, max_hops=30, timeout=2):
    destination_ip = socket.gethostbyname(destination)
    port = 33434
    ttl = 1

    while True:
        # Create the IP and UDP headers
        ip_packet = IP(dst=destination, ttl=ttl)
        udp_packet = UDP(dport=port)

        # Combine the headers
        packet = ip_packet / udp_packet

        # Send the packet and receive a reply
        reply = sr1(packet, timeout=timeout, verbose=0)

        if reply is None:
            # No reply, print * for timeout
            print(f"{ttl}\t*")
        elif reply.type == 3:
            # Destination reached, print the details
            print(f"{ttl}\t{reply.src}")
            break
        else:
            # Print the IP address of the intermediate hop
            print(f"{ttl}\t{reply.src}")

        ttl += 1

        if ttl > max_hops:
            break

def main():
    parser = argparse.ArgumentParser(description="Traceroute implementation in Python.")
    parser.add_argument("destination", help="Destination host or IP address.")
    parser.add_argument("-m", "--max-hops", type=int, default=30, help="Maximum number of hops (default: 30).")
    parser.add_argument("-t", "--timeout", type=int, default=2, help="Timeout for each packet in seconds (default: 2).")

    args = parser.parse_args()

    print(f"Traceroute to {args.destination} (max hops: {args.max_hops}, timeout: {args.timeout} seconds):")
    traceroute(args.destination, max_hops=args.max_hops, timeout=args.timeout)

if __name__ == "__main__":
    main()