#! /bin/bash

# Configure CPU interface
# The FPs are expected to be created independently (e.g., by GNS3)
for num in 133; do
    ip link add eth"$num" type veth peer name veth"$num"
    ip link set eth"$num" mtu 10240 up
    ip link set veth"$num" mtu 10240 up
done
