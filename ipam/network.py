import subprocess, os, wget
from os import path

class Network():

    def network_scan(subnet):
        x = subprocess.check_output("nmap -sn "+ subnet +""" | grep report | awk '{print $NF}' | sed 's/(//g' | sed 's/)//g' """, shell=True, text=False)
        x_decode = x.decode("utf-8")
        lists_ip = list(filter(None,(x_decode.split("\n"))))
        return lists_ip

    def dns_default_config(id, domain, ip):
        config = [
                "; BIND data file "+domain+"\n\n",
                "$TTL\t604800\n",
                "@\tIN\tSOA\t"+domain+". root."+domain+". (\n",
                "\t\t\t"+str(id)+"\t; Serial\n",
                "\t\t\t604800\t; Refresh\n",
                "\t\t\t86400\t; Retry\n",
                "\t\t\t2419200\t; Expire\n",
                "\t\t\t604800 )\t; Negative Chace TTL\n",
                ";\n",
                "@\tIN\tNS\t"+domain+".\n",
                "@\tIN\tA\t"+str(ip)+"\n\n",
            ]
        return config

    def dns_file_config(id, domain, ip, subdomain):
        config = Network.dns_default_config(id, domain, ip)

        for sub in subdomain:
            config += sub.name+"\t\tIN\t"+sub.type+"\t"+str(sub.ip)+"\n"
            print(config)

        file_config = open(r"/etc/bind/zones/"+domain+".db","r+")
        file_config.writelines(config)
        file_config.close()

        x = subprocess.check_output("service bind9 restart", shell=True, text=False)

        return ''

    def dns_config(domains):

        if path.exists("/etc/bind/zones") is False:
            os.mkdir("/etc/bind/zones")

        config = '# Config File for bind9\n\n'
        for domain in domains:
            config += "zone \""+domain.name+"\" {\n"
            config += "\ttype master;\n"
            config += "\tfile \"/etc/bind/zones/"+domain.name+".db\";\n};\n\n"

            file_dns = Network.dns_default_config(domain.id, domain.name, domain.ip)

            if os.path.isfile("/etc/bind/zones/"+domain.name+".db") is False:   
                file_config = open(r"/etc/bind/zones/"+domain.name+".db","w+")
                file_config.writelines(file_dns)
                file_config.close()

        file_config = open(r"/etc/bind/named.conf.local","w+")
        file_config.truncate(0)
        file_config.writelines(config)
        file_config.close()

        x = subprocess.check_output("service bind9 restart", shell=True, text=False)

        return ''

    def dns_delete(domain):

        if os.path.isfile("/etc/bind/zones/"+domain+".db") is True: 
            os.remove("/etc/bind/zones/"+domain+".db")

        x = subprocess.check_output("service bind9 restart", shell=True, text=False)
        return ''