import keyboard
import os
from bitarray import bitarray
from bitarray.util import ba2int
from bitarray.util import int2ba

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
def baFromInt(integer):
	ba = int2ba(integer,endian='big')
	buffer = bitarray('0000 0000', endian='big')
	index = len(ba)
	bi=8
	while index > 0:
		index-=1
		bi-=1
		buffer[bi]=ba[index]
	return buffer


class logger:
	def __init__(self):
		pass
class _registers:
	global mem
	def __init__(self):
		self.PC = bitarray('0000 0000 0000 0000', endian='big')
		self.stackPoint = bitarray('0000 0000', endian='big')
		self.acc = bitarray('0000 0000', endian='big')
		self.regX = bitarray('0000 0000', endian='big')
		self.regY = bitarray('0000 0000', endian='big')
		self.flagReg = bitarray('0010 0000', endian='big')
		self.ones = bitarray('1111 1111', endian='big')
		self.zeros = bitarray('0000 0000', endian='big')
		self.instructReg = bitarray('0000 0000', endian='big')
	def setPCLow(self,inp):
		self.PC[8:] = inp
	def setPCHigh(self,inp):
		self.PC[:8] = inp
	def getPCLow(self):
		return self.PC[8:]
	def getPCHigh(self):
		return self.PC[:8]
	def incPC(self):
		num = ba2int(self.PC)
		num += 1
		num = baFromInt(num)
		self.PC = num
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
		mem.setAddressFromPC()
		self.instructReg = mem.read()
class _memory:
	global r
	global ALU
	def __init__(self):
		self.memoryBlock = bitarray(524288,endian='big')
		self.addressLow = bitarray(8,endian='big')
		self.addressHigh = bitarray(8,endian='big')
		self.address = self.addressHigh + self.addressLow
		self.resetVector = bitarray('0000 0000 0000 0000',endian='big')
		self.nmiVector = bitarray('0000 1111 0000 0000',endian='big')
		self.irqVector = bitarray('0000 1100 0000 0000',endian='big')
		self.accMode = False
		self.setVectors()
		self.addIndex = 0

	def setVectors(self):
		self.setAddressHigh(bitarray('1111 1111',endian='big'))
		self.setAddressLow(bitarray('1111 1010',endian='big'))
		self.write(self.nmiVector[:8])
		self.setAddressLow(bitarray('1111 1011',endian='big'))
		self.write(self.nmiVector[8:])
		self.setAddressLow(bitarray('1111 1100',endian='big'))
		self.write(self.resetVector[:8])
		self.setAddressLow(bitarray('1111 1101',endian='big'))
		self.write(self.resetVector[8:])
		self.setAddressLow(bitarray('1111 1110',endian='big'))
		self.write(self.irqVector[:8])
		self.setAddressLow(bitarray('1111 1111',endian='big'))
		self.write(self.irqVector[8:])
	
	def getResetV(self):
		self.setAddressHigh(bitarray('1111 1111',endian='big'))
		self.setAddressLow(bitarray('1111 1100',endian='big'))
		a = self.read()
		self.setAddressLow(bitarray('1111 1101',endian='big'))
		b = self.read()
		return a, b
	def getNMIV(self):
		self.setAddressHigh(bitarray('1111 1111',endian='big'))
		self.setAddressLow(bitarray('1111 1010',endian='big'))
		a = self.read()
		self.setAddressLow(bitarray('1111 1011',endian='big'))
		b = self.read()
		return a, b
	def getIRQV(self):
		self.setAddressHigh(bitarray('1111 1111',endian='big'))
		self.setAddressLow(bitarray('1111 1110',endian='big'))
		a = self.read()
		self.setAddressLow(bitarray('1111 1111',endian='big'))
		b = self.read()
		return a, b
	def setAddressHigh(self, address):
		self.addressHigh=address
	def setAddressLow(self, address):
		self.addressHigh=address
	def getAddressHigh(self):
		return self.addressHigh
	def getAddressLow(self):
		return self.addressLow
	def getAddress(self):
		self.address = self.addressHigh + self.addressLow
		return self.address
	def getEffectiveAddress(self):
		self.address = self.addressHigh + self.addressLow
		addy = ba2int(self.address)
		self.addIndex = addy*8
		return self.addIndex
	def read(self):
		if(self.accMode):
			return r.acc
		else:
			self.getEffectiveAddress()
			return(self.memoryBlock[self.addIndex:self.addIndex+8])
	def write(self, data):
		if(self.accMode):
			r.acc = data
		else:
			self.getEffectiveAddress()
			self.memoryBlock[self.addIndex:self.addIndex+8] = data
			return True
	def setAddressFromPC(self):
		self.setAddressHigh(r.PC[:8])
		self.setAddressLow(r.PC[8:])
