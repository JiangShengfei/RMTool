import ping

def pingtest(destIP, timeout, count, packetsize):
    try:
        result = ping.quiet_ping(destIP, timeout=timeout, count=count, psize=packetsize)
        return result
    except IndexError:
        print ("ping unknow error.")
