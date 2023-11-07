import os
from bitarray import bitarray
from bitarray.util import ba2int
from bitarray.util import int2ba
from pynput import keyboard
import time
import serial

'''LUT = [ ( bitarray('1110 1010', endian='big') , e.nop ) , ( bitarray('1110 1010', endian='big') , e.dex ),
			( bitarray('1011 1010', endian='big') , e.tsx ) , ( bitarray('1110 1010', endian='big') , e.tax ),
			( bitarray('1001 1010', endian='big') , e.txs ) , ( bitarray('1000 1010', endian='big') , e.txa ),
			( bitarray('1011 1000', endian='big') , e.clv ) , ( bitarray('1001 1000', endian='big') , e.tya ),

			( bitarray('0111 1000', endian='big') , e.sei ) , ( bitarray('0101 1000', endian='big') , e.cli ),
			( bitarray('0011 1000', endian='big') , e.sec ) , ( bitarray('0001 1000', endian='big') , e.clc ),
			( bitarray('1110 1000', endian='big') , e.inx ) , ( bitarray('1100 1000', endian='big') , e.iny ),
			( bitarray('1010 1000', endian='big') , e.tay ) , ( bitarray('1000 1000', endian='big') , e.dey ),

			( bitarray('0110 1000', endian='big') , e.pla )         , ( bitarray('0100 1000', endian='big') , e.pha ),
			( bitarray('0010 1000', endian='big') , e.plp )         , ( bitarray('0000 1000', endian='big') , e.php ),
			( bitarray('0110 0000', endian='big') , e.rts )         , ( bitarray('0100 0000', endian='big') , e.rti ),
			( bitarray('0010 0000', endian='big') , e.jsrAbsolute ) , ( bitarray('0000 0000', endian='big') , e.brk ),

			( bitarray('1111 0000', endian='big') , e.beq ) , ( bitarray('1101 0000', endian='big') , e.bne ),
			( bitarray('1011 0000', endian='big') , e.bcs ) , ( bitarray('1001 0000', endian='big') , e.bcc ),
			( bitarray('0111 0000', endian='big') , e.bvs ) , ( bitarray('0101 0000', endian='big') , e.bvc ),
			( bitarray('0011 0000', endian='big') , e.bmi ) , ( bitarray('0001 0000', endian='big') , e.bpl ),

			( bitarray('111x xx00', endian='big') , e.cpx )         , ( bitarray('110x xx00', endian='big') , e.cpy ), 
			( bitarray('101x xx00', endian='big') , e.ldy )         , ( bitarray('100x xx00', endian='big') , e.sty ), 
			( bitarray('011x xx00', endian='big') , e.jmpAbsolute ) , ( bitarray('010x xx00', endian='big') , e.jmp ),
			( bitarray('001x xx00', endian='big') , e.bit ),

			( bitarray('111x xx10', endian='big') , e.inc ) , ( bitarray('110x xx10', endian='big') , e.dec ),
			( bitarray('101x xx10', endian='big') , e.ldx ) , ( bitarray('100x xx10', endian='big') , e.stx ),
			( bitarray('011x xx10', endian='big') , e.ror ) , ( bitarray('010x xx10', endian='big') , e.lsr ),
			( bitarray('001x xx10', endian='big') , e.rol ) , ( bitarray('000x xx10', endian='big') , e.asl ),

			( bitarray('111x xx01', endian='big') , e.sbc )         , ( bitarray('110x xx01', endian='big') , e.cmp ),
			( bitarray('101x xx01', endian='big') , e.lda )         , ( bitarray('100x xx01', endian='big') , e.sta ),
			( bitarray('011x xx01', endian='big') , e.adc )         , ( bitarray('010x xx01', endian='big') , e.eor ),
			( bitarray('001x xx01', endian='big') , e.andInstruct ) , ( bitarray('000x xx01', endian='big') , e.ora ) ]'''
debugPrints = True