class _runAddressModes:
	def __init__(self,memory):
		self.m = memory
	def zeroPageX(self):
		self.m.accMode = False
		print('zeroPageX')
		self.m.setAddressHigh(r.zeros)
		self.m.setAddressLow(r.regX)
	def zeroPage(self):	
		self.m.accMode = False
		print('zeroPage')
		r.incPC()
		self.m.setAddressFromPC()
		lowBit = self.m.read()
		self.m.setAddressLow(lowBit)
		self.m.setAddressHigh(r.zeros)
	def absoluteX(self):
		self.m.accMode = False
		print('absoluteX')
		r.incPC()
		self.m.setAddressFromPC()
		highPart = self.m.read()
		r.incPC()
		self.m.setAddressFromPC()
		lowPart = self.m.read()
		highPart, lowPart = ALU.addOffset(highPart,lowPart,r.regX)
		self.m.setAddressHigh(highPart)
		self.m.setAddressLow(lowPart)
	def immediate(self):
		self.m.accMode = False
		print('immediate')
		r.incPC()
		self.m.setAddressFromPC()
	def absolute(self):
		self.m.accMode = False
		print('absolute')
		r.incPC()
		self.m.setAddressFromPC()
		highPart = self.m.read()
		r.incPC()
		self.m.setAddressFromPC()
		lowPart = self.m.read()
		self.m.setAddressHigh(highPart)
		self.m.setAddressLow(lowPart)
	def zeroPageY(self):
		self.m.accMode = False
		print('zeroPageY')
		self.m.setAddressHigh(r.zeros)
		self.m.setAddressLow(r.regY)
	def indirectX(self):
		self.m.accMode = False
		print('weirdmode')
		r.eA[0] = r.zeros[0]
		#literally fuck this shit lmao
		incPC()
	def absoluteY(self):
		self.m.accMode = False
		print('absoluteY')
		r.incPC()
		self.m.setAddressFromPC()
		highPart = self.m.read()
		r.incPC()
		self.m.setAddressFromPC()
		lowPart = self.m.read()
		highPart, lowPart = ALU.addOffset(highPart,lowPart,r.regY)
		self.m.setAddressHigh(highPart)
		self.m.setAddressLow(lowPart)
	def accumulator(self):
		print('accumulator mode')
		self.m.accMode = True
	def relative(self):
		pass
	def implied(self):
		pass
