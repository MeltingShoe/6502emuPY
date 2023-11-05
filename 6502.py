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



class registers:
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
	def incPC(self):
		num = ba2int(self.PC)
		num += 1
		num = baFromInt(num)
		self.PC = num
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
class memory:
	global r
	global ALU
	def __init__(self):
		self.memoryBlock = bitarray.zeros(524288,endian='big')
		self.addressLow = bitarray.zeros(8,endian='big')
		self.addressHigh = bitarray.zeros(8,endian='big')
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
		return addIndex
	def read(self):
		self.getEffectiveAddress()
		return(memoryBlock[self.addIndex:self.addIndex+8])
	def write(self, data):
		self.getEffectiveAddress()
		memoryBlock[self.addIndex:self.addIndex+8] = data
		return True
	def setAddressFromPC(self):
		setAddressHigh(r.PC[:8])
		setAddressLow(r.PC[8:])
	def setAddressMode(self, instruction):
		return None   #call the right method to get the target address, then return the target address
	def zeroPageX(self):
		print('zeroPageX')
		self.setAddressHigh(r.zeros)
		self.setAddressLow(r.regX)
	def zeroPage(self):	
		print('zeroPage')
		r.incPC()
		self.setAddressFromPC()
		lowBit = self.read()
		setAddressLow(lowBit)
		self.setAddressHigh(r.zeros)
	def absoluteX(self):
		print('absoluteX')
		r.incPC()
		self.setAddressFromPC()
		highPart = self.read()
		r.incPC()
		self.setAddressFromPC()
		lowPart = self.read()
		ALU.addOffset()
		
		r.PC[:8] = highPart
		r.PC[8:] = lowPart
		r.updateEA()
		r.PC=temp
	def immediate(self):
		r.eA[0] = r.zeros[0]
		print('immediate')
	def absolute(self):
		print('absolute')
		incPC()
		highPart = memMap()
		incPC()
		lowPart = memMap()
		temp = r.PC
		r.PC[:8] = highPart
		r.PC[8:] = lowPart
		r.updateEA()
		r.PC=temp
	def zeroPageY(self):
		print('zeroPageY')
		r.eA[0] = r.zeros[0]
		incPC()
		data = memMap()
		r.eA[1:9] = r.zeros
		data, carry = megaAdder(cIn=0,carry=0,overflow=0,neg=0,zero=0,rA=data,rB=regY)
		r.eA[9:] = data
		r.updateEA()
	def zeroPageXOther(self):
		print('weirdmode')
		r.eA[0] = r.zeros[0]
		#literally fuck this shit lmao
		incPC()
	def absoluteY(self):
		print('absoluteY')
		incPC()
		highPart = memMap()
		incPC()
		lowPart = memMap()
		temp = r.PC
		lowPart, carry = megaAdder(cIn=0,carry=0,overflow=0,neg=0,zero=0,rA=lowPart,rB=regY)
		highPart, carry = megaAdder(cIn=carry,carry=0,overflow=0,neg=0,zero=0,rA=highPart,rB=zeros)
		r.PC[:8] = highPart
		r.PC[8:] = lowPart
		r.updateEA()
		r.PC=temp
	def accumulator(self):
		print('accumulator mode')
		r.eA[0] = r.ones[0]	
