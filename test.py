# -*- coding: utf-8 -*-
import sys, os, socket, http.client
from urllib.parse import urlparse

def dns(hostname):
    ''' convert hostname to ip address.
    '''
    try:
        host_addr = socket.gethostbyname(hostname)
        return host_addr
    except socket.gaierror:
        return False

def ping(ip):
    ''' ping ip address.
    '''
    # the ping option is different between windows and linux.
    ping_option = "-n 1 " if sys.platform.lower() == "win32" else "-c 1 "
    response = os.system("ping " + ping_option + ip)
    return response == 0

def port(ip):
    ''' test whether the port 80 is open or not.
    '''
    sockobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    response = sockobj.connect_ex((ip, 80))
    sockobj.close()
    return response == 0

def request(url):
    ''' use the method 'GET' to request the url.
    '''
    component = urlparse(url, scheme="http")
    # 从 url 中提取 hostname 和 path
    if "//" in url:
        hostname = component.netloc.split(":")[0]
        path = component.path
    else:
        hostname = component.path.split("/")[0]
        path = component.path.lstrip(hostname)
    # 从 url 中提取 query
    query = component.query
    conn = http.client.HTTPConnection(hostname)
    conn.request("GET", (path + query) or '/')
    response = conn.getresponse()
    print("\nHTTP/%s %s %s" % (response.version, response.status, response.reason))
    for i in response:
        print(response.readline().decode("utf-8"))
 
if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
        component = urlparse(url, scheme="http")
        # 从 url 中提取 hostname
        if "//" in url:
            hostname = component.netloc.split(":")[0]
        else:
            hostname = component.path.split("/")[0]
        # 通过 DNS 解析 hostname 对应的 ip 
        ip = dns(hostname)
        # step 1
        if ip:
            print("\nSTEP1: the HOSTNAME: %s maps to the IP: %s" % (hostname, ip))
            # step 2
            if ping(ip):
                print("\nSTEP2: succeed in pinging the IP address.")
                # step 3
                if port(ip):
                    print("\nSTEP3: port 80 is fine.")
                    # step 4
                    request(url)
                else:
                    print("\nSTEP3: fail to find port 80.")
            else:
                print("\nSTEP2: fail to ping the IP address")
        else:
            print("\nSTEP1: Please confirm your url.")
    else:
        print("Please enter a url.")