class _registers:
	global mem
	global debugPrints
	def __init__(self):
		self.PC = bitarray('0000 0000 0000 0000', endian='big')
		self.stackPoint = bitarray('0000 0000', endian='big')
		self.acc = bitarray('0000 0000', endian='big')
		self.regX = bitarray('0000 0000', endian='big')
		self.regY = bitarray('0000 0000', endian='big')
		self.flagReg = bitarray('0010 0000', endian='big')
		self.ones = bitarray('1111 1111', endian='big')
		#self.zeros = bitarray('0000 0000', endian='big')
		self.instructReg = bitarray('0000 0000', endian='big')
		self.savedPC = self.PC
		self.stackStart = bitarray('0000 0001 0000 0000')
		self.IOStart = bitarray('0000 0010 0000 0000')
	def zeros(self):
		return bitarray('0000 0000', endian='big')
	def savePC(self):
		self.savedPC = self.PC
	def restorePC(self):
		self.PC = self.savedPC
	def setPCLow(self,inp):
		self.PC[8:] = inp
	def setPCHigh(self,inp):
		self.PC[:8] = inp
	def getPCLow(self):
		return self.PC[8:]
	def getPCHigh(self):
		return self.PC[:8]
	def incPC(self):
		h=self.PC
		x = ba2int(h)
		x+=1
		ba = int2ba(x,endian='big')
		buffer = bitarray('0000 0000 0000 0000', endian='big')
		index = len(ba)
		bi=16
		while index > 0:
			index-=1
			bi-=1
			buffer[bi]=ba[index]
		self.PC = buffer
	def iFlag(self, setVal = None):
		if setVal is None:
			return self.flagReg[5]
		else:
			self.flagReg[5] = setVal
			return self.flagReg[5]
	def cFlag(self, setVal = None):
		if setVal is None:
			return self.flagReg[7]
		else:
			self.flagReg[7] = setVal
			return self.flagReg[7]
	def zFlag(self, setVal = None):
		if setVal is None:
			return self.flagReg[6]
		else:
			self.flagReg[6] = setVal
			return self.flagReg[6]
	def nFlag(self, setVal = None):
		if setVal is None:
			return self.flagReg[0]
		else:
			self.flagReg[0] = setVal
			return self.flagReg[0]
	def vFlag(self, setVal = None):
		if setVal is None:
			return self.flagReg[1]
		else:
			self.flagReg[1] = setVal
			return self.flagReg[1]
	def setInstructionReg(self):
		self.instructReg = mem.readAddress(ba2int(r.PC))
		if(debugPrints):
			print("Read instruction on "+str(ba2int(r.PC))+": "+str(self.instructReg))
class _memory:
	global r
	global ALU
	global l
	global debugPrints
	def __init__(self):
		self.memoryBlock = bitarray(524288,endian='big')
		self.address = bitarray('0000 0000 0000 0000',endian='big')
		self.eStart = (ba2int(self.address)*8)
		self.eStop = self.eStart+8
		self.accMode = False
		self.resetVector = bitarray('0000 0000 0000 0000',endian='big')
		self.nmiVector = bitarray('0000 1111 0000 0000',endian='big')
		self.irqVector = bitarray('0000 1100 0000 0000',endian='big')
		
		self.addIndex = 0


	def importPROG(self,prog,startIndex):
		i=0
		j=0
		while i*8 < len(prog):
			self.writeAddress(i+startIndex,prog[j:j+8])
			i+=1
			j+=8
		i=0
		while i*8 < len(prog):
			if(debugPrints):
				print(i+startIndex,self.readAddress(i+startIndex))
			i+=1
		return prog

	
	def readAddress(self, inAddress):
		if(type(inAddress) != int):
			inAddress = ba2int(inAddress)
		start = inAddress * 8
		inAddress += 1
		stop = inAddress * 8
		if(self.accMode):
			return r.acc
		return self.memoryBlock[start:stop]
	def writeAddress(self, inAddress, data):
		if(type(inAddress) != int):
			inAddress = ba2int(inAddress)
		start = inAddress * 8
		inAddress += 1
		stop = inAddress * 8
		if(self.accMode):
			r.acc = data
		self.memoryBlock[start:stop] = data


	def zeroPageX(self):
		self.accMode = False
		if(debugPrints):
			print('Run zeroPageX')
		r.incPC()
		l = self.readAddress(r.PC)
		l = ba2int(l) + ba2int(r.regX)
		if(l>255):
			l -= 128
		r.incPC()
		return(l)
	def zeroPage(self):	
		self.accMode = False
		if(debugPrints):
			print('Run zeroPage')
		r.incPC()
		l = self.readAddress(r.PC)
		r.incPC()
		return ba2int(l)
	def absoluteX(self):
		self.accMode = False
		if(debugPrints):
			print('Run absoluteX')
		r.incPC()
		h = self.readAddress(r.PC)
		r.incPC()
		l = self.readAddress(r.PC)
		index = ba2int(h+l)
		index = index + ba2int(r.regX)
		r.incPC()
		return(index)
	def immediate(self):
		self.accMode = False
		if(debugPrints):
			print('Run immediate')
		r.incPC()
		out = ba2int(r.PC)
		r.incPC()
		return(out)
	def absolute(self):
		self.accMode = False
		if(debugPrints):
			print('Run absolute')
		r.incPC()
		h = self.readAddress(r.PC)
		r.incPC()
		l = self.readAddress(r.PC)
		r.incPC()
		return ba2int(h+l)
	def zeroPageY(self):
		self.accMode = False
		if(debugPrints):
			print('Run zeroPageY')
		r.incPC()
		l = self.readAddress(r.PC)
		l = ba2int(l) + ba2int(r.regY)
		if(l>255):
			l -= 128
		r.incPC()
		return(l)
	def indirectX(self):
		r.incPC()
		h = self.readAddress(r.PC)
		r.incPC()
		l = self.readAddress(r.PC)
		xIndexed = ba2int(h+l) + ba2int(r.regX)
		h = self.readAddress(xIndexed)
		l = self.readAddress(xIndexed+1)
		r.incPC()
		return(ba2int(h+l))
	def absoluteY(self):
		self.accMode = False
		if(debugPrints):
			print('Run absoluteX')
		r.incPC()
		h = self.readAddress(r.PC)
		r.incPC()
		l = self.readAddress(r.PC)
		index = ba2int(h+l)
		index = index + ba2int(r.regY)
		r.incPC()
		return(index)
	def accumulator(self):
		if(debugPrints):
			print('Run accumulator')
		self.accMode = True
		r.incPC()
		return 0
	def relative(self):
		self.accMode = False
		r.incPC()
		if(debugPrints):
			print('Run relative')
		return(ba2int(r.PC))
	def implied(self):
		self.accMode = False
		r.incPC()
		if(debugPrints):
			print('Run implied')
		return(ba2int(r.PC))


	def getResetV(self):
		return bitarray('1000 0000 0000 0000',endian='big')
	def getNMIV(self):
		return self.readAddress(bitarray('1111 1111 1111 1010',endian='big')) + self.readAddress(bitarray('1111 1111 1111 1011',endian='big'))
	def getIRQV(self):
		return bitarray('1000 0000 0000 0000',endian='big')