class ALU:
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
	def add16bTo8b(self,a,b):
		sL, c = addVal(a[:8],b,carry=0,flags=False)
		sH, c = addVal(a[8:],r.zeros,carry=c,flags=False)
		sF = sH + sL
		return sF
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
	def incVal(self, data, retCarry = False, flags = False, cFlag=False, zFlag=False, nFlag=False, vFlag=False)
		s, c = addVal(data, r.zeros, carry = r.ones[0], flags=flags, cFlag=cFlag, zFlag=zFlag, nFlag=nFlag, vFlag=vFlag)
		if(retCarry):
			return s,c
		return s
	def decVal(self, data, retCarry = False, flags = False, cFlag=False, zFlag=False, nFlag=False, vFlag=False)
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
class execute():
	def __init__(self):
		global r

	def bpl(self):
		if(flagReg[0]==zeros[1]):
			incPC()
			data = memMap()
			sumReg, c3 = megaAdder(cIn=0, rA = PC[8:], rB = data, carry=0,zero=0,overflow=0,neg=0)
			sumReg1, c3 = megaAdder(cIn=c3, rA = PC[:8], rB = zeros, carry=0,zero=0,overflow=0,neg=0)
			r.PC[8:] = sumReg
			r.PC[:8] = sumReg1
			r.updateEA()
	def bmi(self):
		if(flagReg[0]==ones[1]):
			incPC()
			data = memMap()
			sumReg, c3 = megaAdder(cIn=0, rA = PC[8:], rB = data, carry=0,zero=0,overflow=0,neg=0)
			sumReg1, c3 = megaAdder(cIn=c3, rA = PC[:8], rB = zeros, carry=0,zero=0,overflow=0,neg=0)
			r.PC[8:] = sumReg
			r.PC[:8] = sumReg1
			r.updateEA()
	def bvc(self):
		if(flagReg[1]==zeros[1]):
			incPC()
			data = memMap()
			sumReg, c3 = megaAdder(cIn=0, rA = PC[8:], rB = data, carry=0,zero=0,overflow=0,neg=0)
			sumReg1, c3 = megaAdder(cIn=c3, rA = PC[:8], rB = zeros, carry=0,zero=0,overflow=0,neg=0)
			r.PC[8:] = sumReg
			r.PC[:8] = sumReg1
			r.updateEA()
	def bvs(self):
		if(flagReg[1]==ones[1]):
			incPC()
			data = memMap()
			sumReg, c3 = megaAdder(cIn=0, rA = PC[8:], rB = data, carry=0,zero=0,overflow=0,neg=0)
			sumReg1, c3 = megaAdder(cIn=c3, rA = PC[:8], rB = zeros, carry=0,zero=0,overflow=0,neg=0)
			r.PC[8:] = sumReg
			r.PC[:8] = sumReg1
			r.updateEA()
	def bcc(self):
		if(flagReg[7]==zeros[7]):
			incPC()
			data = memMap()
			sumReg, c3 = megaAdder(cIn=0, rA = PC[8:], rB = data, carry=0,zero=0,overflow=0,neg=0)
			sumReg1, c3 = megaAdder(cIn=c3, rA = PC[:8], rB = zeros, carry=0,zero=0,overflow=0,neg=0)
			r.PC[8:] = sumReg
			r.PC[:8] = sumReg1
			r.updateEA()
	def bcs(self):
		if(flagReg[7]==ones[7]):
			incPC()
			data = memMap()
			sumReg, c3 = megaAdder(cIn=0, rA = PC[8:], rB = data, carry=0,zero=0,overflow=0,neg=0)
			sumReg1, c3 = megaAdder(cIn=c3, rA = PC[:8], rB = zeros, carry=0,zero=0,overflow=0,neg=0)
			r.PC[8:] = sumReg
			r.PC[:8] = sumReg1
			r.updateEA()
	def bne(self):
		if(flagReg[6]==zeros[6]):
			incPC()
			data = memMap()
			sumReg, c3 = megaAdder(cIn=0, rA = PC[8:], rB = data, carry=0,zero=0,overflow=0,neg=0)
			sumReg1, c3 = megaAdder(cIn=c3, rA = PC[:8], rB = zeros, carry=0,zero=0,overflow=0,neg=0)
			r.PC[8:] = sumReg
			r.PC[:8] = sumReg1
			r.updateEA()
	def beq(self):
		if(flagReg[6]==ones[6]):
			incPC()
			data = memMap()
			sumReg, c3 = megaAdder(cIn=0, rA = PC[8:], rB = data, carry=0,zero=0,overflow=0,neg=0)
			sumReg1, c3 = megaAdder(cIn=c3, rA = PC[:8], rB = zeros, carry=0,zero=0,overflow=0,neg=0)
			r.PC[8:] = sumReg
			r.PC[:8] = sumReg1
			r.updateEA()
	def brk(self):
		pass
	def jsrAbsolute(self):
		incPC()
		highPart = memMap()
		incPC()
		lowPart = memMap()
		incPC()
		stack[r.stackPoint:r.stackPoint+16] = r.PC
		r.stackPoint += 16
		r.PC[:8] = highPart
		r.PC[8:] = lowPart
		r.updateEA()
	def rti(self):
		pass
	def rts(self):
		r.stackPoint -= 16
		r.PC = stack[r.stackPoint:r.stackPoint+16]
		r.updateEA()
	def php(self):
		tpc = r.PC
		r.PC=stackPoint
		r.updateEA()
		first = r.eA[1:17]
		incPC()
		last = r.eA[1:17]
		stack[ba2int(first),ba2int(last)] = r.flagReg
		r.PC = tpc
		incPC()
	def plp(self):
		tpc = r.PC
		r.PC=stackPoint
		r.updateEA()
		first = r.eA[1:17]
		incPC()
		last = r.eA[1:17]
		data = stack[ba2int(first),ba2int(last)]
		r.flagReg = data
		r.PC = tpc
		incPC()
	def pha(self):
		tpc = r.PC
		r.PC=stackPoint
		r.updateEA()
		first = r.eA[1:17]
		incPC()
		last = r.eA[1:17]
		stack[ba2int(first),ba2int(last)] = r.acc
		r.PC = tpc
		incPC()
	def pla(self):
		tpc = r.PC
		r.PC=stackPoint
		r.updateEA()
		first = r.eA[1:17]
		incPC()
		last = r.eA[1:17]
		data = stack[ba2int(first),ba2int(last)]
		r.acc = data
		r.PC = tpc
		incPC()
	def dey(self):
		#print('dey')
		r.regY, carry= megaAdder(cIn=r.zeros[7],rA=r.regY, rB=bitarray('0000 0001',endian='big'), overflow=False, carry=False, sub=True)
		#print('DEY data: ',r.regX)
		incPC()
	def tay(self):
		#print('tay')
		r.regY = r.acc
		#print('TAY r.regY: ',r.regY)
		incPC()
	def iny(self):
		#print('iny')
		r.regY, carry= megaAdder(cIn=r.zeros[7],rA=r.regY, rB=bitarray('0000 0001',endian='big'), overflow=False, carry=False)
		#print('INY data: ',r.regY)
		incPC()
	def inx(self):
		#print('inx')
		r.regX, carry= megaAdder(cIn=r.zeros[7],rA=r.regX, rB=bitarray('0000 0001',endian='big'), overflow=False, carry=False)
		#print('INX data: ',r.regX)
		incPC()
	def clc(self):
		#print('clc')
		r.flagReg[7] = r.zeros[7]
		#print('CLC flags: ',r.flagReg)
		incPC()
	def sec(self):
		#print('sec')
		r.flagReg[7] = r.ones[7]
		#print('SEC flags: ',r.flagReg)
		incPC()
	def cli(self):
		#print('cli')
		r.flagReg[5] = r.zeros[7]
		#print('CLI flags: ',r.flagReg)
		incPC()
	def sei(self):
		#print('sei')
		r.flagReg[5] = r.ones[7]
		#print('SEI flags: ',r.flagReg)
		incPC()
	def tya(self):
		#print('tya')
		r.acc = r.regY
		#print('TYA r.acc: ',r.acc)
		incPC()
	def clv(self):
		#print('clv')
		r.flagReg[1] = r.zeros[7]
		#print('CLV flags: ',r.flagReg)
		incPC()
	def txa(self):
		#print('txa')
		r.acc = r.regX
		#print('TXA r.acc: ',r.acc)
		incPC()
	def txs(self):
		#print('txs')
		r.stackPoint = r.regX
		#print('TXS stack: ',r.stackPoint)
		incPC()
	def tax(self):
		#print('tax')
		r.regX = r.acc
		#print('TAX r.regX: ',r.regX)
		incPC()
	def tsx(self):
		#print('tsx')
		r.regX = r.stackPoint
		#print('TSX r.regX: ',r.regX)
		incPC()
	def dex(self):
		#print('dex')
		r.regX, carry= megaAdder(cIn=r.zeros[7],rA=r.regX, rB=bitarray('0000 0001',endian='big'), overflow=False, carry=False, sub=True)
		#print('DEX data: ',r.regX)
		incPC()
	def nop(self):
		#print('nop')
		incPC()
	def bit(self):
		#print('bit')
		#print('effective address: ',r.eA)
		data = memMap()
		#print('r.acc, data',r.acc,data)
	def jmp(self):
		incPC()
		lowPart = memMap()
		incPC()
		highPart = memMap()
		r.PC[:8] = highPart
		r.PC[8:] = lowPart
		r.updateEA()
		highPart = memMap()
		incPC()
		lowPart = memMap()
		r.PC[:8] = highPart
		r.PC[8:] = lowPart
		r.updateEA()
	def jmpAbsolute(self):
		highPart = memMap()
		incPC()
		lowPart = memMap()
		r.PC[:8] = highPart
		r.PC[8:] = lowPart
	def sty(self):
		#print('sty')
		#print('effective address: ',r.eA)
		memMap(write=True,data=r.regY)
		#print('STY r.regY: ',r.regY)
		incPC()
	def ldy(self):
		#print('ldy')
		#print('effective address: ',r.eA)
		data = memMap()
		r.regY = data
		#print('LDY r.regY: ',r.regY)
		incPC()
	def cpy(self):
		#print('cpy')
		#print('effective address: ',r.eA)
		data = memMap()
		#print('y, data',r.regY,data)
		r.flagReg[7]=r.zeros[7]
		megaAdder(cIn=r.flagReg[7],rA=r.regY, rB=data, overflow=False, sub=True)
		#print('CPX flags: ',r.flagReg)
		incPC()
	def cpx(self):
		#print('cpx')
		#print('effective address: ',r.eA)
		data = memMap()
		#print('x, data',r.regX,data)
		r.flagReg[7]=r.zeros[7]
		megaAdder(cIn=r.flagReg[7],rA=r.regX, rB=data, overflow=False, sub=True)
		#print('CPX flags: ',r.flagReg)
		incPC()
	def ora(self):
		#print('ora')
		#print('effective address: ',r.eA)
		data = memMap()
		#print('acc, data',r.acc,data)
		r.acc = r.acc | data
		#print('ORA r.acc: ',r.acc)
		megaAdder(carry=False,overflow=False,rB=r.zeros)
		incPC()
	def eor(self):
		#print('eor')
		#print('effective address: ',r.eA)
		data = memMap()
		#print('r.acc, data',r.acc,data)
		r.acc = r.acc ^ data
		#print('EOR r.acc: ',r.acc)
		megaAdder(carry=False,overflow=False,rB=r.zeros)
		incPC()
	def sta(self):
		#print('staC')
		#print('effective address: ',r.eA)
		memMap(write=True,data=r.acc)
		#print('STA DONE')
		incPC()
	def cmp(self):
		#print('cmp')
		#print('effective address: ',r.eA)
		data = memMap()
		#print('r.acc, data',r.acc,data)
		r.flagReg[7]=r.zeros[7]
		megaAdder(cIn=r.flagReg[7],rA=r.acc, rB=data, overflow=False, sub=True)
		#print('CMP flags: ',r.flagReg)
		incPC()
	def andInstruct(self):
		#print('and')
		#print('effective address: ',r.eA)
		data = memMap()
		#print('r.acc, data',r.acc,data)
		r.acc = r.acc & data
		#print('AND r.acc: ',r.acc)
		megaAdder(carry=False,overflow=False,rB=r.zeros)
		incPC()
	def adc(self):
		#print('adc')
		#print('effective address: ',r.eA)
		data = memMap()
		#print('r.acc, data',r.acc,data)
		r.acc, carryOut = megaAdder(cIn=r.flagReg[7],rA=r.acc, rB=data)
		#print('ADC r.acc: ',r.acc)
		incPC()
	def lda(self):
		print('lda')
		print('PC: ',r.PC)
		#print('effective address: ',r.eA)
		data = memMap()
		print('data: ',data)
		r.acc = data
		print('LDA r.acc: ',data)
		incPC()

	def sbc(self):
		#print('sbc')
		#print('effective address: ',r.eA)
		data = memMap()
		#print('r.acc, data',r.acc,data)
		r.acc, carryOut = megaAdder(cIn=r.flagReg[7],rA=r.acc, rB=data, sub=True)
		#print('SBC r.acc: ',r.acc)
		incPC()
	def asl(self):
		#print('asl')
		#print('effective address: ',r.eA)
		data = memMap()
		#print('data',data)
		r.flagReg[7]=data[0]
		data[0]=data[1]
		data[1]=data[2]
		data[2]=data[3]
		data[3]=data[4]
		data[4]=data[5]
		data[5]=data[6]
		data[6]=data[7]
		data[7]=r.zeros[7]
		megaAdder(cIn=r.flagReg[7],rA=data, rB=r.zeros, overflow=False)
		memMap(write=True,data=data)
		incPC()
	def rol(self):
		#print('rol')
		#print('effective address: ',r.eA)
		data = memMap()
		#print('data',data)
		temp = r.flagReg[7]
		r.flagReg[7]=data[0]
		data[0]=data[1]
		data[1]=data[2]
		data[2]=data[3]
		data[3]=data[4]
		data[4]=data[5]
		data[5]=data[6]
		data[6]=data[7]
		data[7]=temp
		megaAdder(cIn=r.flagReg[7],rA=data, rB=r.zeros, overflow=False)
		memMap(write=True,data=data)
		incPC()
	def lsr(self):
		#print('lsr')
		#print('effective address: ',r.eA)
		data = memMap()
		#print('data',data)
		r.flagReg[7]=data[7]
		data[7]=data[6]
		data[6]=data[5]
		data[5]=data[4]
		data[4]=data[3]
		data[3]=data[2]
		data[2]=data[1]
		data[1]=data[0]
		data[0]=r.zeros[0]
		megaAdder(cIn=r.flagReg[7],rA=data, rB=r.zeros, overflow=False)
		memMap(write=True,data=data)
		incPC()
	def ror(self):
		#print('ror')
		#print('effective address: ',r.eA)
		data = memMap()
		#print('data',data)
		temp = r.flagReg[7]
		r.flagReg[7]=data[7]
		data[7]=data[6]
		data[6]=data[5]
		data[5]=data[4]
		data[4]=data[3]
		data[3]=data[2]
		data[2]=data[1]
		data[1]=data[0]
		data[0]=temp
		megaAdder(cIn=r.flagReg[7],rA=data, rB=r.zeros, overflow=False)
		memMap(write=True,data=data)
		incPC()
	def stx(self):
		#print('staC')
		#print('effective address: ',r.eA)
		memMap(write=True,data=r.regX)
		#print('STX DONE')
		incPC()
	def ldx(self):
		#print('ldx')
		#print('effective address: ',r.eA)
		data = memMap()
		r.regX = data
		#print('LDX r.acc: ',r.acc)
		incPC()
	def dec(self):
		#print('dec')
		#print('effective address: ',r.eA)
		data = memMap()
		#print('data',data)
		data, carry = megaAdder(cIn=r.zeros[7],carry=False,overflow=False,rA=data, rB=ones[0], sub=True)
		memMap(write=True,data=data)
		incPC()
	def inc(self):
		#print('inc')
		#print('effective address: ',r.eA)
		data = memMap()
		#print('data',data)
		data, carry = megaAdder(cIn=r.zeros[7],rA=data, rB=bitarray('0000 0001',endian='big'), overflow=False, carry=False, sub=True)
		memMap(write=True,data=data)
		incPC()
