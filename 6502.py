import os
from bitarray import bitarray
from bitarray.util import ba2int
from bitarray.util import int2ba
from bitarray.util import hex2ba
from pynput import keyboard
import time
import serial

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

	def importHex(self,prog,startIndex):
		i=0
		while(i<len(prog)):
			perogi = prog[i]
			perogi = hex2ba(perogi)
			while(len(perogi)<8):
				perogi = bitarray('0',endian='big') + perogi
			self.writeAddress(i+startIndex,perogi)
			i+=1
		for j in prog:
			print(j)
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

	def indirectY(self):
		pass
	def zeroPageX(self):
		self.accMode = False
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
		return bitarray('1111 0000 0000 0000',endian='big')
	def getIRQV(self):
		return bitarray('1000 1111 0000 0000',endian='big')
class _ALU:
	global r
	global debugPrints

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
		val = bitarray('0',endian='big') + data
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
			high, low = ALU.addOffset(r.getPCHigh(),r.getPCLow(),data)
			r.PC = high + low
	def bcc(self,offSet):        #DONE
		if(debugPrints):
			print('Run BCC')
		if(r.cFlag()==r.zeros()[1]):
			data = mem.readAddress(offSet)
			high, low = ALU.addOffset(r.getPCHigh(),r.getPCLow(),data)
			r.PC = high + low
	def bcs(self,offSet):        #DONE
		if(debugPrints):
			print('Run BCS')
		if(r.cFlag()==r.ones[1]):
			data = mem.readAddress(offSet)
			high, low = ALU.addOffset(r.getPCHigh(),r.getPCLow(),data)
			r.PC = high + low
	def bne(self,offSet):         #DONE
		if(debugPrints):
			print('Run BNE')
		if(r.zFlag()==r.zeros()[1]):
			data = mem.readAddress(offSet)
			high, low = ALU.addOffset(r.getPCHigh(),r.getPCLow(),data)
			r.PC = high + low
	def beq(self,offSet):          #DONE
		if(debugPrints):
			print('Run BEQ')
		if(r.zFlag()==r.ones[1]):
			data = mem.readAddress(offSet)
			high, low = ALU.addOffset(r.getPCHigh(),r.getPCLow(),data)
			r.PC = high + low
	def brk(self,offSet):
		if(debugPrints):
			print('Run BRK')
		if(debugPrints):
			print('RUNNING OS._EXIT')
		os._exit(1)
	def jsrAbsolute(self,offSet):   
		print('RUN JSR')        
		#r.incPC()
		hD = mem.readAddress(r.PC)
		r.incPC()
		lD = mem.readAddress(r.PC)
		r.incPC()
		print("JSR PC",r.PC)
		h = r.PC[:8]
		l = r.PC[8:]
		mem.writeAddress(ba2int(r.stackPoint) + ba2int(r.stackStart), l)
		r.stackPoint = ALU.incVal(r.stackPoint) 
		mem.writeAddress(ba2int(r.stackPoint) + ba2int(r.stackStart), h)
		r.stackPoint = ALU.incVal(r.stackPoint)
		r.PC = hD + lD
	def rts(self,offSet):
		print('RUN RTS')
		r.stackPoint = ALU.decVal(r.stackPoint)
		h = mem.readAddress(ba2int(r.stackPoint) + ba2int(r.stackStart))
		r.stackPoint = ALU.decVal(r.stackPoint)   
		l = mem.readAddress(ba2int(r.stackPoint) + ba2int(r.stackStart))
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
		r.regY = ALU.decVal(r.regY)
	def tay(self,offSet):                #DONE
		if(debugPrints):
			print('Run TAY')
		r.regY = r.acc
	def iny(self,offSet):     #DONE
		if(debugPrints):
			print('Run INY')
		r.regY = ALU.incVal(r.regY)
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
		self.LUT=[( bitarray('0000 0000', endian='big'), mem.implied, e.brk ),
		( bitarray('0000 0001', endian='big'), mem.indirectX, e.ora ),
		( bitarray('0000 0101', endian='big'), mem.zeroPage, e.ora ),
		( bitarray('0000 0110', endian='big'), mem.zeroPage, e.asl ),
		( bitarray('0000 1000', endian='big'), mem.implied, e.php ),
		( bitarray('0000 1001', endian='big'), mem.immediate, e.ora ), 
		( bitarray('0000 1010', endian='big'), mem.accumulator, e.asl ),
		( bitarray('0000 1101', endian='big'), mem.absolute, e.ora ),
		( bitarray('0000 1110', endian='big'), mem.absolute, e.asl ),
		( bitarray('0001 0000', endian='big'), mem.relative, e.bpl ),
		( bitarray('0001 0001', endian='big'), mem.indirectY, e.ora ),
		( bitarray('0001 0101', endian='big'), mem.zeroPageX, e.ora ),
		( bitarray('0001 0110', endian='big'), mem.zeroPageX, e.asl ),
		( bitarray('0001 1000', endian='big'), mem.implied, e.clc ),
		( bitarray('0001 1001', endian='big'), mem.absoluteY, e.ora ), 
		( bitarray('0001 1101', endian='big'), mem.absoluteX, e.ora ),
		( bitarray('0001 1110', endian='big'), mem.absoluteX, e.asl ),
		( bitarray('0010 0000', endian='big'), mem.implied, e.jsrAbsolute ),
		( bitarray('0010 0001', endian='big'), mem.indirectX, e.andInstruct ),
		( bitarray('0010 0100', endian='big'), mem.zeroPage, e.bit ),
		( bitarray('0010 0101', endian='big'), mem.zeroPage, e.andInstruct ),
		( bitarray('0010 0110', endian='big'), mem.zeroPage, e.rol ),
		( bitarray('0010 1000', endian='big'), mem.implied, e.plp ),
		( bitarray('0010 1001', endian='big'), mem.immediate, e.andInstruct ), 
		( bitarray('0010 1010', endian='big'), mem.accumulator, e.rol ),
		( bitarray('0010 1100', endian='big'), mem.zeroPage, e.bit ),
		( bitarray('0010 1101', endian='big'), mem.absolute, e.andInstruct ),
		( bitarray('0010 1110', endian='big'), mem.absolute, e.rol ),
		( bitarray('0011 0000', endian='big'), mem.relative, e.bmi ),
		( bitarray('0011 0001', endian='big'), mem.indirectY, e.andInstruct),
		( bitarray('0011 0101', endian='big'), mem.zeroPageX, e.andInstruct ),
		( bitarray('0011 0110', endian='big'), mem.zeroPageX, e.rol ),
		( bitarray('0011 1000', endian='big'), mem.implied, e.sec ),
		( bitarray('0011 1001', endian='big'), mem.absoluteY, e.andInstruct ), 
		( bitarray('0011 1101', endian='big'), mem.absoluteX, e.andInstruct ),
		( bitarray('0011 1110', endian='big'), mem.absolute, e.asl ),
		( bitarray('0100 0000', endian='big'), mem.implied, e.rti ),
		( bitarray('0100 0001', endian='big'), mem.indirectX, e.eor),
		( bitarray('0100 0101', endian='big'), mem.zeroPage, e.eor ),
		( bitarray('0100 0110', endian='big'), mem.zeroPage, e.lsr ),
		( bitarray('0100 1000', endian='big'), mem.implied, e.pha ),
		( bitarray('0100 1001', endian='big'), mem.immediate, e.eor ), 
		( bitarray('0100 1010', endian='big'), mem.accumulator, e.lsr ),
		( bitarray('0100 1100', endian='big'), mem.implied, e.jmpAbsolute ),
		( bitarray('0100 1101', endian='big'), mem.absolute, e.eor ),
		( bitarray('0100 1110', endian='big'), mem.absolute, e.lsr ),
		( bitarray('0101 0000', endian='big'), mem.relative, e.bvc ),
		( bitarray('0101 0001', endian='big'), mem.indirectY, e.eor),
		( bitarray('0101 0101', endian='big'), mem.zeroPageX, e.eor ),
		( bitarray('0101 0110', endian='big'), mem.zeroPageX, e.lsr ),
		( bitarray('0101 1000', endian='big'), mem.implied, e.cli ),
		( bitarray('0101 1001', endian='big'), mem.absoluteY, e.eor ), 
		( bitarray('0101 1101', endian='big'), mem.absoluteX, e.eor ),
		( bitarray('0101 1110', endian='big'), mem.absoluteX, e.lsr ),
		( bitarray('0110 0000', endian='big'), mem.implied, e.rts ),
		( bitarray('0110 0001', endian='big'), mem.indirectX, e.adc),
		( bitarray('0110 0101', endian='big'), mem.zeroPage, e.adc ),
		( bitarray('0110 0110', endian='big'), mem.zeroPage, e.ror ),
		( bitarray('0110 1000', endian='big'), mem.implied, e.pla ),
		( bitarray('0110 1001', endian='big'), mem.immediate, e.adc ), 
		( bitarray('0110 1010', endian='big'), mem.accumulator, e.ror ),
		( bitarray('0110 1100', endian='big'), mem.implied, e.jmp),
		( bitarray('0110 1101', endian='big'), mem.absolute, e.adc ),
		( bitarray('0110 1110', endian='big'), mem.absolute, e.ror ),
		( bitarray('0111 0000', endian='big'), mem.relative, e.bvs ),
		( bitarray('0111 0001', endian='big'), mem.indirectY, e.adc),
		( bitarray('0111 0101', endian='big'), mem.zeroPageX, e.adc ),
		( bitarray('0111 0110', endian='big'), mem.zeroPageX, e.ror ),
		( bitarray('0111 1000', endian='big'), mem.implied, e.sei ),
		( bitarray('0111 1001', endian='big'), mem.absoluteY, e.adc ), 
		( bitarray('0111 1101', endian='big'), mem.absoluteX, e.adc ),
		( bitarray('0111 1110', endian='big'), mem.absoluteX, e.ror ),
		( bitarray('1000 0001', endian='big'), mem.indirectX, e.sta),
		( bitarray('1000 0100', endian='big'), mem.zeroPage, e.sty),
		( bitarray('1000 0101', endian='big'), mem.zeroPage, e.sta ),
		( bitarray('1000 0110', endian='big'), mem.zeroPage, e.stx ),
		( bitarray('1000 1000', endian='big'), mem.implied, e.dey ),
		( bitarray('1000 1010', endian='big'), mem.implied, e.txa ), 
		( bitarray('1000 1100', endian='big'), mem.absolute, e.sty ),
		( bitarray('1000 1101', endian='big'), mem.absolute, e.sta ),
		( bitarray('1000 1110', endian='big'), mem.absolute, e.stx ),
		( bitarray('1001 0000', endian='big'), mem.relative, e.bcc ),
		( bitarray('1001 0001', endian='big'), mem.indirectY, e.sta),
		( bitarray('1001 0100', endian='big'), mem.zeroPageX, e.sty),
		( bitarray('1001 0101', endian='big'), mem.zeroPageX, e.sta ),
		( bitarray('1001 0110', endian='big'), mem.zeroPageY, e.stx ),
		( bitarray('1001 1000', endian='big'), mem.implied, e.tya ),
		( bitarray('1001 1001', endian='big'), mem.absoluteY, e.sta ), 
		( bitarray('1001 1010', endian='big'), mem.implied, e.txs ),
		( bitarray('1001 1101', endian='big'), mem.absoluteX, e.sta),
		( bitarray('1010 0000', endian='big'), mem.immediate, e.ldy ),
		( bitarray('1010 0001', endian='big'), mem.indirectX, e.lda),
		( bitarray('1010 0010', endian='big'), mem.immediate, e.ldx),
		( bitarray('1010 0100', endian='big'), mem.zeroPage, e.ldy),
		( bitarray('1010 0101', endian='big'), mem.zeroPage, e.lda ),
		( bitarray('1010 0110', endian='big'), mem.zeroPage, e.ldx ),
		( bitarray('1010 1000', endian='big'), mem.implied, e.tay ),
		( bitarray('1010 1001', endian='big'), mem.immediate, e.lda ), 
		( bitarray('1010 1010', endian='big'), mem.implied, e.tax ),
		( bitarray('1010 1100', endian='big'), mem.absolute, e.ldy),
		( bitarray('1010 1101', endian='big'), mem.absolute, e.lda),
		( bitarray('1010 1110', endian='big'), mem.absolute, e.ldx),
		( bitarray('1011 0000', endian='big'), mem.relative, e.bcs ),
		( bitarray('1011 0001', endian='big'), mem.indirectY, e.lda),
		( bitarray('1011 0100', endian='big'), mem.zeroPageX, e.ldy),
		( bitarray('1011 0101', endian='big'), mem.zeroPageX, e.lda ),
		( bitarray('1011 0110', endian='big'), mem.zeroPageY, e.ldx ),
		( bitarray('1011 1000', endian='big'), mem.implied, e.clv ),
		( bitarray('1011 1001', endian='big'), mem.absoluteY, e.lda ), 
		( bitarray('1011 1010', endian='big'), mem.implied, e.tsx ),
		( bitarray('1011 1100', endian='big'), mem.absoluteX, e.ldy),
		( bitarray('1011 1101', endian='big'), mem.absoluteX, e.lda),
		( bitarray('1011 1110', endian='big'), mem.absoluteY, e.ldx),
		( bitarray('1100 0000', endian='big'), mem.immediate, e.cpy ),
		( bitarray('1100 0001', endian='big'), mem.indirectX, e.cmp),
		( bitarray('1100 0100', endian='big'), mem.zeroPage, e.cpy),
		( bitarray('1100 0101', endian='big'), mem.zeroPage, e.cmp ),
		( bitarray('1100 0110', endian='big'), mem.zeroPage, e.dec ),
		( bitarray('1100 1000', endian='big'), mem.implied, e.iny ),
		( bitarray('1100 1001', endian='big'), mem.immediate, e.cmp ), 
		( bitarray('1100 1010', endian='big'), mem.implied, e.dex ),
		( bitarray('1100 1100', endian='big'), mem.absolute, e.cpy),
		( bitarray('1100 1101', endian='big'), mem.absolute, e.cmp),
		( bitarray('1100 1110', endian='big'), mem.absolute, e.dec),
		( bitarray('1101 0000', endian='big'), mem.relative, e.bne ),
		( bitarray('1101 0001', endian='big'), mem.indirectY, e.cmp),
		( bitarray('1101 0101', endian='big'), mem.zeroPageX, e.cmp ),
		( bitarray('1101 0110', endian='big'), mem.zeroPageX, e.dec ),
		( bitarray('1101 1001', endian='big'), mem.absoluteY, e.cmp ), 
		( bitarray('1101 1101', endian='big'), mem.absoluteX, e.cmp),
		( bitarray('1101 1110', endian='big'), mem.absoluteX, e.dec),
		( bitarray('1110 0000', endian='big'), mem.immediate, e.cpx ),
		( bitarray('1110 0001', endian='big'), mem.indirectX, e.sbc),
		( bitarray('1110 0100', endian='big'), mem.zeroPage, e.cpx),
		( bitarray('1110 0101', endian='big'), mem.zeroPage, e.sbc ),
		( bitarray('1110 0110', endian='big'), mem.zeroPage, e.inc ),
		( bitarray('1110 1000', endian='big'), mem.implied, e.inx ),
		( bitarray('1110 1001', endian='big'), mem.immediate, e.sbc ), 
		( bitarray('1110 1010', endian='big'), mem.implied, e.nop ),
		( bitarray('1110 1100', endian='big'), mem.absolute, e.cpx),
		( bitarray('1110 1101', endian='big'), mem.absolute, e.sbc),
		( bitarray('1110 1110', endian='big'), mem.absolute, e.inc),
		( bitarray('1111 0000', endian='big'), mem.relative, e.beq ),
		( bitarray('1111 0001', endian='big'), mem.indirectY, e.sbc),
		( bitarray('1111 0101', endian='big'), mem.zeroPageX, e.sbc ),
		( bitarray('1111 0110', endian='big'), mem.zeroPageX, e.inc ),
		( bitarray('1111 1001', endian='big'), mem.absoluteY, e.sbc ), 
		( bitarray('1111 1101', endian='big'), mem.absoluteX, e.sbc),
		( bitarray('1111 1110', endian='big'), mem.absoluteX, e.inc),
		]
		self.instruction = bitarray('0000 0000',endian='big')
	def parseInstructionReg(self):
		a = r.instructReg
		high = len(self.LUT)-1
		low=0
		while(low<=high):
			mid = (high+low)//2
			element = self.LUT[mid]
			mE = element[0]
			if(a==mE):
				return element[1], element[2]
			if(a<mE):
				high = mid - 1
			if(a>mE):
				low = mid + 1
		print('EPIC FUCKIN FAIL',r.instructReg,element[0])
		return element[1], element[2]
class _cycle:
	global mem
	global r
	global decode
	global e
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
		print('ACC:'+str(ba2int(r.acc))+' PC:'+str(ba2int(r.PC))+ ' Instruction: '+str(hex(ba2int(r.instructReg))))
	def input(self):
		if(self.charLen > 0):
			self.charLen-=1
			out = self.charBuff[self.charLen]
			self.charBuff.remove(out)
			out = str(out)
			print('OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOUUUUUUUUUUUUUUUUUT',out[0])
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

#LDAabsX IOIndexHigh inIndexLow SBCimm s BEQ offs STAabsX  
#IOIndexHigh outIndexLow INX JSR subHigh subLow  
# STXabs rH rL JMPabs jmpH jmpL xR
#RTS)
progHEX1 = ["AD","02","00","E9","0A","F0","08","9D",
            "02","80","E8","20","80","15","8E","80",
            "17","4C","80","00","00","EA","EA","EA",
            "EA","EA","EA","EA","EA","EA","EA","60"]
cpu.reset()
#mem.importPROG(prog4,32768)
mem.importHex(progHEX1,32768)

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