class _ALU:
	global r
	global debugPrints
	def cheatAdder(self,a,b,cIn):
		a = ba2int(a)
		b=ba2int(b)
		c=ba2int(cIn)
		s = a+b+c
		s = int2ba(s,endian='big')
		if(len(s)>8):
			return s[1:], s[:1]
		while(len(s)<8):
			s = bitarray('0',endian='big') + s
		return s, bitarray('0',endian='big')


	def fullAdder(self,a,b,cIn):
			hXor = a^b
			hOut = a&b
			s = hXor^cIn
			fOut = hXor&cIn
			cOut = fOut | hOut
			return s,cOut
	def addOffset(self,high,low,offset):
		sL, c = self.addVal(low,offset,carry=0,flags=False)
		sH, c = self.addVal(high,r.zeros(),carry=c,flags=False)
		return sH, sL
	def addVal(self, data1, data2, carry = None, flags = True, cFlag=True, zFlag=True, nFlag=True, vFlag=True):
		if carry is None:
			cIn = r.flagReg[7]
		else:
			cIn = carry
		out = r.zeros()
		out[7], cIn = self.fullAdder(data1[7],data2[7],cIn)
		out[6], cIn = self.fullAdder(data1[6],data2[6],cIn)
		out[5], cIn = self.fullAdder(data1[5],data2[5],cIn)
		out[4], cIn = self.fullAdder(data1[4],data2[4],cIn)
		out[3], cIn = self.fullAdder(data1[3],data2[3],cIn)
		out[2], cIn = self.fullAdder(data1[2],data2[2],cIn)
		out[1], cIn = self.fullAdder(data1[1],data2[1],cIn)
		out[0], cOut = self.fullAdder(data1[0],data2[0],cIn)
		if(flags):
			if(vFlag):    #FIX THIS FLAG
				pass
			if(cFlag):
				r.cFlag(setVal=cOut)
			if(nFlag):
				r.nFlag(setVal=out[0])
			if(zFlag):
				r.zFlag(setVal=out.any())
		if carry is None:
			return out
		else:
			return out, cOut
	def subVal(self, data1, data2, carry = None, flags = True, cFlag=True, zFlag=True, nFlag=True, vFlag=True):
		if carry is None:            # RATHER THAN SETTING THE CARRY TO 1 FOR SUB WE'RE JUST INCREMENTING D1
			cIn = r.flagReg[7]       # THIS LETS US TAKE IN A CARRY
		else:
			cIn = carry
		data1 = self.incVal(data1)
		data2 = data2^r.ones
		out = r.zeros()
		out[7], cIn = self.fullAdder(data1[7],data2[7],cIn)
		out[6], cIn = self.fullAdder(data1[6],data2[6],cIn)
		out[5], cIn = self.fullAdder(data1[5],data2[5],cIn)
		out[4], cIn = self.fullAdder(data1[4],data2[4],cIn)
		out[3], cIn = self.fullAdder(data1[3],data2[3],cIn)
		out[2], cIn = self.fullAdder(data1[2],data2[2],cIn)
		out[1], cIn = self.fullAdder(data1[1],data2[1],cIn)
		out[0], cOut = self.fullAdder(data1[0],data2[0],cIn)
		if(flags):
			if(vFlag):    #FIX THIS FLAG
				pass
			if(cFlag):
				r.flagReg[7] = cOut
			if(nFlag):
				r.flagReg[0] = out[0]
			if(zFlag):
				r.flagReg[6] = out.any() ^ r.ones[1]
		if carry is None:
			return out
		else:
			return out, cOut
	def add(self, data):
		r.acc = self.addVal(r.acc, data)
	def sub(self, data):
		r.acc = self.subVal(r.acc, data)
	def incVal(self, data, retCarry = False, flags = False, cFlag=False, zFlag=False, nFlag=False, vFlag=False):
		s, c = self.addVal(data, r.zeros(), carry = r.ones[0], flags=flags, cFlag=cFlag, zFlag=zFlag, nFlag=nFlag, vFlag=vFlag)
		if(retCarry):
			return s,c
		return s
	def decVal(self, data, retCarry = False, flags = False, cFlag=False, zFlag=False, nFlag=False, vFlag=False):
		s, c = self.addVal(data, r.ones, carry = r.zeros()[0], flags=flags, cFlag=cFlag, zFlag=zFlag, nFlag=nFlag, vFlag=vFlag)
		if(retCarry):
			return s,c
		return s
	def lsrVal(self, data):
		val = data + r.zeros()[0]
		val >>= 1
		r.cFlag(setVal = val[8])
		return(val[:8])
	def aslVal(self, data):
		val = r.zeros()[0] + data
		val <<= 1
		r.cFlag(setVal = val[0])
		return(val[1:])
	def rorVal(self,data):
		val = r.flagReg[7] + data + r.zeros()[0]
		val >>= 1
		r.cFlag(setVal = val[9])
		return val[1:9]
	def rolVal(self,data):
		val = r.zeros()[0] + data + r.flagReg[7]
		val <<= 1
		r.cFlag(setVal = val[0])
		return val[1:9]
	def andAcc(self,data):
		r.acc &= data 
		r.nFlag(setVal=r.acc[0])
		r.zFlag(setVal=r.acc.any())
	def bitTest(self,data):
		r.nFlag(setVal=data[0])
		r.vFlag(setVal=data[1])
		data &= r.acc
		r.zFlag(setVal=data.any())
	def eorAcc(self,data):
		r.acc ^= data 
		r.nFlag(setVal=r.acc[0])
		r.zFlag(setVal=r.acc.any())
	def oraAcc(self,data):
		r.acc |= data 
		r.nFlag(setVal=r.acc[0])
		r.zFlag(setVal=r.acc.any())
	def cmpVal(self,data1,data2):
		data1, carry = subVal(self, data1, data2, carry = 0, flags = True, cFlag=True, zFlag=True, nFlag=True, vFlag=False)
		return zFlag()
