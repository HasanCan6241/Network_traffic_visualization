import dpkt
import socket
import pygeoip
import folium
import  requests

gi = pygeoip.GeoIP('maxmind4.dat')
hedef_enlem=[]
hedef_boylam=[]
kaynak=[]
hedef=[]
ıp="193.255.125.93"
#print(socket.gethostbyname(socket.gethostname()))

def donustur_KML(dstip, srcip):
    dst = gi.record_by_name(dstip)
    src = gi.record_by_name(ıp)
    try:
        src_enlemi = src['latitude']
        dst_boylamı = dst['longitude']
        dst_enlemi = dst['latitude']
        src_boylamı = src['longitude']
        hedef_enlem.append(dst_enlemi)
        hedef_boylam.append(dst_boylamı)
        kml = (
                  '<Placemark>\n'
                  '<name>%s</name>\n'
                  '<extrude>1</extrude>\n'
                  '<tessellate>1</tessellate>\n'
                  '<styleUrl>#transBluePoly</styleUrl>\n'
                  '<LineString>\n'
                  '<coordinates>%6f,%6f\n%6f,%6f</coordinates>\n'
                  '</LineString>\n'
                  '</Placemark>\n'
              ) % (dstip, dst_boylamı, dst_enlemi, src_boylamı, src_enlemi)
        kaynak.append(srcip)
        hedef.append(dstip)
        return kml

    except:
        return ''


def ıp_cıkar(pcap):
    kmlPts = ''
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            KML = donustur_KML(dst, src)
            kmlPts = kmlPts + KML
        except:
            pass
    return kmlPts
    #ıp_cıkar()

def main():
    f = open('wire.pcap', 'rb')
    pcap = dpkt.pcap.Reader(f)
    kmlheader = '<?xml version="1.0" encoding="UTF-8"?> \n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'\
    '<Style id="transBluePoly">' \
                '<LineStyle>' \
                '<width>1.5</width>' \
                '<color>501400E6</color>' \
                '</LineStyle>' \
                '</Style>'
    kmlfooter = '</Document>\n</kml>\n'
    kmldoc=kmlheader+ıp_cıkar(pcap)+kmlfooter
    print(kmldoc)

if __name__ == '__main__':
    main()


#verileri okuma
"""import csv
sure=[]
protokol=[]

with open('wire_Analiz.csv', 'r') as file:

    rows = csv.reader(file)
    for row in rows:

        if row[1]=="Time":
            continue
        for i in range(0, len(hedef)):
            if hedef[i]==row[3]:
                print("Kaynak:{}".format(row[2]))

                print("Hedef:{}".format(row[3]))

                print("Süre:{}".format(row[1]))
                sure.append(row[1])
                print("Protokol:{}".format(row[4]))
                protokol.append(row[4])
                print("---------")"""


#verileri haritalaştırma
m = folium.Map(location=[38.67784186176803, 39.201955583215835])
r = requests.get("https://api.iplocation.net/?cmd=ip-country&ip={}".format(kaynak[0]))
text = r.text
iframe = folium.IFrame("<h1><strong>{}</strong></h1><p><br/>"
                           "Ip Versiyon :{} <br/>"
                           "Ülke Adı :{} <br/>"
                           "İnternet Sağlayıcısı :{} <br/>"
                           "</p>".format("Kullanıcı Ip",r.text.split(",")[2],r.text.split(",")[3],r.text.split(",")[5]))
popup = folium.Popup(iframe,
                         min_width=290,
                         max_width=290)
folium.Marker(location=[38.67784186176803, 39.201955583215835], popup=popup,tooltip="Kullanıcı Ip").add_to(m)
m.save("Ağ_trafiği.html")

for i in range(0,len(hedef_enlem)):
    x = str(hedef_enlem[i])
    y = str(hedef_boylam[i])
    a = x + "," + y
    lat=x
    long=y
    r = requests.get("https://api.iplocation.net/?cmd=ip-country&ip={}".format(hedef[i]))
    text = r.text
    iframe = folium.IFrame("<h1><strong>{}</strong></h1><p><br/>"
                           "kaynak ıp : {}<br/>"
                           "Yakalanan hedef ıp :{} <br/>"
                           "Ip Versiyon :{} <br/>"
                           "Ülke Adı :{} <br/>"
                           "İnternet Sağlayıcısı :{} <br/>"
                           "</p>".format("Yakalanan Ağ", kaynak[i], hedef[i],r.text.split(",")[2],r.text.split(",")[3],r.text.split(",")[5]))
    popup = folium.Popup(iframe,
                         min_width=290,
                         max_width=290)
    folium.Marker(location=[lat,long], popup =popup,icon=folium.Icon(color="red",icon='info-sign'),tooltip="Yakalanan Ağ").add_to(m)
    folium.CircleMarker(location=[lat,long],radius=15,color="green").add_to(m)
    folium.PolyLine([[38.67784186176803, 39.201955583215835],
                     [lat, long]],color="orange").add_to(m)
    m.save("Ağ_trafiği.html")