class doAddressMode:
	def zeroPageX(self):
		print('zeroPageX')
		r.eA[0] = r.zeros[0]
		incPC()
		data = memMap()
		r.eA[1:9] = r.zeros
		data, carry = megaAdder(cIn=0,carry=0,overflow=0,neg=0,zero=0,rA=data,rB=regX)
		r.eA[9:] = data
		r.updateEA()
	def zeroPage(self):	
		print('zeroPage')
		r.eA[0] = r.zeros[0]
		incPC()
		data = memMap()
		r.eA[1:9] = r.zeros
		r.eA[9:] = data
		r.updateEA()
	def absoluteX(self):
		print('absoluteX')
		incPC()
		highPart = memMap()
		incPC()
		lowPart = memMap()
		temp = r.PC
		lowPart, carry = megaAdder(cIn=0,carry=0,overflow=0,neg=0,zero=0,rA=lowPart,rB=regX)
		highPart, carry = megaAdder(cIn=carry,carry=0,overflow=0,neg=0,zero=0,rA=highPart,rB=zeros)
		r.PC[:8] = highPart
		r.PC[8:] = lowPart
		r.updateEA()
		r.PC=temp
	def immediate(self):
		r.eA[0] = r.zeros[0]
		print('immediate')
	def absolute(self):
		print('absolute')
		incPC()
		highPart = memMap()
		incPC()
		lowPart = memMap()
		temp = r.PC
		r.PC[:8] = highPart
		r.PC[8:] = lowPart
		r.updateEA()
		r.PC=temp
	def zeroPageY(self):
		print('zeroPageY')
		r.eA[0] = r.zeros[0]
		incPC()
		data = memMap()
		r.eA[1:9] = r.zeros
		data, carry = megaAdder(cIn=0,carry=0,overflow=0,neg=0,zero=0,rA=data,rB=regY)
		r.eA[9:] = data
		r.updateEA()
	def zeroPageXOther(self):
		print('weirdmode')
		r.eA[0] = r.zeros[0]
		#literally fuck this shit lmao
		incPC()
	def absoluteY(self):
		print('absoluteY')
		incPC()
		highPart = memMap()
		incPC()
		lowPart = memMap()
		temp = r.PC
		lowPart, carry = megaAdder(cIn=0,carry=0,overflow=0,neg=0,zero=0,rA=lowPart,rB=regY)
		highPart, carry = megaAdder(cIn=carry,carry=0,overflow=0,neg=0,zero=0,rA=highPart,rB=zeros)
		r.PC[:8] = highPart
		r.PC[8:] = lowPart
		r.updateEA()
		r.PC=temp
	def accumulator(self):
		print('accumulator mode')
		r.eA[0] = r.ones[0]