class _execute:
	global debugPrints
	def __init__(self):
		global r
		global ALU
	def rti(self,offSet):
		if(debugPrints):
			print('Run RTI')
	def bpl(self,offSet):          #DONE
		if(debugPrints):
			print('Run BPL')
		if(r.nFlag()==r.zeros()[1]):
			data = mem.readAddress(offSet)
			high, low = ALU.addOffset(r.getPCHigh(),r.getPCLow(),data)
			r.setPC = high + low
	def bmi(self,offSet):        #DONE
		if(debugPrints):
			print('Run BMI')
		if(r.nFlag()==r.ones[1]):
			data = mem.readAddress(offSet)
			high, low = ALU.addOffset(r.getPCHigh(),r.getPCLow(),data)
			r.PC = high + low
	def bvc(self,offSet):          #DONE
		if(debugPrints):
			print('Run BVC')
		if(r.vFlag()==r.zeros()[1]):
			data = mem.readAddress(offSet)
			high, low = ALU.addOffset(r.getPCHigh(),r.getPCLow(),data)
			r.PC = high + low
	def bvs(self,offSet):        #DONE
		if(debugPrints):
			print('Run BVS')
		if(r.vFlag()==r.ones[1]):
			data = mem.readAddress(offSet)
			high, low = ALU.addOffset(r.getPCHigh,r.getPCLow,data)
			r.PC = high + low
	def bcc(self,offSet):        #DONE
		if(debugPrints):
			print('Run BCC')
		if(r.cFlag()==r.zeros()[1]):
			data = mem.readAddress(offSet)
			high, low = ALU.addOffset(r.getPCHigh,r.getPCLow,data)
			r.PC = high + low
	def bcs(self,offSet):        #DONE
		if(debugPrints):
			print('Run BCS')
		if(r.cFlag()==r.ones[1]):
			data = mem.readAddress(offSet)
			high, low = ALU.addOffset(r.getPCHigh,r.getPCLow,data)
			r.PC = high + low
	def bne(self,offSet):         #DONE
		if(debugPrints):
			print('Run BNE')
		if(r.zFlag()==r.zeros()[1]):
			data = mem.readAddress(offSet)
			high, low = ALU.addOffset(r.getPCHigh,r.getPCLow,data)
			r.PC = high + low
	def beq(self,offSet):          #DONE
		if(debugPrints):
			print('Run BEQ')
		if(r.zFlag()==r.ones[1]):
			data = mem.readAddress(offSet)
			high, low = ALU.addOffset(r.getPCHigh,r.getPCLow,data)
			r.PC = high + low
	def brk(self,offSet):
		if(debugPrints):
			print('Run BRK')
		if(debugPrints):
			print('RUNNING OS._EXIT')
		os._exit(1)
	def jsrAbsolute(self,offSet):           
		h = r.PC[:8]
		l = r.PC[8:]
		mem.writeAddress(ba2int(r.stackPoint) + ba2int(r.stackStart), l)
		r.stackPoint = incVal(r.stackPoint) 
		mem.writeAddress(ba2int(r.stackPoint) + ba2int(r.stackStart), h)
		r.stackPoint = incVal(r.stackPoint)
		r.incPC()
		hD = mem.readAddress(r.PC)
		r.incPC()
		lD = mem.readAddress(r.PC)
		r.PC = hD + lD


	def rts(self,offSet):
		h = mem.readAddress(ba2int(r.stackPoint) + ba2int(r.stackStart))
		r.stackPoint = ALU.decVal(r.stackPoint)   
		l = mem.readAddress(ba2int(r.stackPoint) + ba2int(r.stackStart))
		r.stackPoint = ALU.decVal(r.stackPoint) 
		r.PC = h + l

	def php(self,offSet):
		mem.writeAddress(ba2int(r.stackPoint) + ba2int(r.stackStart), r.flagReg)
		r.stackPoint = ALU.incVal(r.stackPoint)        
	def plp(self,offSet):
		r.flagReg = mem.readAddress(ba2int(r.stackPoint) + ba2int(r.stackStart))
		r.stackPoint = ALU.decVal(r.stackPoint)      
	def pha(self,offSet):
		mem.writeAddress(ba2int(r.stackPoint) + ba2int(r.stackStart), r.acc)
		r.stackPoint = ALU.incVal(r.stackPoint)        
	def pla(self,offSet):
		r.acc = mem.readAddress(ba2int(r.stackPoint) + ba2int(r.stackStart))
		r.stackPoint = ALU.decVal(r.stackPoint) 
	def dey(self,offSet):         #DONE
		if(debugPrints):
			print('Run DEY')
		r.regY = ALU.decVal(regY)
	def tay(self,offSet):                #DONE
		if(debugPrints):
			print('Run TAY')
		r.regY = r.acc
	def iny(self,offSet):     #DONE
		if(debugPrints):
			print('Run INY')
		r.regY = ALU.incVal(regY)
	def inx(self,offSet):      #DONE
		if(debugPrints):
			print('Run INX')
		r.regX = ALU.incVal(r.regX)
	def clc(self,offSet):          #DONE
		if(debugPrints):
			print('Run CLC')
		r.cFlag(setVal=r.zeros()[0])
	def sec(self,offSet):         #DONE
		if(debugPrints):
			print('Run SEC')
		r.cFlag(setVal=r.ones[0])
	def cli(self,offSet):        	#DONE
		if(debugPrints):
			print('Run CLI')
		r.iFlag(setVal=r.zeros()[0])
	def sei(self,offSet):          #DONE
		if(debugPrints):
			print('Run SEI')
		r.iFlag(setVal=r.ones[0])
	def tya(self,offSet):              #DONE
		if(debugPrints):
			print('Run TYA')
		r.acc = r.regY
	def clv(self,offSet):          #DONE
		if(debugPrints):
			print('Run CLV')
		r.vFlag(setVal=r.zeros()[0])
	def txa(self,offSet):          #DONE
		if(debugPrints):
			print('Run TXA')
		r.acc = r.regX
	def txs(self,offSet):               #DONE
		if(debugPrints):
			print('Run TXS')
		r.stackPoint = r.regX
	def tax(self,offSet):               #DONE
		if(debugPrints):
			print('Run TAX')
		r.regX = r.acc
	def tsx(self,offSet):      #DONE
		if(debugPrints):
			print('Run TSX')
		r.regX = r.stackPoint
	def dex(self,offSet):          #DONE
		if(debugPrints):
			print('Run DEX')
		r.regX = ALU.decVal(r.regX)
	def nop(self,offSet):
		if(debugPrints):
			print('Run NOP')
	def bit(self,offSet):       #DONE
		if(debugPrints):
			print('Run BIT')
		data = mem.readAddress(offSet)
		r.nFlag(setVal=data[0])
		r.vFlag(setVal=data[1])
		data &= r.acc
		ALU.addVal(self,offSet, data, r.zeros(), carry = r.zeros()[0], flags = True, cFlag=False, zFlag=True, nFlag=False, vFlag=False)
	def jmp(self,offSet):                  #DONE
		if(debugPrints):
			print('Run JMP')
		highPart = mem.readAddress(offSet)
		r.incPC()
		lowPart = mem.readAddress(offSet)
		r.PC = highPart+lowPart
	def jmpAbsolute(self,offSet):                    #DONE
		if(debugPrints):
			print('Run JMP abs')
		highPart = mem.readAddress(offSet)
		lowPart = mem.readAddress(offSet+1)
		r.PC = highPart+lowPart
	def sty(self,offSet):              #DONE
		if(debugPrints):
			print('Run STY')
		mem.writeAddress(offSet,r.regY)
	def ldy(self,offSet):              #DONE
		if(debugPrints):
			print('Run LDY')
		data = mem.readAddress(offSet)
		r.regY = data
	def cpy(self,offSet):            #DONE
		if(debugPrints):
			print('Run CPY')
		data = mem.readAddress(offSet)
		ALU.cmpVal(data,regY)
	def cpx(self,offSet):            #DONE
		if(debugPrints):
			print('Run CPX')
		data = mem.readAddress(offSet)
		ALU.cmpVal(data,regX)
	def ora(self,offSet):            #DONE
		if(debugPrints):
			print('Run ORA')
		data = mem.readAddress(offSet)
		r.acc |= data
		ALU.add(r.zeros())
	def eor(self,offSet):        #DONE
		if(debugPrints):
			print('Run EOR')
		data = mem.readAddress(offSet)
		r.acc ^= data
		ALU.add(r.zeros())
	def sta(self,offSet):        #DONE
		if(debugPrints):
			print('Run STA')
		mem.writeAddress(offSet,r.acc)
	def cmp(self,offSet):       #DONE
		if(debugPrints):
			print('Run CMP')
		data = mem.readAddress(offSet)
		ALU.cmpVal(data,r.acc)
	def andInstruct(self,offSet):    #DONE
		if(debugPrints):
			print('Run AND')
		data = mem.readAddress(offSet)
		ALU.andAcc(data)
	def adc(self,offSet):   #DONE
		if(debugPrints):
			print('Run ADC')
		data = mem.readAddress(offSet)
		if(debugPrints):
			print('ADC DATA',data)
		sOut = ALU.addVal(data, r.acc)
		if(debugPrints):
			print('sOut:',sOut)
		r.acc = sOut
	def lda(self,offSet):          #DONE
		if(debugPrints):
			print('Run LDA, offset=',offSet)
		data = mem.readAddress(offSet)
		r.acc = data
		if(debugPrints):
			print('IN LDA acc: ',r.acc)
	def sbc(self,offSet):              #DONE
		if(debugPrints):
			print('Run SBC')
		data = mem.readAddress(offSet)
		ALU.sub(data)
	def asl(self,offSet):     #DONE
		if(debugPrints):
			print('Run ASL')
		data = mem.readAddress(offSet)
		data = ALU.aslVal(data)
		mem.writeAddress(offSet,data)
	def rol(self,offSet):                #DONE
		if(debugPrints):
			print('Run ROL')
		data = mem.readAddress(offSet)
		data = ALU.rolVal(data)
		mem.writeAddress(offSet,data)
	def lsr(self,offSet):                    #DONE
		if(debugPrints):
			print('Run LSR')
		data = mem.readAddress(offSet)
		data = ALU.lsrVal(data)
	def ror(self,offSet):           #DONE
		if(debugPrints):
			print('Run ROR')
		data = mem.readAddress(offSet)
		data = ALU.rorVal(data)
		mem.writeAddress(offSet,data)
	def stx(self,offSet):         #DONE
		if(debugPrints):
			print('Run STX')
		mem.writeAddress(offSet,r.regX)
	def ldx(self,offSet):       #DONE
		if(debugPrints):
			print('Run LDX')
		data = mem.readAddress(offSet)
		r.regX = data
	def dec(self,offSet):         #DONE
		if(debugPrints):
			print('Run DEC')
		data = mem.readAddress(offSet)
		data = ALU.decVal(data)
		mem.writeAddress(offSet,data)
	def inc(self,offSet):          #DONE
		if(debugPrints):
			print('Run INC')
		data = mem.readAddress(offSet)
		data = ALU.incVal(data)
		mem.writeAddress(offSet,data)
