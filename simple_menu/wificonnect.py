import network

wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(True)       # activate the interface
nets = wlan.scan()             # scan for access points

print(nets)
for net in nets:
    print(net.ssid)


# wlan.isconnected()      # check if the station is connected to an AP
# wlan.connect('essid', 'password') # connect to an AP
# wlan.config('mac')      # get the interface's MAC adddress
# wlan.ifconfig()         # get the interface's IP/netmask/gw/DNS addresses

