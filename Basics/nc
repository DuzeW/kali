pobranie tcp
nc 192.168.100.5 10001 > tcpconnect.png
wyslanie
cat tcpconnect.png | nc 192.168.100.5 20001

pobranbie udp
echo | nc -u 192.168.100.5 10002 -w 5 > udpconnect.png
wyslanie
cat udpconnect.png |  nc -u 192.168.100.5 20002 -w 5

nasłuchiwanie pobieranie
nc -lvp 10003 > tcplisten.png

host pliku
cat tcplisten.png |  nc -lvp 20003

nc -luvp 10004 -w 30 > udplisten.png
cat udplisten.png |  nc -ulvp 20004 #CTRL-C po pojawieniu się napisu „UPLOADED”

