#/usr/bin/python
import sys
import struct  
import obspy
import pylab
import os

def SearchForPStart(m_data,dot):
	idx=0
	length=len(m_data)
	ave=sum(m_data)/length
	M_data=list()
	for idx in range(0,length):
		M_data.append(m_data[idx]-ave)
		if(M_data[idx]<0):
			M_data[idx]=0-M_data[idx]
	Ave=sum(M_data)/length
	frontA=sum(M_data[0:127])
	frontB=sum(M_data[128:255])
	dot.append(0)
	Max=0
	for idx1 in range(0,(length-256)):
		A=(frontB+4.5*Ave)/(frontA+4.5*Ave)
		if((A>=2) and (Max<A)):
			dot[len(dot)-1]=idx1+128
			Max=A
		if(Max!=0 and idx1==dot[len(dot)-1]+128):
			break
		if(idx1!=length-256):
			frontA-=M_data[idx1]
			frontA+=M_data[idx1+128]
			frontB-=M_data[idx1+128]
			frontB+=M_data[idx1+256]


class sacfile_wave:  
	def read(self,sFile):  
		f=open(sFile,'rb')  
		hdrBin=f.read(632)  

		sfmt='f'*70+'I '*40+'8s '*22+'16s'  
		hdrFmt=struct.Struct(sfmt)  
		self.m_header=hdrFmt.unpack(hdrBin)  

		npts=int(self.m_header[79])
		delta=float(self.m_header[0])
		year=int(self.m_header[70])
		day=int(self.m_header[71])
		hour=int(self.m_header[72])
		minu=int(self.m_header[73])
		sec=int(self.m_header[74])
		msec=int(self.m_header[75])
		resp=float(self.m_header[21])
		fmt_data='f'*npts  
		dataFmt=struct.Struct(fmt_data)  
		dataBin=f.read(4*npts)  
		f.close()  
		self.m_data=dataFmt.unpack(dataBin)  
		print "start time:year day hour minute sec msec:",year,day,hour,minu,sec,msec
		print "data len:",len(self.m_data) 
		print "sample",round(delta,2),"second and time length",npts*round(delta,2),"second"
		print "sensitivity for unit conversion",round(resp,2)


	def draw(self,sImageFile,count):
		dot=list()
		cirdot=list()
		SearchForPStart(self.m_data,dot)
		npts=len(self.m_data)
		xd=range(1,npts+1)
		pylab.figure(count)  
		pylab.plot(xd,self.m_data,linewidth=0.3)
		for DotIdx in dot:
			cirdot.append(self.m_data[DotIdx])
		print dot
		print cirdot
		pylab.plot(dot,cirdot,'ob-')
		pylab.savefig(sImageFile)  

	def exportAsc(self,sAscFile):  
		f2=open(sAscFile,"wt")  
		sdataAsc=[str(x) for x in self.m_data]  
		sDataAsc='\n'.join(sdataAsc)  
		f2.writelines(sDataAsc)  
		f2.close()  

if __name__=="__main__":  

	currentdir = os.getcwd() + "\\example30";
	os.chdir(currentdir);
	filename_list = os.listdir(currentdir)
	count = 0;
	for file in filename_list:
		if(file[-3:]=='SAC'):
			print file
			sac = sacfile_wave()
			sac.read(file)
			sac.draw(file+'.jpg',count)
			#sac.exportAsc(file)
			count += 1
