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
	buffer = bitarray('0000 0000 0000 0000', endian='big')
	index = len(ba)
	bi=16
	while index > 0:
		index-=1
		bi-=1
		buffer[bi]=ba[index]
	return buffer


class _logger:
	global r
	def __init__(self):
		self.printRegs = True
		self.regOuts = ""
		self.printRWData = True
		self.printRWAddress = True
		self.memOuts = ""
		self.printAddressMode = True
		self.AMOut = ""
		self.printInstruction = True
		self.instructOut = ""
	def setRegOuts(self):
		print(r.PC)
		self.regOuts = "PC: "+str(hex(ba2int(r.PC)))+" ACC:"+str(hex(ba2int(r.acc)))+" regX:"+str(hex(ba2int(r.regX)))+" regY:"+str(hex(ba2int(r.regY)))+" Flags:"+str(hex(ba2int(r.flagReg)))+" stackPoint:"+str(hex(ba2int(r.stackPoint)))+" instruction:"+str(hex(ba2int(r.instructReg)))
	def addMemOuts(self,data):
		self.memOuts += data
	def addAMOut(self,data):
		self.AMOut += data
	def addInstructOut(self,data):
		self.instructOut += data
	def output(self):
		print("===========================================================")
		print('\n')
		self.setRegOuts()
		print(self.regOuts)
		print('\n')
		print(self.memOuts)
		print('\n')
		print(self.instructOut)
		self.regOuts = ""
		self.memOuts = ""
		self.AMOut = ""
		self.instructOut = ""

l = _logger()

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
		self.savedPC = self.PC
	def savePC(self):
		self.savedPC = self.PC
	def restorePC(self):
		self.PC = self.savedPC
	def setPCLow(self,inp):
		self.PC[8:] = inp
		print('L',self.PC)
	def setPCHigh(self,inp):
		self.PC[:8] = inp
		print('H',self.PC)
	def getPCLow(self):
		return self.PC[8:]
	def getPCHigh(self):
		return self.PC[:8]
	def incPC(self):
		h=self.PC
		x = ba2int(h)
		x+=1
		x=baFromInt(x)
		self.PC = x
		print('PC: ',h,' -> ',self.PC)
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
	global l
	def __init__(self):
		self.memoryBlock = bitarray(524288,endian='big')
		self.address = bitarray('0000 0000 0000 0000',endian='big')
		self.eStart = (ba2int(self.address)*8)
		self.eStop = self.eStart+8
		self.resetVector = bitarray('0000 0000 0000 0000',endian='big')
		self.nmiVector = bitarray('0000 1111 0000 0000',endian='big')
		self.irqVector = bitarray('0000 1100 0000 0000',endian='big')
		self.accMode = False
		self.addIndex = 0
	def readAddress(self, inAddress):
		start = inAddress * 8
		stop = (inAddress + 1) * 8
		if(accMode):
			return r.acc
		return self.memoryBlock[start:stop]
	def getAddressOffset(self, inAddress, addressMode):
		out = addressMode(inAddress)
		return out
	

	def zeroPageX(self, inAddress):
		self.accMode = False
		print('Run zeroPageX')
		return(ba2int(r.zeros + r.regX))
	def zeroPage(self, inAddress):	
		self.accMode = False
		print('Run zeroPage')
		l = self.readAddress(inAddress)
		return r.zeros+l
	def absoluteX(self, inAddress):
		self.accMode = False
		print('Run absoluteX')
		h = self.readAddress(inAddress)
		l = self.readAddress(inAddress+1)
		index = ba2int(h+l)
		index = index + ba2int(r.regX)
		return(index)
	def immediate(self, inAddress):
		self.accMode = False
		print('Run immediate')
		return(inAddress+1)
		
	def absolute(self, inAddress):
		self.accMode = False
		print('Run absolute')
		h = self.readAddress(inAddress)
		l = self.readAddress(inAddress+1)
		return h+l
		
	def zeroPageY(self, inAddress):
		self.accMode = False
		print('Run zeroPageY')
		return(ba2int(r.zeros + r.regY))
	def indirectX(self, inAddress):
		self.accMode = False
		print('Run indirectX')
		r.incPC()
		data = mem.read()
		mem.setAddressHigh(r.zeros)
		mem.setAddressLow(data)
		high = mem.read()
		data = ALU.incVal(data)
		mem.setAddressLow(data)
		low = mem.read()
		mem.setAddressHigh(high)
		mem.setAddressLow(low)
	def absoluteY(self, inAddress):
		self.accMode = False
		print('Run absoluteY')
		h = self.readAddress(inAddress)
		l = self.readAddress(inAddress+1)
		index = ba2int(h+l)
		index = index + ba2int(r.regY)
		return(index)
	def accumulator(self, inAddress):
		print('Run accumulator')
		self.accMode = True
		return self.accMode
	def relative(self, inAddress):
		self.accMode = False
		print('Run relative')
		r.incPC()
	def implied(self, inAddress):
		self.accMode = False
		print('Run implied')
		return(inAddress)

	def updateAddress(self):
		self.address = r.PC
	def updateEA(self):
		self.updateAddress()
		self.eStart = ba2int(self.address) * 8
		self.eStop = self.eStart+8
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
		self.address = self.getAddressHigh() + self.getAddressLow()
		print('addy: ',self.address)
		
		addy = self.address

		print('eA: ',addy)
		self.addIndex = ba2int(addy)
		return self.addIndex
	def read(self):
		print('Reading')

		if(self.accMode):
			print('ACC: ')
			print(str(hex(ba2int(r.acc))))
			return r.acc
		else:
			self.updateEA()
			print('data' + str(hex(ba2int(self.memoryBlock[self.eStart:self.eStop]))))

			return(self.memoryBlock[self.eStart:self.eStop])
	def write(self, data):
		print('Writing')

		if(self.accMode):
			print('ACC: ')
			print(str(hex(ba2int(r.acc))))
			r.acc = data
		else:
			self.updateEA()
			self.memoryBlock[self.eStart:self.eStop] = data
			print(str(hex(ba2int(self.memoryBlock[self.eStart:self.eStop]))))
			return True
	def setAddressFromPC(self):
		self.setAddressHigh(r.PC[:8])
		self.setAddressLow(r.PC[8:])
