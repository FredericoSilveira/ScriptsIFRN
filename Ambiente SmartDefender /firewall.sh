#! /bin/sh

### BEGIN INIT INFO
# Provides:             firewall
# Required-Start:       $remote_fs $syslog
# Required-Stop:        $remote_fs $syslog
# Default-Start:        2 3 4 5
# Default-Stop:
# Short-Description:    Firewall script
### END INIT INFO

INT_IFACE="eth1"
INT_ADDR="172.16.10.1"
INT_NET="172.16.0.0/16"

DTI_IFACE="eth7"
DTI_NET="10.7.98.0/24"

EXT_IFACE="eth0"
EXT_ADDR="10.7.162.66"
EXT_NET="10.7.162.66/27"



fw_load_modules(){
        # Load modules
        modprobe ip_tables
        modprobe ip_conntrack
        modprobe iptable_filter
        modprobe iptable_mangle
        modprobe iptable_nat
        modprobe ipt_LOG
        modprobe ipt_limit
        modprobe ipt_state
        modprobe ipt_REDIRECT
        modprobe ipt_owner
        modprobe ipt_REJECT
        modprobe ipt_MASQUERADE
        modprobe ip_conntrack_ftp
        modprobe ip_nat_ftp
}

fw_reset_police(){
        # Flush rules
        iptables -X
        iptables -Z
        iptables -F INPUT
        iptables -F OUTPUT
        iptables -F FORWARD
        iptables -F -t nat
        iptables -F -t mangle

        iptables -t filter -P INPUT ACCEPT #DROP
        iptables -t filter -P OUTPUT ACCEPT
        iptables -t filter -P FORWARD ACCEPT #DROP
                iptables -t nat -P PREROUTING ACCEPT
        iptables -t nat -P OUTPUT ACCEPT
        iptables -t nat -P POSTROUTING ACCEPT
        iptables -t mangle -P PREROUTING ACCEPT
        iptables -t mangle -P OUTPUT ACCEPT

        #Enable Forwad
        #echo 0 > /proc/sys/net/ipv4/ip_forward
        echo 1 > /proc/sys/net/ipv4/ip_forward
}

fw_start(){
        echo "Starting..."
        fw_reset_police
        fw_load_modules

        iptables -t filter -P INPUT DROP
        iptables -t filter -P OUTPUT ACCEPT
        #iptables -t filter -P FORWARD DROP
        iptables -t filter -P FORWARD ACCEPT
        iptables -t nat -P PREROUTING ACCEPT
        iptables -t nat -P OUTPUT ACCEPT
        iptables -t nat -P POSTROUTING ACCEPT
        iptables -t mangle -P PREROUTING ACCEPT
        iptables -t mangle -P OUTPUT ACCEPT

        #Enable Forwad
        echo 1 > /proc/sys/net/ipv4/ip_forward

        # Basic reletionship conections
        iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
        iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT
        iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

        iptables -A INPUT -p icmp -j ACCEPT

        # loopback
        iptables -t filter -A INPUT -s 127.0.0.0/16 -j ACCEPT

        ###############################
        ### Local Services ###

        # Port 4422 (SSH)
        iptables -A INPUT -s $INT_NET -j ACCEPT
        #iptables -A INPUT -p tcp --dport 4422 -j ACCEPT
        # Port 80,8080,443 (HTTP) / rabbit-server/Zabbix
        iptables -A INPUT  -p tcp -m multiport --dport 80,443,4422 -j ACCEPT
        #iptables -A INPUT  -p tcp -m multiport --dport 80,8080,5671,5672 -j ACCEPT


        ###############################
        ### Forward  ###

        iptables -A FORWARD -p all -s $INT_NET -j ACCEPT
        iptables -A FORWARD -p all -d $INT_NET -j ACCEPT

        iptables -A FORWARD -p all -s $DTI_NET -j ACCEPT
        iptables -A FORWARD -p all -d $DTI_NET -j ACCEPT

        ###############################
        # Hyper-V
        iptables -A FORWARD -p tcp -s 10.7.162.74 -j ACCEPT
        iptables -A FORWARD -p tcp -d 10.7.162.74 -j ACCEPT

        iptables -t nat -A PREROUTING -p tcp --dport 3390 -i $EXT_IFACE -j DNAT --to 10.7.162.74:3389
        iptables -t nat -A POSTROUTING -p tcp --dport 3389 -o $EXT_IFACE -j SNAT --to $EXT_ADDR:3390

        # Zabbix
        iptables -t nat -A PREROUTING -p tcp --dport 10050 -i $EXT_IFACE -j DNAT --to 172.16.10.202:10050
        iptables -t nat -A PREROUTING -p tcp --dport 10051 -i $EXT_IFACE -j DNAT --to 172.16.10.202:10051
        #iptables -t nat -A POSTROUTING -p tcp --dport 10050 -o $EXT_IFACE -j SNAT --to $EXT_ADDR:10050

        # RabbitMQ
        iptables -t nat -A PREROUTING -p tcp --dport 8080 -i $EXT_IFACE -j DNAT --to 172.16.20.157:8080
        iptables -t nat -A PREROUTING -p tcp --dport 5672 -i $EXT_IFACE -j DNAT --to 172.16.20.157:5672
        iptables -t nat -A PREROUTING -p tcp --dport 15672 -i $EXT_IFACE -j DNAT --to 10.7.40.225:15672



        # NAT INT <-> EXT
        iptables -t nat -A POSTROUTING -s $INT_NET -o $EXT_IFACE -j MASQUERADE



}

fw_stop(){
        echo "Stoping..."
        fw_reset_police
}
fw_list(){
        echo "Listing..."
        echo " ===================== Filter table =========================="
        iptables -n -L -t filter
        echo " ====================== Nat table ============================"
        iptables -n -L -t nat
        echo " ============================================================="
}


case "$1" in
  start)
        fw_start
        ;;
  stop)
        fw_stop
        ;;
  reload|restart)
        fw_stop
        fw_start
        ;;
  list)
        fw_list
        ;;
    *)
        # failed to stop
        echo "Usage: firewall stop | start | restart | list"
        ;;
esac
exit 0