class _decode:
	global debugPrints
	global r
	def __init__(self):
		self.LUT=[( bitarray('0000 0000', endian='big'), False, e.brk ),
		( bitarray('0000 1000', endian='big'), False, e.php ),
		( bitarray('0001 0000', endian='big'), True, e.bpl ),
		( bitarray('0001 1000', endian='big'), False, e.clc ),
		( bitarray('0010 0000', endian='big'), False, e.jsrAbsolute ),
		( bitarray('0010 1000', endian='big'), False, e.plp ), 
		( bitarray('0011 0000', endian='big'), True, e.bmi ),
		( bitarray('0011 1000', endian='big'), False, e.sec ),
		( bitarray('0011 1100', endian='big'), True, e.bit ),

		( bitarray('0100 0000', endian='big'), False, e.rti ),
		( bitarray('0100 1000', endian='big'), False, e.pha ),
		( bitarray('0101 0000', endian='big'), True, e.bvc ),
		( bitarray('0101 1000', endian='big'), False, e.cli ),
		( bitarray('0101 1100', endian='big'), True, e.jmp ),
		( bitarray('0110 0000', endian='big'), False, e.rts ), 
		( bitarray('0110 1000', endian='big'), False, e.pla ),
		( bitarray('0111 0000', endian='big'), True, e.bvs ),
		( bitarray('0111 1000', endian='big'), False, e.sei ),
		( bitarray('0111 1100', endian='big'), False, e.jmpAbsolute ),

		( bitarray('1000 1000', endian='big'), False, e.dey ),
		( bitarray('1001 0000', endian='big'), True, e.bcc ),
		( bitarray('1001 1000', endian='big'), False, e.tya ),
		( bitarray('1001 1100', endian='big'), True, e.sty ),
		( bitarray('1010 1000', endian='big'), False, e.tay ),
		( bitarray('1011 0000', endian='big'), True, e.bcs ) ,
		( bitarray('1011 1000', endian='big'), False, e.clv ),
		( bitarray('1011 1100', endian='big'), True, e.ldy ) ,
		 
		( bitarray('1100 1000', endian='big'), False, e.iny ),
		( bitarray('1101 0000', endian='big'), True, e.bne ),
		( bitarray('1101 1100', endian='big'), True, e.cpy ),
		( bitarray('1110 1000', endian='big'), False, e.inx ) ,
		( bitarray('1111 0000', endian='big'), True, e.beq ),
		( bitarray('1111 1100', endian='big'), True, e.cpx ) ,

		( bitarray('0001 1101', endian='big'), True, e.ora ),
		( bitarray('0011 1101', endian='big'), True, e.andInstruct ),
		( bitarray('0101 1101', endian='big'), True, e.eor ),
		( bitarray('0111 1101', endian='big'), True, e.adc ),
		( bitarray('1001 1101', endian='big'), True, e.sta ),
		( bitarray('1011 1101', endian='big'), True, e.lda ),
		( bitarray('1101 1101', endian='big'), True, e.cmp ),
		( bitarray('1111 1101', endian='big'), True, e.sbc ),

		( bitarray('0001 1110', endian='big'), True, e.asl ),
		( bitarray('0011 1110', endian='big'), True, e.rol ) ,
		( bitarray('0101 1110', endian='big'), True, e.lsr ),
		( bitarray('0111 1110', endian='big'), True, e.ror ) ,
		( bitarray('1000 1010', endian='big'), False, e.txa ),
		( bitarray('1001 1010', endian='big'), True, e.txs ) ,
		( bitarray('1001 1110', endian='big'), True, e.stx ),
		( bitarray('1011 1010', endian='big'), False, e.tsx ) ,
		( bitarray('1011 1110', endian='big'), True, e.ldx ) ,
		( bitarray('1010 1010', endian='big'), False, e.tax ),
		( bitarray('1100 1010', endian='big'), True, e.dex ),
		( bitarray('1101 1110', endian='big'), True, e.dec ),
		( bitarray('1111 1110', endian='big'), True, e.inc ),

		( bitarray('1110 1010', endian='big'), False, e.nop )]
		self.addressModeLUT = [ 

	                   (bitarray('00 000', endian='big') , mem.immediate),
	                   (bitarray('00 001', endian='big') , mem.zeroPage),
	                   (bitarray('00 011', endian='big') , mem.absolute),
	                   (bitarray('00 100', endian='big') , mem.relative),
	                   (bitarray('00 101', endian='big') , mem.indirectX),
	                   (bitarray('00 111', endian='big') , mem.absoluteX),
	                   (bitarray('01 000', endian='big') , mem.zeroPageX), 
	                   (bitarray('01 001', endian='big') , mem.zeroPage),  
	                   (bitarray('01 010', endian='big') , mem.immediate), 
	                   (bitarray('01 011', endian='big') , mem.absolute),  
	                   (bitarray('01 100', endian='big') , mem.zeroPageY), 
	                   (bitarray('01 101', endian='big') , mem.indirectX), 
	                   (bitarray('01 110', endian='big') , mem.absoluteY), 
	                   (bitarray('01 111', endian='big') , mem.absoluteX), 
	                   (bitarray('10 000', endian='big') , mem.immediate),
	                   (bitarray('10 001', endian='big') , mem.zeroPage),
	                   (bitarray('10 010', endian='big') , mem.accumulator),
	                   (bitarray('10 011', endian='big') , mem.absolute),
	                   (bitarray('10 101', endian='big') , mem.indirectX),
	                   (bitarray('10 111', endian='big') , mem.absoluteX),]
		self.instruction = bitarray('0000 0000',endian='big')

	def setInstruction(self, instruction):
		self.instruction = instruction
	def parse(self):
		decodedInstruction = self.getInstruction()
		if(decodedInstruction[1]):
			decodedAddressMode = self.getAddressMode()
			if(decodedAddressMode == False):
				decodedAddressMode = mem.implied
		else:
			decodedAddressMode = mem.implied
		return decodedAddressMode, decodedInstruction[2]
	def parseInstruction(self, instruction):
		self.setInstruction(instruction)
		decodedAddressMode, decodedInstruction = self.parse()
		return decodedAddressMode, decodedInstruction
	def parseInstructionReg(self):
		self.setInstruction(r.instructReg)
		decodedAddressMode, decodedInstruction = self.parse()
		

		return decodedAddressMode, decodedInstruction
	def getAddressMode(self):
		aOPC = self.instruction[6:] + self.instruction[3:6]
		low = 0
		high = len(self.addressModeLUT)-1
		while(low<=high):
			mid = (low+high) // 2
			element = self.addressModeLUT[mid]
			if(aOPC == element[0]):
				return element[1]
			if(aOPC < element[0]):
				high = mid - 1
			if(aOPC > element[0]):
				low = mid + 1
		
		element = self.addressModeLUT[mid+1]
		return element[1]

	def getInstruction(self):
		OPC = self.instruction[6:] + self.instruction[:6]
		low = 0
		high = len(self.LUT)-1
		while(low<=high):
			mid = (low+high) // 2
			element = self.LUT[mid]
			key = element[0]
			tmp = key[6:]
			key = tmp + key[:6]
			if(OPC == key):
				return element
			if(OPC < key):
				high = mid - 1
			if(OPC > key):
				low = mid + 1
		element = self.LUT[mid]
		return element
	def getGroup(self):
		return self.instruction[6:]
	def getADMCode(self):
		return self.instruction[3:6]