class _runAddressModes:
	global mem
	global l
	def zeroPageX(self):
		mem.accMode = False
		print('Run zeroPageX')
		mem.setAddressHigh(r.zeros)
		mem.setAddressLow(r.regX)
	def zeroPage(self):	
		mem.accMode = False
		print('Run zeroPage')
		r.incPC()
		lowBit = mem.read()
		r.incPC()
		r.savePC()
		r.PC = r.zeros+lowBit
		print(r.PC)
	def absoluteX(self):
		mem.accMode = False
		print('Run absoluteX')
		r.incPC()
		mem.setAddressFromPC()
		highPart = mem.read()
		r.incPC()
		mem.setAddressFromPC()
		lowPart = mem.read()
		highPart, lowPart = ALU.addOffset(highPart,lowPart,r.regX)
		mem.setAddressHigh(highPart)
		mem.setAddressLow(lowPart)
	def immediate(self):
		mem.accMode = False
		print('Run immediate')
		r.incPC()
		mem.setAddressFromPC()
	def absolute(self):
		mem.accMode = False
		print('Run absolute')
		r.incPC()
		
	def zeroPageY(self):
		mem.accMode = False
		print('Run zeroPageY')
		mem.setAddressHigh(r.zeros)
		mem.setAddressLow(r.regY)
	def indirectX(self):
		mem.accMode = False
		print('Run indirectX')
		r.incPC()
		data = mem.read()
		mem.setAddressHigh(r.zeros)
		mem.setAddressLow(data)
		high = mem.read()
		data = ALU.incVal(data)
		mem.setAddressLow(data)
		low = mem.read()
		mem.setAddressHigh(high)
		mem.setAddressLow(low)
	def absoluteY(self):
		mem.accMode = False
		print('Run absoluteY')
		r.incPC()
		mem.setAddressFromPC()
		highPart = mem.read()
		r.incPC()
		mem.setAddressFromPC()
		lowPart = mem.read()
		highPart, lowPart = ALU.addOffset(highPart,lowPart,r.regY)
		mem.setAddressHigh(highPart)
		mem.setAddressLow(lowPart)
	def accumulator(self):
		print('Run accumulator')
		mem.accMode = True
	def relative(self):
		mem.accMode = False
		print('Run relative')
		r.incPC()
	def implied(self):
		print('Run implied')
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
		sL, c = self.addVal(low,offset,carry=0,flags=False)
		sH, c = self.addVal(high,r.zeros,carry=c,flags=False)
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
		r.acc = self.subVal(r.acc, data)
	def incVal(self, data, retCarry = False, flags = False, cFlag=False, zFlag=False, nFlag=False, vFlag=False):
		s, c = self.addVal(data, r.zeros, carry = r.ones[0], flags=flags, cFlag=cFlag, zFlag=zFlag, nFlag=nFlag, vFlag=vFlag)
		if(retCarry):
			return s,c
		return s
	def decVal(self, data, retCarry = False, flags = False, cFlag=False, zFlag=False, nFlag=False, vFlag=False):
		s, c = self.addVal(data, r.ones, carry = r.zeros[0], flags=flags, cFlag=cFlag, zFlag=zFlag, nFlag=nFlag, vFlag=vFlag)
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
	def rti(self):
		print('Run RTI')
	def bpl(self):          #DONE
		print('Run BPL')
		if(r.nFlag()==r.zeros[1]):
			data = mem.read()
			high, low = ALU.addOffset(r.getPCHigh(),r.getPCLow(),data)
			r.setPCHigh(high)
			r.setPCLow(low)
	def bmi(self):        #DONE
		print('Run BMI')
		if(r.nFlag()==r.ones[1]):
			data = mem.read()
			high, low = ALU.addOffset(r.getPCHigh(),r.getPCLow(),data)
			r.setPCHigh(high)
			r.setPCLow(low)
	def bvc(self):          #DONE
		print('Run BVC')
		if(r.vFlag()==r.zeros[1]):
			data = mem.read()
			high, low = ALU.addOffset(r.getPCHigh(),r.getPCLow(),data)
			r.setPCHigh(high)
			r.setPCLow(low)
	def bvs(self):        #DONE
		print('Run BVS')
		if(r.vFlag()==r.ones[1]):
			data = mem.read()
			high, low = ALU.addOffset(r.getPCHigh,r.getPCLow,data)
			r.setPCHigh(high)
			r.setPCLow(low)
	def bcc(self):        #DONE
		print('Run BCC')
		if(r.cFlag()==r.zeros[1]):
			data = mem.read()
			high, low = ALU.addOffset(r.getPCHigh,r.getPCLow,data)
			r.setPCHigh(high)
			r.setPCLow(low)
	def bcs(self):        #DONE
		print('Run BCS')
		if(r.cFlag()==r.ones[1]):
			data = mem.read()
			high, low = ALU.addOffset(r.getPCHigh,r.getPCLow,data)
			r.setPCHigh(high)
			r.setPCLow(low)
	def bne(self):         #DONE
		print('Run BNE')
		if(r.zFlag()==r.zeros[1]):
			data = mem.read()
			high, low = ALU.addOffset(r.getPCHigh,r.getPCLow,data)
			r.setPCHigh(high)
			r.setPCLow(low)
	def beq(self):          #DONE
		print('Run BEQ')
		if(r.zFlag()==r.ones[1]):
			data = mem.read()
			high, low = ALU.addOffset(r.getPCHigh,r.getPCLow,data)
			r.setPCHigh(high)
			r.setPCLow(low)
	def brk(self):
		print('Run BRK')
		pass
	def jsrAbsolute(self):           #DONE
		print('Run JSR')
		r.incPC()
		lowBit = mem.read()
		r.incPC()
		highBit = mem.read()
		r.incPC()
		mem.setAddressHigh(bitarray('0000 0001',endian='big'))
		mem.setAddressLow(r.stackPoint)
		mem.write(r.getPCHigh())
		r.stackPoint = ALU.incVal(r.stackPoint)
		mem.setAddressLow(r.stackPoint)
		mem.write(r.getPCLow())
		r.stackPoint = ALU.incVal(r.stackPoint)
		r.setPCLow(lowBit)
		r.setPCHigh(highBit)

	def rts(self):                #DONE
		print('Run RTS')
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
		print('Run PHP')
		mem.setAddressLow(r.stackPoint)
		mem.setAddressHigh(bitarray('0000 0001',endian='big'))
		mem.write(r.flagReg)
		r.stackPoint = ALU.incVal(r.stackPoint)
		r.incPC()
	def plp(self):          #DONE
		print('Run PLP')
		mem.setAddressLow(r.stackPoint)
		mem.setAddressHigh(bitarray('0000 0001',endian='big'))
		r.flagReg = mem.read()
		r.stackPoint = ALU.decVal(r.stackPoint)
		r.incPC()
	def pha(self):              #DONE
		print('Run PHA')
		mem.setAddressLow(r.stackPoint)
		mem.setAddressHigh(bitarray('0000 0001',endian='big'))
		mem.write(r.acc)
		r.stackPoint = ALU.incVal(r.stackPoint)
		r.incPC()
	def pla(self):              #DONE
		print('Run PLA')
		mem.setAddressLow(r.stackPoint)
		mem.setAddressHigh(bitarray('0000 0001',endian='big'))
		r.acc = mem.read()
		r.stackPoint = ALU.decVal(r.stackPoint)
		r.incPC()
	def dey(self):         #DONE
		print('Run DEY')
		r.regY = ALU.decVal(regY)
		r.incPC()
	def tay(self):                #DONE
		print('Run TAY')
		r.regY = r.acc
		r.incPC()
	def iny(self):     #DONE
		print('Run INY')
		r.regY = ALU.incVal(regY)
		r.incPC()
	def inx(self):      #DONE
		print('Run INX')
		r.regX = ALU.incVal(r.regX)
		r.incPC()
	def clc(self):          #DONE
		print('Run CLC')
		r.cFlag(setVal=r.zeros[0])
		r.incPC()
	def sec(self):         #DONE
		print('Run SEC')
		r.cFlag(setVal=r.ones[0])
		r.incPC()
	def cli(self):        	#DONE
		print('Run CLI')
		r.iFlag(setVal=r.zeros[0])
		r.incPC()
	def sei(self):          #DONE
		print('Run SEI')
		r.iFlag(setVal=r.ones[0])
		r.incPC()
	def tya(self):              #DONE
		print('Run TYA')
		r.acc = r.regY
		r.incPC()
	def clv(self):          #DONE
		print('Run CLV')
		r.vFlag(setVal=r.zeros[0])
		r.incPC()
	def txa(self):          #DONE
		print('Run TXA')
		r.acc = r.regX
		r.incPC()
	def txs(self):               #DONE
		print('Run TXS')
		r.stackPoint = r.regX
		r.incPC()
	def tax(self):               #DONE
		print('Run TAX')
		r.regX = r.acc
		r.incPC()
	def tsx(self):      #DONE
		print('Run TSX')
		r.regX = r.stackPoint
		r.incPC()
	def dex(self):          #DONE
		print('Run DEX')
		r.regX = ALU.decVal(r.regX)
		r.incPC()
	def nop(self):
		print('Run NOP')
		r.incPC()
	def bit(self):       #DONE
		print('Run BIT')
		data = mem.read()
		r.nFlag(setVal=data[0])
		r.vFlag(setVal=data[1])
		data &= r.acc
		ALU.addVal(self, data, r.zeros, carry = r.zeros[0], flags = True, cFlag=False, zFlag=True, nFlag=False, vFlag=False)
		r.incPC()
	def jmp(self):                  #DONE
		print('Run JMP')
		r.incPC()
		highPart = mem.read()
		r.incPC()
		lowPart = mem.read()
		r.PC = highPart+lowPart
		r.savePC()
	def jmpAbsolute(self):                    #DONE
		print('Run JMP abs')
		r.incPC()
		highPart = mem.read()
		r.incPC()
		lowPart = mem.read()
		r.PC = highPart+lowPart
		r.savePC()
	def sty(self):              #DONE
		print('Run STY')
		mem.write(r.regY)
		r.incPC()
	def ldy(self):              #DONE
		print('Run LDY')
		data = mem.read()
		r.regY = data
		r.incPC()
	def cpy(self):            #DONE
		print('Run CPY')
		data = mem.read()
		ALU.cmpVal(data,regY)
	def cpx(self):            #DONE
		print('Run CPX')
		data = mem.read()
		ALU.cmpVal(data,regX)
	def ora(self):            #DONE
		print('Run ORA')
		data = mem.read()
		r.acc |= data
		ALU.add(r.zeros)
		r.incPC()
	def eor(self):        #DONE
		print('Run EOR')
		data = mem.read()
		r.acc ^= data
		ALU.add(r.zeros)
	def sta(self):        #DONE
		print('Run STA')
		mem.write(r.acc)
		r.incPC()
	def cmp(self):       #DONE
		print('Run CMP')
		data = mem.read()
		ALU.cmpVal(data,r.acc)
	def andInstruct(self):    #DONE
		print('Run AND')
		data = mem.read()
		ALU.andAcc(data)
	def adc(self):   #DONE
		print('Run ADC')
		data = mem.read()
		ALU.add(data)
	def lda(self):          #DONE
		print('Run LDA')
		print('LLDAPC:',r.PC)
		data = mem.read()
		r.acc = data
		print('acc: ',r.acc)
	def sbc(self):              #DONE
		print('Run SBC')
		data = mem.read()
		ALU.sub(data)
		r.incPC()
	def asl(self):     #DONE
		print('Run ASL')
		data = mem.read()
		data = ALU.aslVal(data)
		mem.write(data)
		r.incPC()
	def rol(self):                #DONE
		print('Run ROL')
		data = mem.read()
		data = ALU.rolVal(data)
		mem.write(data)
		r.incPC()
	def lsr(self):                    #DONE
		print('Run LSR')
		data = mem.read()
		data = ALU.lsrVal(data)
		r.incPC()
	def ror(self):           #DONE
		print('Run ROR')
		data = mem.read()
		data = ALU.rorVal(data)
		mem.write(data)
		r.incPC()
	def stx(self):         #DONE
		print('Run STX')
		mem.write(r.regX)
		r.incPC()
	def ldx(self):       #DONE
		print('Run LDX')
		data = mem.read()
		r.regX = data
		r.incPC()
	def dec(self):         #DONE
		print('Run DEC')
		data = mem.read()
		data = ALU.decVal(data)
		mem.write(data)
	def inc(self):          #DONE
		print('Run INC')
		data = mem.read()
		data = ALU.incVal(data)
		mem.write(data)