class _ALU:
	global r
	def __init__(self):
		print('hewwo im ALU')
	def fullAdder(self,a,b,cIn):
			hXor = a^b
			hOut = a&b
			s = hXor^cIn
			fOut = hXor&cIn
			cOut = fOut | hOut
			return s,cOut
	def addOffset(self,high,low,offset):
		sL, c = addVal(low,offset,carry=0,flags=False)
		sH, c = addVal(high,r.zeros,carry=c,flags=False)
		return sH, sL
	def addVal(self, data1, data2, carry = None, flags = True, cFlag=True, zFlag=True, nFlag=True, vFlag=True):
		if carry is None:
			cIn = r.flagReg[7]
		else:
			cIn = carry
		out = r.zeros
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
		out = r.zeros
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
		r.acc = subVal(r.acc, data)
	def incVal(self, data, retCarry = False, flags = False, cFlag=False, zFlag=False, nFlag=False, vFlag=False):
		s, c = addVal(data, r.zeros, carry = r.ones[0], flags=flags, cFlag=cFlag, zFlag=zFlag, nFlag=nFlag, vFlag=vFlag)
		if(retCarry):
			return s,c
		return s
	def decVal(self, data, retCarry = False, flags = False, cFlag=False, zFlag=False, nFlag=False, vFlag=False):
		s, c = addVal(data, r.ones, carry = r.zeros[0], flags=flags, cFlag=cFlag, zFlag=zFlag, nFlag=nFlag, vFlag=vFlag)
		if(retCarry):
			return s,c
		return s
	def lsrVal(self, data):
		val = data + zeros[0]
		val >>= 1
		r.cFlag(setVal = val[8])
		return(val[:8])
	def aslVal(self, data):
		val = zeros[0] + data
		val <<= 1
		r.cFlag(setVal = val[0])
		return(val[1:])
	def rorVal(self,data):
		val = r.flagReg[7] + data + zeros[0]
		val >>= 1
		r.cFlag(setVal = val[9])
		return val[1:9]
	def rolVal(self,data):
		val = zeros[0] + data + r.flagReg[7]
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
	def __init__(self):
		global r
		global ALU
	def bpl(self):          #DONE
		if(r.nFlag()==r.zeros[1]):
			data = mem.read()
			high, low = ALU.addOffset(r.getPCHigh,r.getPCLow,data)
			r.setPCHigh(high)
			r.setPCLow(low)
	def bmi(self):        #DONE
		if(r.nFlag()==r.ones[1]):
			data = mem.read()
			high, low = ALU.addOffset(r.getPCHigh,r.getPCLow,data)
			r.setPCHigh(high)
			r.setPCLow(low)
	def bvc(self):          #DONE
		if(r.vFlag()==r.zeros[1]):
			data = mem.read()
			high, low = ALU.addOffset(r.getPCHigh,r.getPCLow,data)
			r.setPCHigh(high)
			r.setPCLow(low)
	def bvs(self):        #DONE
		if(r.vFlag()==r.ones[1]):
			data = mem.read()
			high, low = ALU.addOffset(r.getPCHigh,r.getPCLow,data)
			r.setPCHigh(high)
			r.setPCLow(low)
	def bcc(self):        #DONE
		if(r.cFlag()==r.zeros[1]):
			data = mem.read()
			high, low = ALU.addOffset(r.getPCHigh,r.getPCLow,data)
			r.setPCHigh(high)
			r.setPCLow(low)
	def bcs(self):        #DONE
		if(r.cFlag()==r.ones[1]):
			data = mem.read()
			high, low = ALU.addOffset(r.getPCHigh,r.getPCLow,data)
			r.setPCHigh(high)
			r.setPCLow(low)
	def bne(self):         #DONE
		if(r.zFlag()==r.zeros[1]):
			data = mem.read()
			high, low = ALU.addOffset(r.getPCHigh,r.getPCLow,data)
			r.setPCHigh(high)
			r.setPCLow(low)
	def beq(self):          #DONE
		if(r.zFlag()==r.ones[1]):
			data = mem.read()
			high, low = ALU.addOffset(r.getPCHigh,r.getPCLow,data)
			r.setPCHigh(high)
			r.setPCLow(low)
	def brk(self):
		pass
	def jsrAbsolute(self):           #DONE
		r.incPC()
		lowBit = mem.read()
		r.incPC()
		highBit = mem.read()
		r.incPC()
		mem.setAddressHigh(bitarray('0000 0001',endian='big'))
		mem.setAddressLow(r.stackPoint)
		mem.write(r.getPCHigh)
		r.stackPoint = ALU.incVal(r.stackPoint)
		mem.setAddressLow(r.stackPoint)
		mem.write(r.getPCLow)
		r.stackPoint = ALU.incVal(r.stackPoint)
		r.setPCLow(lowBit)
		r.setPCHigh(highBit)

	def rts(self):                #DONE
		mem.setAddressHigh(bitarray('0000 0001',endian='big'))
		r.stackPoint = ALU.decVal(r.stackPoint)
		mem.setAddressLow(r.stackPoint)
		lowPart = mem.read()
		r.stackPoint = ALU.decVal(r.stackPoint)
		highPart = mem.read()
		mem.setAddressLow(r.stackPoint)
		r.setPCHigh(highPart)
		r.setPCLow(lowPart)

	def php(self):         #DONE
		mem.setAddressLow(r.stackPoint)
		mem.setAddressHigh(bitarray('0000 0001',endian='big'))
		mem.write(r.flagReg)
		r.stackPoint = ALU.incVal(r.stackPoint)
		r.incPC()
	def plp(self):          #DONE
		mem.setAddressLow(r.stackPoint)
		mem.setAddressHigh(bitarray('0000 0001',endian='big'))
		r.flagReg = mem.read()
		r.stackPoint = ALU.decVal(r.stackPoint)
		r.incPC()
	def pha(self):              #DONE
		mem.setAddressLow(r.stackPoint)
		mem.setAddressHigh(bitarray('0000 0001',endian='big'))
		mem.write(r.acc)
		r.stackPoint = ALU.incVal(r.stackPoint)
		r.incPC()
	def pla(self):              #DONE
		mem.setAddressLow(r.stackPoint)
		mem.setAddressHigh(bitarray('0000 0001',endian='big'))
		r.acc = mem.read()
		r.stackPoint = ALU.decVal(r.stackPoint)
		r.incPC()
	def dey(self):         #DONE
		r.regY = ALU.decVal(regY)
		r.incPC()
	def tay(self):                #DONE
		r.regY = r.acc
		r.incPC()
	def iny(self):     #DONE
		r.regY = ALU.incVal(regY)
		r.incPC()
	def inx(self):      #DONE
		r.regX = ALU.incVal(r.regX)
		r.incPC()
	def clc(self):          #DONE
		r.cFlag(setVal=r.zeros[0])
		r.incPC()
	def sec(self):         #DONE
		r.cFlag(setVal=r.ones[0])
		r.incPC()
	def cli(self):        	#DONE
		r.iFlag(setVal=r.zeros[0])
		r.incPC()
	def sei(self):          #DONE
		r.iFlag(setVal=r.ones[0])
		r.incPC()
	def tya(self):              #DONE
		r.acc = r.regY
		r.incPC()
	def clv(self):          #DONE
		r.vFlag(setVal=r.zeros[0])
		r.incPC()
	def txa(self):          #DONE
		r.acc = r.regX
		r.incPC()
	def txs(self):               #DONE
		r.stackPoint = r.regX
		r.incPC()
	def tax(self):               #DONE
		r.regX = r.acc
		r.incPC()
	def tsx(self):      #DONE
		r.regX = r.stackPoint
		r.incPC()
	def dex(self):          #DONE
		r.regX = ALU.decVal(r.regX)
		r.incPC()
	def nop(self):
		r.incPC()
	def bit(self):       #DONE
		data = mem.read()
		r.nFlag(setVal=data[0])
		r.vFlag(setVal=data[1])
		data &= r.acc
		ALU.addVal(self, data, r.zeros, carry = r.zeros[0], flags = True, cFlag=False, zFlag=True, nFlag=False, vFlag=False)
		r.incPC()
	def jmp(self):                  #DONE
		r.incPC()
		highPart = mem.read()
		r.incPC()
		lowPart = mem.read()
		r.setPCHigh(highPart)
		r.setPCLow(lowPart)
		mem.setAddressFromPC()
		highPart = mem.read()
		r.incPC()
		lowPart = mem.read()
		r.setPCHigh(highPart)
		r.setPCLow(lowPart)
	def jmpAbsolute(self):                    #DONE
		r.incPC()
		highPart = mem.read()
		r.incPC()
		lowPart = mem.read()
		r.setPCHigh(highPart)
		r.setPCLow(lowPart)
	def sty(self):              #DONE
		mem.write(r.regY)
		r.incPC()
	def ldy(self):              #DONE
		data = mem.read()
		r.regY = data
		r.incPC()
	def cpy(self):            #DONE
		data = mem.read()
		ALU.cmpVal(data,regY)
	def cpx(self):            #DONE
		data = mem.read()
		ALU.cmpVal(data,regX)
	def ora(self):            #DONE
		data = mem.read()
		r.acc |= data
		ALU.add(r.zeros,cFlag=False,vFlag=False)
		r.incPC()
	def eor(self):        #DONE
		data = mem.read()
		r.acc ^= data
		ALU.add(r.zeros,cFlag=False,vFlag=False)
	def sta(self):        #DONE
		mem.write(r.acc)
		r.incPC()
	def cmp(self):       #DONE
		data = mem.read()
		ALU.cmpVal(data,r.acc)
	def andInstruct(self):    #DONE
		data = mem.read()
		ALU.andAcc(data)
	def adc(self):   #DONE
		data = mem.read()
		r.acc, carryOut = ALU.add(data)
	def lda(self):          #DONE
		data = mem.read()
		r.acc = data
		r.incPC()
	def sbc(self):              #DONE
		data = mem.read()
		ALU.sub(data)
		r.incPC()
	def asl(self):     #DONE
		data = mem.read()
		data = ALU.aslVal(data)
		mem.write(data)
		r.incPC()
	def rol(self):                #DONE
		data = mem.read()
		data = ALU.rolVal(data)
		mem.write(data)
		r.incPC()
	def lsr(self):                    #DONE
		data = mem.read()
		data = ALU.lsrVal(data)
		r.incPC()
	def ror(self):
		data = mem.read()
		data = ALU.rorVal(data)
		mem.write(data)
		r.incPC()
	def stx(self):
		mem.write(r.regX)
		r.incPC()
	def ldx(self):       #DONE
		data = mem.read()
		r.regX = data
		r.incPC()
	def dec(self):         #DONE
		data = mem.read()
		data = ALU.decVal(data)
		mem.write(data)
	def inc(self):          #DONE
		data = mem.read()
		data = ALU.incVal(data)
		mem.write(data)