class _cycle:
	global mem
	global r
	global decode
	global AM
	global e
	global l

	def __init__(self):
		self.ioPoint = 0
		self.charLen = 0
		self.charBuff = []
		self.pressBuff = []
		self.outLen = 0
		self.IOIndex = 0

	def output(self):
		if(self.outLen>0):
			self.outLen-=1
			i9 = 0
			while(i9<self.ioPoint):

				x = mem.readAddress(ba2int(r.IOStart)+i9)
				i9+=1
				#b = bitarray(x, endian='little')
				b = x.tobytes()
				self.IOIndex+=1
				#print('inouttput',b)
				SerialObj.write(b)
		
				#SerialObj.write(bytes(10))
			self.outLen = 0
		print('ACC:'+str(ba2int(r.acc))+' PC:'+str(ba2int(r.PC))+ ' Instruction: '+str(ba2int(r.instructReg)))
	def input(self):
		if(self.charLen > 0):
			self.charLen-=1
			out = self.charBuff[self.charLen]
			self.charBuff.remove(out)
			out = str(out)
			print('OOOOOOOOOOOOOOOOUUUUUUUUUUUUUUUUUT',out[0])
			if(out[0]=="K"):
				if(out[5]=="p"):
					out = 32
					out = int2ba(out)
				elif(out[5]=="h"):
					out = 15
					out = int2ba(out)
					return
				elif(out[5]=="n"):
					out = 10
					out = int2ba(out)
				elif(out[5]=="a"):
					out = 8
					out = int2ba(out)
			else:
				out = ord(out[1])
				out = int2ba(out)
			while(len(out)<8):
				out = bitarray('0',endian='big') + out
			mem.writeAddress(ba2int(r.IOStart)+self.ioPoint,out)
			print(out)
			self.outLen+=1
			self.ioPoint+=1		
	def cycle(self):
		self.input()
		r.setInstructionReg()
		decodedAddressMode, decodedInstruction = decode.parseInstructionReg()
		offset = decodedAddressMode()
		decodedInstruction(offset)
		self.output()
	def reset(self):
		print('RESETTING')
		r.PC = bitarray('1000 0000 0000 0000', endian='big')
		r.acc = r.zeros()
		r.regX = r.zeros()
		r.regY = r.zeros()
		r.flagReg = bitarray('0010 0000', endian='big')
		r.instructReg = r.zeros()
		r.stackPoint = r.zeros()
		