class instruction:
	def __init__(self):
		print("i am instruction class :)")
r = registers()
mem = memory()
ALU = ALU()
e = execute()
dam = doAddressMode()


def search(instruction):
	print("search instruction",instruction)
	#this is not the real LUT, this has the last 2 bits moved to the front and address bits swapped with 1s
	LUT=[( bitarray('0000 0000', endian='big') , e.brk ),( bitarray('0000 0010', endian='big') , e.php ),
		( bitarray('0000 0100', endian='big') , e.bpl ),( bitarray('0000 0110', endian='big') , e.clc ),
		( bitarray('0000 1000', endian='big') , e.jsrAbsolute ),( bitarray('0000 1010', endian='big') , e.plp ), 
		( bitarray('0000 1100', endian='big') , e.bmi ),( bitarray('0000 1110', endian='big') , e.sec ),
		( bitarray('0000 1111', endian='big') , e.bit ),

		( bitarray('0001 0000', endian='big') , e.rti ),( bitarray('0001 0010', endian='big') , e.pha ),
		( bitarray('0001 0100', endian='big') , e.bvc ),( bitarray('0001 0110', endian='big') , e.cli ),
		( bitarray('0001 0111', endian='big') , e.jmp ),( bitarray('0001 1000', endian='big') , e.rts ), 
		( bitarray('0001 1010', endian='big') , e.pla ),( bitarray('0001 1100', endian='big') , e.bvs ),
		( bitarray('0001 1110', endian='big') , e.sei ),( bitarray('0001 1111', endian='big') , e.jmpAbsolute ),

		( bitarray('0010 0010', endian='big') , e.dey ),( bitarray('0010 0100', endian='big') , e.bcc ),
		( bitarray('0010 0110', endian='big') , e.tya ),( bitarray('0010 0111', endian='big') , e.sty ),
		( bitarray('0010 1010', endian='big') , e.tay ),( bitarray('0010 1100', endian='big') , e.bcs ) ,
		( bitarray('0010 1110', endian='big') , e.clv ),( bitarray('0010 1111', endian='big') , e.ldy ) ,
		 
		( bitarray('0011 0010', endian='big') , e.iny ),( bitarray('0011 0100', endian='big') , e.bne ),
		( bitarray('0011 0111', endian='big') , e.cpy ),( bitarray('0011 1010', endian='big') , e.inx ) ,
		( bitarray('0011 1100', endian='big') , e.beq ),( bitarray('0011 1111', endian='big') , e.cpx ) ,

		( bitarray('0100 0111', endian='big') , e.ora ),( bitarray('0101 0111', endian='big') , e.eor ),
		( bitarray('0110 0111', endian='big') , e.sta ),( bitarray('0111 0111', endian='big') , e.cmp ),
		( bitarray('0100 1111', endian='big') , e.andInstruct ),( bitarray('0101 1111', endian='big') , e.adc ),
		( bitarray('0110 1111', endian='big') , e.lda ),( bitarray('0111 1111', endian='big') , e.sbc ),

		( bitarray('1000 0111', endian='big') , e.asl ),( bitarray('1000 1111', endian='big') , e.rol ) ,
		( bitarray('1001 0111', endian='big') , e.lsr ),( bitarray('1001 1111', endian='big') , e.ror ) ,
		( bitarray('1010 0010', endian='big') , e.txa ),( bitarray('1010 0110', endian='big') , e.txs ) ,
		( bitarray('1010 0111', endian='big') , e.stx ),( bitarray('1010 1110', endian='big') , e.tsx ) ,
		( bitarray('1010 1111', endian='big') , e.ldx ) ,
		( bitarray('1010 1010', endian='big') , e.tax ),( bitarray('1011 0010', endian='big') , e.dex ),
		( bitarray('1011 0111', endian='big') , e.dec ),( bitarray('1011 1111', endian='big') , e.inc ),

		( bitarray('1110 1010', endian='big') , e.nop )]

	k=bitarray('0000 0000', endian='big')
	k[:2] = instruction[6:]
	k[2:] = instruction[:6]

	print('K: ',k)

	low = 0
	high = len(LUT)-1
	mid = (high+low)//2
	while(low<=high):
		key = LUT[mid]
		key = key[0]
		#print('hopehope',LUT[mid])
		if(k == key):
			
			return(LUT[mid])
		if(k < key):
			#print(k,' IS LESS THAN ',key)
			high = mid - 1
			mid = ( high + low ) // 2
		if(k > key):
			#print(k, ' IS MORE THAN ', key)
			low = mid + 1
			mid = ( high + low ) // 2
	key = LUT[mid+1]
	#print('no find', key)
	return(key)

