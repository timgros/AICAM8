import pyshark

capture = pyshark.LiveCapture(interface = 'eth0')

capture.sniff(timeout=1)

print(capture)