r = _registers()
mem = _memory()
ALU = _ALU()
e = _execute()
decode = _decode()
cpu = _cycle()


def on_press(key):
	global cpu
	if key in cpu.pressBuff:
		pass
	else:
		cpu.pressBuff.append(key)
def on_release(key):
	global cpu
	if key in cpu.pressBuff:
		cpu.charBuff.append(key)
		cpu.pressBuff.remove(key)
		cpu.charLen+=1
	else:
		pass

LDAzp = bitarray('1010 0101',endian='big')
ADCzp = bitarray('0110 0101',endian='big')
SBCzp = bitarray('1110 0101',endian='big')
JMPabs = bitarray('0111 1100',endian='big')
STAzp = bitarray('1000 0101',endian='big')
BRK = bitarray('0000 0000',endian='big')

LDAabsX= bitarray('1011 1101',endian='big')
STAabsX=bitarray('1001 1101',endian='big')
INX=bitarray('1110 1000',endian='big')
SBCimm=bitarray('1110 1001',endian='big')
BEQ=bitarray('1111 0000',endian='big')
STXabs=bitarray('1000 1110',endian='big')

JSR=bitarray('0010 0000', endian='big')
RTI=bitarray('0100 0000', endian='big')

IOIndexHigh=bitarray('0000 0010',endian='big')
inIndexLow=bitarray('0000 0000',endian='big')
outIndexLow=bitarray('1000 0000',endian='big')
jmpH=bitarray('1000 0000',endian='big')
jmpL=bitarray('0000 0000', endian='big')
sHigh = bitarray('1000 0000', endian='big')
sLow = bitarray('0000 0000', endian='big')
s=bitarray('0000 1010', endian='big')
xR=bitarray('0000 0000',endian='big')
offs=bitarray('0000 1000',endian='big')
rL=bitarray('0001 0100',endian='big')
rH=bitarray('1000 0000',endian='big')
prog3 = LDAabsX + IOIndexHigh + inIndexLow + STAabsX + IOIndexHigh + outIndexLow + INX + JMPabs + jmpH + jmpL

prog4 = LDAabsX + IOIndexHigh + inIndexLow +SBCimm + s + BEQ + offs + STAabsX + IOIndexHigh + outIndexLow + INX + JMPabs + jmpH + jmpL + STXabs + rH + rL + JMPabs + jmpH + jmpL + xR
cpu.reset()

mem.importPROG(prog3,32768)
SerialObj = serial.Serial(port='COM3') 
SerialObj.baudrate = 9600  # set Baud rate to 9600
SerialObj.bytesize = 8   # Number of data bits = 8
SerialObj.parity  ='N'   # No parity
SerialObj.stopbits = 1   # Number of Stop bits = 1
time.sleep(3)
print("RESET FINISHED...  RUNNING!")
print("RESET FINISHED...  RUNNING!")
print(r.PC)
while True:
	cpu.cycle()
	listener = keyboard.Listener(on_press=on_press,on_release=on_release)
	listener.start()