class _decode:
	global r
	def __init__(self):
		self.LUT=[( bitarray('0000 0000', endian='big'), False, e.brk ),( bitarray('0000 1000', endian='big'), False, e.php ),
		( bitarray('0001 0000', endian='big'), True, e.bpl ),( bitarray('0001 1000', endian='big'), False, e.clc ),
		( bitarray('0010 0000', endian='big'), False, e.jsrAbsolute ),( bitarray('0010 1000', endian='big'), False, e.plp ), 
		( bitarray('0011 0000', endian='big'), True, e.bmi ),( bitarray('0011 1000', endian='big'), False, e.sec ),
		( bitarray('0011 1100', endian='big'), True, e.bit ),

		( bitarray('0100 0000', endian='big'), False, e.rti ),( bitarray('0100 1000', endian='big'), False, e.pha ),
		( bitarray('0101 0000', endian='big'), True, e.bvc ),( bitarray('0101 1000', endian='big'), False, e.cli ),
		( bitarray('0101 1100', endian='big'), True, e.jmp ),( bitarray('0110 0000', endian='big'), False, e.rts ), 
		( bitarray('0110 1000', endian='big'), False, e.pla ),( bitarray('0111 0000', endian='big'), True, e.bvs ),
		( bitarray('0111 1000', endian='big'), False, e.sei ),( bitarray('0111 1100', endian='big'), True, e.jmpAbsolute ),

		( bitarray('1000 1000', endian='big'), False, e.dey ),( bitarray('1001 0000', endian='big'), True, e.bcc ),
		( bitarray('1001 1000', endian='big'), False, e.tya ),( bitarray('1001 1100', endian='big'), True, e.sty ),
		( bitarray('1010 1000', endian='big'), False, e.tay ),( bitarray('1011 0000', endian='big'), True, e.bcs ) ,
		( bitarray('1011 1000', endian='big'), False, e.clv ),( bitarray('1011 1100', endian='big'), True, e.ldy ) ,
		 
		( bitarray('1100 1000', endian='big'), False, e.iny ),( bitarray('1101 0000', endian='big'), True, e.bne ),
		( bitarray('1101 1100', endian='big'), True, e.cpy ),( bitarray('1110 1000', endian='big'), False, e.inx ) ,
		( bitarray('1111 0000', endian='big'), True, e.beq ),( bitarray('1111 1100', endian='big'), True, e.cpx ) ,

		( bitarray('0001 1101', endian='big'), True, e.ora ),( bitarray('0101 1101', endian='big'), True, e.eor ),
		( bitarray('1001 1101', endian='big'), True, e.sta ),( bitarray('1101 1101', endian='big'), True, e.cmp ),
		( bitarray('0011 1101', endian='big'), True, e.andInstruct ),( bitarray('0111 1101', endian='big'), True, e.adc ),
		( bitarray('1011 1101', endian='big'), True, e.lda ),( bitarray('1111 1101', endian='big'), True, e.sbc ),

		( bitarray('0001 1110', endian='big'), True, e.asl ),( bitarray('0011 1110', endian='big'), True, e.rol ) ,
		( bitarray('0101 1110', endian='big'), True, e.lsr ),( bitarray('0111 1110', endian='big'), True, e.ror ) ,
		( bitarray('1000 1010', endian='big'), False, e.txa ),( bitarray('1001 1010', endian='big'), True, e.txs ) ,
		( bitarray('1001 1110', endian='big'), True, e.stx ),( bitarray('1011 1010', endian='big'), False, e.tsx ) ,
		( bitarray('1011 1110', endian='big'), True, e.ldx ) ,
		( bitarray('1010 1010', endian='big'), False, e.tax ),( bitarray('1100 1010', endian='big'), True, e.dex ),
		( bitarray('1101 1110', endian='big'), True, e.dec ),( bitarray('1111 1110', endian='big'), True, e.inc ),

		( bitarray('1110 1010', endian='big'), False, e.nop )]
		self.addressModeLUT = [ (bitarray('01 000', endian='big') , AM.zeroPageX), (bitarray('10 000', endian='big') , AM.immediate),
	                   (bitarray('01 001', endian='big') , AM.zeroPage),  (bitarray('10 001', endian='big') , AM.zeroPage),
	                   (bitarray('01 010', endian='big') , AM.immediate), (bitarray('10 010', endian='big') , AM.accumulator),
	                   (bitarray('01 011', endian='big') , AM.absolute),  (bitarray('10 011', endian='big') , AM.absolute),
	                   (bitarray('01 100', endian='big') , AM.zeroPageY), 
	                   (bitarray('01 101', endian='big') , AM.indirectX), (bitarray('10 101', endian='big') , AM.indirectX),
	                   (bitarray('01 110', endian='big') , AM.absoluteY), 
	                   (bitarray('01 111', endian='big') , AM.absoluteX), (bitarray('10 111', endian='big') , AM.absoluteX),

	                   (bitarray('00 000', endian='big') , AM.immediate),
	                   (bitarray('00 001', endian='big') , AM.zeroPage),
	                   (bitarray('00 011', endian='big') , AM.absolute),
	                   (bitarray('00 100', endian='big') , AM.relative),
	                   (bitarray('00 101', endian='big') , AM.indirectX),
	                   (bitarray('00 111', endian='big') , AM.absoluteX),]
		self.instruction = bitarray('0000 0000',endian='big')

	def setInstruction(self, instruction):
		self.instruction = instruction
	def parse(self):
		decodedInstruction = self.getInstruction()
		if(decodedInstruction[1]):
			decodedAddressMode = self.getAddressMode()
			if(decodedAddressMode == False):
				print('COULDNT FIND ADDRESS MODE, DEFAULTING TO IMPLIED')
				decodedAddressMode = AM.implied
		else:
			decodedAddressMode = AM.implied
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
		print('FAILED TO FIND ADDRESS MODE')
		return False
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
		print('FAILED TO FIND INSTRUCTION, ROUNDING UP')
		element = self.LUT[mid+1]
		if(element[1] == False):
			print('FAILED, IMPLIED ADDRESS MODE')
			return None
		if((ba2int(element[0]) - ba2int(self.instruction)) > 8):
			print('FAILED, ROUNDED TOO FAR')
			return None
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
	def __init__(self):
		r.acc=r.zeros
		r.regX=r.zeros
		r.regY=r.zeros
		r.stackPoint=r.zeros
		r.flagReg=r.zeros
		r.instructReg=r.zeros
		rHigh, rLow = mem.getResetV()
		r.setPCHigh(rHigh)
		r.setPCLow(rLow)
		self.cycle()
	def cycle(self):
		r.setInstructionReg()
		decodedAddressMode, decodedInstruction = decode.parseInstructionReg()
		decodedAddressMode()
		decodedInstruction()
		r.incPC()
	def reset(self):
		r.acc=r.zeros
		r.regX=r.zeros
		r.regY=r.zeros
		r.stackPoint=r.zeros
		r.flagReg=r.zeros
		r.instructReg=r.zeros
		rHigh, rLow = mem.getResetV()
		r.setPCHigh(rHigh)
		r.setPCLow(rLow)
		self.cycle()



r = _registers()
mem = _memory()
ALU = _ALU()
e = _execute()
AM = _runAddressModes(mem)
decode = _decode()
cpu = _cycle()


charBuff = []
def pressEvent(callback):
	charBuff.append(callback.name)
def quitProg():
	#print('tryna quit...')
	keyboard.unhook_all()
	os._exit(1)

for i in range(0,1000000000):
	print(charBuff)

keyboard.on_press(pressEvent)
keyboard.add_hotkey('ctrl+z', quitProg)