def baFromInt(integer):
	ba = int2ba(integer,endian='big')
	buffer = bitarray('0000 0000', endian='big')
	index = len(ba)
	bi=8
	while index > 0:
		index-=1
		bi-=1
		buffer[bi]=TESTTEMP[index]
	return buffer


def fetch():
	global r
	#print('fetchdatshi')
	#print(r.eA,'\n')
	data = memMap()
	r.instructReg = data
	print('insReg',r.instructReg)




def getAddr(instruction):
	found = search(instruction)
	print('found',found)
	foundIns = found[0]
	addrM = foundIns[5:]
	grp = foundIns[:2]
	if(addrM==bitarray('111',endian='big')):
		addrM = instruction[3:6]
		print("group: ",grp, ' addrM: ',addrM,' found: ',found)
		if(grp == bitarray('01',endian='big')):
			if(addrM==bitarray('000',endian='big')):
				dam.zeroPageX()
			elif(addrM==bitarray('001',endian='big')):
				dam.zeroPage()
			elif(addrM==bitarray('010',endian='big')):
				dam.immediate()
			elif(addrM==bitarray('011',endian='big')):
				dam.absolute()
			elif(addrM==bitarray('100',endian='big')):
				dam.zeroPageY()
			elif(addrM==bitarray('101',endian='big')):
				dam.zeroPageXOther()
			elif(addrM==bitarray('110',endian='big')):
				dam.absoluteY()
			elif(addrM==bitarray('111',endian='big')):
				dam.absoluteX()
		elif(grp == bitarray('10',endian='big')):
			if(addrM==bitarray('000',endian='big')):
				dam.immediate()
			elif(addrM==bitarray('001',endian='big')):
				dam.zeroPage()
			elif(addrM==bitarray('010',endian='big')):
				dam.accumulator()
			elif(addrM==bitarray('011',endian='big')):
				dam.absolute()
			elif(addrM==bitarray('101',endian='big')):
				dam.zeroPageXOther()
			elif(addrM==bitarray('111',endian='big')):
				dam.absoluteX()
		elif(grp == bitarray('00',endian='big')):
			if(addrM==bitarray('000',endian='big')):
				dam.immediate()
			elif(addrM==bitarray('001',endian='big')):
				dam.zeroPage()
			elif(addrM==bitarray('011',endian='big')):
				dam.absolute()
			elif(addrM==bitarray('101',endian='big')):
				dam.zeroPageXOther()
			elif(addrM==bitarray('111',endian='big')):
				dam.absoluteX()

	found[1]()
	return found

def cycle():
	global r
	print('CYCLE')
	fetch()
	getAddr(r.instructReg)
	#print("ACC: ",r.acc)

def pressEvent(callback):
	charBuff.append(callback.name)
def quitProg():
	#print('tryna quit...')
	keyboard.unhook_all()
	os._exit(1)

fetch()
incPC()
getAddr(r.instructReg)
i2=0
while i2<10:
	i2+=1
	cycle()
	print("eA: ",eA)
	print("acc: ",r.acc)

keyboard.on_press(pressEvent)
keyboard.add_hotkey('ctrl+z', quitProg)