class _decode:
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
				print('COULDNT FIND ADDRESS MODE, DEFAULTING TO IMPLIED')
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
		print('Instruction: ')
		print(str(hex(ba2int(r.instructReg))))
		print(' ')
		decodedAddressMode, decodedInstruction = self.parse()
		

		return decodedAddressMode, decodedInstruction
	def getAddressMode(self):
		aOPC = self.instruction[6:] + self.instruction[3:6]
		print('OPC',self.instruction[6:],self.instruction[3:6])
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
		
		element = self.addressModeLUT[mid+1]
		print(element[0])
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
		print('FAILED TO FIND INSTRUCTION, ROUNDING UP')
		element = self.LUT[mid]
		if(element[1] == False):
			print('FAILED, IMPLIED ADDRESS MODE')
		if((ba2int(element[0]) - ba2int(self.instruction)) > 8):
			print('FAILED, ROUNDED TOO FAR')

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

	def cycle(self):
		r.restorePC()
		print('acc: ',r.acc, r.PC)
		r.setInstructionReg()
		decodedAddressMode, decodedInstruction = decode.parseInstructionReg()
		decodedAddressMode()
		decodedInstruction()
	def reset(self):
		print('RESETTING')
		r.PC = bitarray('0000 0000 0000 0000',endian='big')
		r.acc = r.zeros
		r.regX = r.zeros
		r.regY = r.zeros
		r.flagReg = bitarray('0010 0000', endian='big')
		r.instructReg = r.zeros
		r.stackPoint = r.zeros
		mem.addIndex = 0
		mem.setAddressFromPC()
		print('PC:',r.PC)
		r.setInstructionReg()
		print('got instruction. PC:',r.PC)
		decodedAddressMode, decodedInstruction = decode.parseInstructionReg()
		decodedAddressMode()
		decodedInstruction()


r = _registers()
mem = _memory()
ALU = _ALU()
e = _execute()
AM = _runAddressModes()
decode = _decode()
cpu = _cycle()


charBuff = []
def pressEvent(callback):
	charBuff.append(callback.name)
def quitProg():
	#print('tryna quit...')
	keyboard.unhook_all()
	os._exit(1)

prog = bitarray('1010 0101 0000 1000 0110 0101 0000 1000 0100 1100 0000 0000 0000 0000 0000 0000 0000 0010',endian='big')
prog1 = bitarray('1010 0101 0000 1000 0110 0101 0000 1000 0111 1100 0000 0000 0000 0010 0000 0000 0000 0001',endian='big')
i=0
while i < len(prog1):
	mem.memoryBlock[i] = prog1[i]
	i+=1
cpu.reset()
print(r.PC)
for i in range(0,10):
	cpu.cycle()

keyboard.on_press(pressEvent)
keyboard.add_hotkey('ctrl+z', quitProg)
