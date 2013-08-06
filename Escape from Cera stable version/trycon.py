# this works by facing where the 3 screens are

import socket
#-----------------------------------------------------------------------------------------
#Ubisense server ip
UBISERVER="192.168.33.39"
#Ubisense server port
UBIPORT=12000
clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientSocket.connect((UBISERVER,UBIPORT))
sock = clientSocket.makefile("rb") #buffered file (for readline)

counter = 0
xOld = 0
yOld = 0
moveX = ""
moveZ = ""

while(True):
	print "hi"
	data = sock.readline()
	tagId = data[25:28]
	print data
	#if tagId == "68":
		#print("old Y",yOld)
		
	dataPrime = data.split()			
	print dataPrime
	"""z = dataPrime[3]
		x = dataPrime[1]
		
		zP = z[0:3]
		xP = x[0:4]
		
		xNew = float(xP)
		zNew = float(zP)
		
		if counter == 0:
			xOld = xNew
			zOld = zNew
			counter = 1
		
		if xOld != xNew:
			if xOld < xNew:
				moveX ="down"
			elif xOld > xNew:
				moveX = "up"
			xOld = xNew
			
			
		if zOld != zNew:
			if zOld < zNew:
				moveZ ="right"
			elif zOld > zNew:
				moveZ = "left"
			zOld = zNew
			
		print (zNew)"""
		#print moveY
		#print("new Y",yNew)
#-----------------------------end while--------------------------------------------------------	
#except error,errval:
	#print str(errval)
#if not DEBUG:
#	quit()
# x / y /z			
#000000000000000020000007068 33.010555267334 0.732201278209686 5.19519090652466	
		