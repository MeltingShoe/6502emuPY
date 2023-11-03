import keyboard
import os
from bitarray import bitarray

charBuff = []
PC = bitarray('0000 0000 0000 0000', endian='big')
stackPoint = bitarray('0011 0011', endian='big')
eA = bitarray('0 0000 0000 0000 0000', endian='big')
acc = bitarray('0000 0000', endian='big')
regX = bitarray('0011 0011', endian='big')
regY = bitarray('0011 0011', endian='big')
flagReg = bitarray('0010 0000', endian='big')
regA = bitarray('1010 1001', endian='big')
regB = bitarray('1100 0011', endian='big')
sumReg = bitarray('0011 0011', endian='big')
ones = bitarray('1111 1111', endian='big')
zeros = bitarray('0000 0000', endian='big')
stepCounter = bitarray('0000', endian='big')
instructReg = bitarray('0000 0000', endian='big')

class registers:
	def __init__(self,PC,stackPoint,eA,acc,regX,regY,flagReg,ones,zeros,stepCounter,instructReg):
		self.PC = PC
		self.stackPoint = stackPoint
		self.eA = eA
		self.acc = acc
		self.regX = regX
		self.regY = regY
		self.flagReg = flagReg
		self.ones = ones
		self.zeros = zeros
		self.stepCounter = stepCounter
		self.instructReg = instructReg

r = registers(PC,stackPoint,eA,acc,regX,regY,flagReg,ones,zeros,stepCounter,instructReg)

zeroPage = bitarray(2048)
stack = bitarray(2048)
vectors = bitarray(48)
rom = bitarray(32768)
ram = bitarray(28624)

prog = bitarray('1010 1010 0000 1111 1100 1010 0000 1111 0000 0000')
i1 = 0
while(i1<40):
	zeroPage[i1] = prog[i1]
	i1+=1

class execute():
	def __init__(self):
		global r
	oraC = bitarray('000', endian='big')
	andC = bitarray('001', endian='big')
	eorC = bitarray('010', endian='big')
	adcC = bitarray('011', endian='big')
	staC = bitarray('100', endian='big')
	ldaC = bitarray('101', endian='big')
	cmpC = bitarray('110', endian='big')
	sbcC = bitarray('111', endian='big')

	aslC = bitarray('000', endian='big')
	rolC = bitarray('001', endian='big')
	lsrC = bitarray('010', endian='big')
	rorC = bitarray('011', endian='big')
	stxC = bitarray('100', endian='big')
	ldxC = bitarray('101', endian='big')
	decC = bitarray('110', endian='big')
	incC = bitarray('111', endian='big')

	#bplC = bitarray('0001 0000', endian='big')
	def bpl():
		pass
	#bmiC = bitarray('0011 0000', endian='big')
	def bmi():
		pass
	#bvcC = bitarray('0101 0000', endian='big')
	def bvc():
		pass
	#bvsC = bitarray('0111 0000', endian='big')
	def bvs():
		pass
	#bccC = bitarray('1001 0000', endian='big')
	def bcc():
		pass
	#bcsC = bitarray('1011 0000', endian='big')
	def bcs():
		pass
	#bneC = bitarray('1101 0000', endian='big')
	def bne():
		pass
	#beqC = bitarray('1111 0000', endian='big')
	def beq():
		pass


	#brkC = bitarray('0000 0000', endian='big')
	def brk():
		pass
	#jsrAbsoluteC = bitarray('0010 0000', endian='big')
	def jsrAbsolute():
		pass
	#rtiC = bitarray('0100 0000', endian='big')
	def rti():
		pass
	#rtsC = bitarray('0110 0000', endian='big')
	def rts():
		pass
	#phpC = bitarray('0000 1000', endian='big')
	def php():
		pass
	#plpC = bitarray('0010 1000', endian='big')
	def plp():
		pass
	#phaC = bitarray('0100 1000', endian='big')
	def pha():
		pass
	#plaC = bitarray('0110 1000', endian='big')
	def pla():
		pass
	#deyC = bitarray('1000 1000', endian='big')
	def dey():
		print('dey')
		r.regY= megaAdder(cIn=r.zeros[7],rA=r.regY, rB=bitarray('0000 0001',endian='big'), overflow=False, carry=False, sub=True)
		print('DEY data: ',r.regX)
		incPC()
		r.stepCounter = bitarray('0000',endian='big')
	#tayC = bitarray('1010 1000', endian='big')
	def tay():
		print('tay')
		r.regY = r.acc
		print('TAY r.regY: ',r.regY)
		incPC()
		r.stepCounter = bitarray('0000',endian='big')
	#inyC = bitarray('1100 1000', endian='big')
	def iny():
		print('iny')
		r.regY= megaAdder(cIn=r.zeros[7],rA=r.regY, rB=bitarray('0000 0001',endian='big'), overflow=False, carry=False)
		print('INY data: ',r.regY)
		incPC()
		r.stepCounter = bitarray('0000',endian='big')
	#inxC = bitarray('1110 1000', endian='big')
	def inx():
		print('inx')
		r.regX= megaAdder(cIn=r.zeros[7],rA=r.regX, rB=bitarray('0000 0001',endian='big'), overflow=False, carry=False)
		print('INX data: ',r.regX)
		incPC()
		r.stepCounter = bitarray('0000',endian='big')
	#clcC = bitarray('0001 1000', endian='big')
	def clc():
		print('clc')
		r.flagReg[7] = r.zeros[7]
		print('CLC flags: ',r.flagReg)
		incPC()
		r.stepCounter = bitarray('0000',endian='big')
	#secC = bitarray('0011 1000', endian='big')
	def sec():
		print('sec')
		r.flagReg[7] = r.ones[7]
		print('SEC flags: ',r.flagReg)
		incPC()
		r.stepCounter = bitarray('0000',endian='big')
	#cliC = bitarray('0101 1000', endian='big')
	def cli():
		print('cli')
		r.flagReg[5] = r.zeros[7]
		print('CLI flags: ',r.flagReg)
		incPC()
		r.stepCounter = bitarray('0000',endian='big')
	#seiC = bitarray('0111 1000', endian='big')
	def sei():
		print('sei')
		r.flagReg[5] = r.ones[7]
		print('SEI flags: ',r.flagReg)
		incPC()
		r.stepCounter = bitarray('0000',endian='big')
	#tyaC = bitarray('1001 1000', endian='big')
	def tya():
		print('tya')
		r.acc = r.regY
		print('TYA r.acc: ',r.acc)
		incPC()
		r.stepCounter = bitarray('0000',endian='big')
	#clvC = bitarray('1011 1000', endian='big')
	def clv():
		print('clv')
		r.flagReg[1] = r.zeros[7]
		print('CLV flags: ',r.flagReg)
		incPC()
		r.stepCounter = bitarray('0000',endian='big')
	#cldC = bitarray('1101 1000', endian='big')
	def cld():
		pass
	#sedC = bitarray('1111 1000', endian='big')
	def sed():
		pass
	#txaC = bitarray('1000 1010', endian='big')
	def txa():
		print('txa')
		r.acc = r.regX
		print('TXA r.acc: ',r.acc)
		incPC()
		r.stepCounter = bitarray('0000',endian='big')
	#txsC = bitarray('1001 1010', endian='big')
	def txs():
		print('txs')
		r.stackPoint = r.regX
		print('TXS stack: ',r.stackPoint)
		incPC()
		r.stepCounter = bitarray('0000',endian='big')
	#taxC = bitarray('1010 1010', endian='big')
	def tax():
		print('tax')
		r.regX = r.acc
		print('TAX r.regX: ',r.regX)
		incPC()
		r.stepCounter = bitarray('0000',endian='big')
	def tsx():
		print('tsx')
		r.regX = r.stackPoint
		print('TSX r.regX: ',r.regX)
		incPC()
		r.stepCounter = bitarray('0000',endian='big')
	def dex():
		print('dex')
		r.regX= megaAdder(cIn=r.zeros[7],rA=r.regX, rB=bitarray('0000 0001',endian='big'), overflow=False, carry=False, sub=True)
		print('DEX data: ',r.regX)
		incPC()
		r.stepCounter = bitarray('0000',endian='big')
	def nop():
		print('nop')
		incPC()
		r.stepCounter = bitarray('0000',endian='big')
	def bit():
		pass
	def jmp():
		pass
	def jmpAbsolute():
		pass
	def sty():
		pass
	def ldy():
		pass
	def cpy():
		pass
	def cpx():
		pass
	def ora():
		pass
	def eor():
		pass
	def sta():
		pass
	def cmp():
		pass
	def andInstruct():
		pass
	def adc():
		pass
	def lda():
		pass
	def sbc():
		pass
	def asl():
		pass
	def rol():
		pass
	def lsr():
		pass
	def ror():
		pass
	def stx():
		pass
	def ldx():
		pass
	def dec():
		pass
	def inc():
		pass
e = execute()

bitC = bitarray('001', endian='big')
jmpC = bitarray('010', endian='big')
jmpAbsoluteC = bitarray('011', endian='big')
styC = bitarray('100', endian='big')
ldyC = bitarray('101', endian='big')
cpyC = bitarray('110', endian='big')
cpxC = bitarray('111', endian='big')

g1c = bitarray('01', endian='big')
g2c = bitarray('10', endian='big')
g3c = bitarray('00', endian='big')

zeroPageXC = bitarray('000', endian='big')
directZeroPageXC = bitarray('101', endian='big')
absoluteXC = bitarray('111', endian='big')

def addEight(count, cIn=0):
	count, carryOut = megaAdder(cIn=0, carry=False, zero=False, neg=False, overflow = False, rA = count, rB = bitarray('0000 1000',endian='big'))
	return count
def inc4bits(count):
	if(count[3]==r.ones[3]):
		count[3]=r.zeros[3]
		if(count[2]==r.ones[2]):
			count[2]=r.zeros[2]
			if(count[1]==r.ones[1]):
				count[1]=r.zeros[1]
				if(count[0]==r.ones[0]):
					count[0]=r.zeros[0]
					return True, count
				else:
					count[0]=r.ones[0]
			else:	
				count[1]=r.ones[1]
		else:
			count[2]=r.ones[2]
	else:	
		count[3]=r.ones[3]
	return False, count
def incStep(count):
	f, count = inc4bits(count)
	return count
def inc8bits(count):
	aaa = bitarray('0000',endian='big')
	bbb = bitarray('0000',endian='big')
	ooo = bitarray('0000 0000',endian='big')
	aaa = r.PC[:4]
	bbb = r.PC[4:]
	carryOut, bbb = inc4bits(bbb)
	if(carryOut):
		carryOut, aaa = inc4bits(ccc)
	ooo[0]=aaa[0]
	ooo[1]=aaa[1]
	ooo[2]=aaa[2]
	ooo[3]=aaa[3]
	ooo[4]=bbb[0]
	ooo[5]=bbb[1]
	ooo[6]=bbb[2]
	ooo[7]=bbb[3]
	return ooo
def incPC():
	global r
	aaa = bitarray('0000',endian='big')
	bbb = bitarray('0000',endian='big')
	ccc = bitarray('0000',endian='big')
	ddd = bitarray('0000',endian='big')
	aaa = r.PC[:4]
	bbb = r.PC[4:8]
	ccc = r.PC[8:12]
	ddd = r.PC[12:16]
	carryOut, ddd = inc4bits(ddd)
	if(carryOut):
		carryOut, ccc = inc4bits(ccc)
	if(carryOut):
		carryOut, bbb = inc4bits(bbb)
	if(carryOut):
		carryOut, aaa = inc4bits(aaa)
	if(carryOut):
		carryOut, ddd = inc4bits(ddd)
	if(carryOut):
		carryOut, ccc = inc4bits(ccc)
	if(carryOut):
		carryOut, bbb = inc4bits(bbb)
	if(carryOut):
		carryOut, aaa = inc4bits(aaa)
	r.PC[0]=aaa[0]
	r.PC[1]=aaa[1]
	r.PC[2]=aaa[2]
	r.PC[3]=aaa[3]
	r.PC[4]=bbb[0]
	r.PC[5]=bbb[1]
	r.PC[6]=bbb[2]
	r.PC[7]=bbb[3]
	r.PC[8]=ccc[0]
	r.PC[9]=ccc[1]
	r.PC[10]=ccc[2]
	r.PC[11]=ccc[3]
	r.PC[12]=ddd[0]
	r.PC[13]=ddd[1]
	r.PC[14]=ddd[2]
	r.PC[15]=ddd[3]

	r.eA[1:] = r.PC

	r.eA[1] = r.eA[4]
	r.eA[2] = r.eA[5]
	r.eA[3] = r.eA[6]
	r.eA[4] = r.eA[7]
	r.eA[5] = r.eA[8]
	r.eA[6] = r.eA[9]
	r.eA[7] = r.eA[10]
	r.eA[8] = r.eA[11]
	r.eA[9] = r.eA[12]
	r.eA[10] = r.eA[13]
	r.eA[11] = r.eA[14]
	r.eA[12] = r.eA[15]
	r.eA[13] = r.eA[16]
	r.eA[14] = r.zeros[0]
	r.eA[15] = r.zeros[0]
	r.eA[16] = r.zeros[0]

	print('PC: ',r.PC)
def memMap(write=False, data=r.zeros):
	if(r.eA[0] == r.ones[0] and write==False):
		return r.acc
	elif(r.eA[0] == r.ones[0] and write==True):
		r.acc = data
	mapLen = 0
	eAddy = r.eA[1:17]
	print('memmap eA: ',r.eA)
	address = eAddy.tobytes()
	address = int.from_bytes(address, "big")
	print('addy: ',address)
	addressStart = address
	print('aStart: ',addressStart)
	endAddress = address + 8
	print('endAddress: ', endAddress)
	if(address<2048):
		if(write != True):	
			data = zeroPage[addressStart:endAddress]
			print('0 page data: ',data)
			return data
		zeroPage[addressStart:endAddress] = data
		print('write 0 page: ',zeroPage[addressStart:endAddress],data)
		return data
	mapLen+=2048
	if(address>=mapLen and address < (mapLen+2048)):
		if(write != True):	
			data = stack[(addressStart-mapLen):(endAddress-mapLen)]
			print('stack data: ', data)
			return data
		stack[(addressStart-mapLen):(endAddress-mapLen)] = data
		print('write stack: ',stack[(addressStart-mapLen):(endAddress-mapLen)])
		return data
	mapLen+=2048
	if(address>=mapLen and address < (mapLen+28624)):
		if(write != True):	
			data = ram[(addressStart-mapLen):(endAddress-mapLen)]
			print('ram data: ', data)
			return data
		ram[(addressStart-mapLen):(endAddress-mapLen)] = data
		print('write ram: ',ram[(addressStart-mapLen):(endAddress-mapLen)])
		return data
	mapLen+=28624
	if(address>=mapLen and address < (mapLen+48)):
		if(write != True):	
			data = vectors[(addressStart-mapLen):(endAddress-mapLen)]
			print('vectors data: ', data)
			return data
		vectors[(addressStart-mapLen):(endAddress-mapLen)] = data
		print('write vectors: ',vectors[(addressStart-mapLen):(endAddress-mapLen)])
		return data
	mapLen+=48
	if(address>=mapLen and address < (mapLen+32768)):
		if(write != True):	
			data = rom[(addressStart-mapLen):(endAddress-mapLen)]
			print('rom data: ', data)
			return data
		rom[(addressStart-mapLen):(endAddress-mapLen)] = data
		print('write rom: ',rom[(addressStart-mapLen):(endAddress-mapLen)])
		return data
	mapLen+=32768
	if(address>=mapLen):
		print('out of range')
def fullAdder(a,b,cIn):
	hXor = a^b
	hOut = a&b
	s = hXor^cIn
	fOut = hXor&cIn
	cOut = fOut | hOut
	return s,cOut	
def megaAdder(cIn=0, carry=True, zero=True, neg=True, overflow = True, rA = r.acc, rB = regB, sub = False):
	x = r.zeros[0]
	y=True
	if sub:
		cIn = cIn^r.ones[0]
		rB = rB^r.ones
		print("ra: ",rA,cIn)
	if((rA[0]^rB[0])^r.ones[0]):
		print('set x',rA[0])
		x = rA[0]
		y = True

	s, cIn = fullAdder(rA[7],rB[7],cIn)
	print(cIn)
	s1, cIn = fullAdder(rA[6],rB[6],cIn)
	print(cIn)
	s2, cIn = fullAdder(rA[5],rB[5],cIn)
	print(cIn)
	s3, cIn = fullAdder(rA[4],rB[4],cIn)
	print(cIn)
	s4, cIn = fullAdder(rA[3],rB[3],cIn)
	print(cIn)
	s5, cIn = fullAdder(rA[2],rB[2],cIn)
	print(cIn)
	s6, cIn = fullAdder(rA[1],rB[1],cIn)
	print(cIn)
	s7, cOut = fullAdder(rA[0],rB[0],cIn)
	print(cOut)
	if(overflow):
		if(s7 != x and y):
			r.flagReg[1] = r.ones[1]
		else:
			r.flagReg[1] = r.zeros[1]
	sumReg[0] = s7
	sumReg[1] = s6
	sumReg[2] = s5
	sumReg[3] = s4
	sumReg[4] = s3
	sumReg[5] = s2
	sumReg[6] = s1
	sumReg[7] = s
	if(carry):
		r.flagReg[7] = cOut
	if(s7):
		r.flagReg[0] = s7
	zF = (s|s1|s2|s3|s4|s5|s6|s7) ^ r.ones[1]
	print('zF: ',(zF))
	r.flagReg[6] = (zF)
	return sumReg, cOut
def fetch():
	global r
	print('fetchdatshi')
	print(r.eA,'\n')
	data = memMap()
	r.instructReg = data

def decode():
	# Set the address mode bits in LUT to 0 . Then do a binary search on the input instruction. If no matching instruction is found, round down.
	LUT = [ ( bitarray('1110 1010', endian='big') , e.nop ) , ( bitarray('1110 1010', endian='big') , e.dex ),
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
			( bitarray('001x xx01', endian='big') , e.andInstruct ) , ( bitarray('000x xx01', endian='big') , e.ora ) ]


#Sorting input array, by hand :(
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

			#this array is reordered from AAAB BBCC to CCAA ABBB
			#AAA = OPCode
			#BBB = Address mode
			#CC = Group
			#Group 3 has many instructions that use BBB as part of the instruction code
			#This array is not the real opcodes, incoming instructions are reordered to this
''' [ ( bitarray('1011 1010', endian='big') , e.nop ) , ( bitarray('1011 1010', endian='big') , e.dex ),
			( bitarray('1010 1110', endian='big') , e.tsx ) , ( bitarray('1011 1010', endian='big') , e.tax ),
			( bitarray('1010 0110', endian='big') , e.txs ) , ( bitarray('1010 0010', endian='big') , e.txa ),
			( bitarray('0010 1110', endian='big') , e.clv ) , ( bitarray('0010 0110', endian='big') , e.tya ),

			( bitarray('0001 1110', endian='big') , e.sei ) , ( bitarray('0001 0110', endian='big') , e.cli ),
			( bitarray('0000 1110', endian='big') , e.sec ) , ( bitarray('0000 0110', endian='big') , e.clc ),
			( bitarray('0011 1010', endian='big') , e.inx ) , ( bitarray('0011 0010', endian='big') , e.iny ),
			( bitarray('0010 1010', endian='big') , e.tay ) , ( bitarray('0010 0010', endian='big') , e.dey ),

			( bitarray('0001 1010', endian='big') , e.pla )         , ( bitarray('0001 0010', endian='big') , e.pha ),
			( bitarray('0000 1010', endian='big') , e.plp )         , ( bitarray('0000 0010', endian='big') , e.php ),
			( bitarray('0001 1000', endian='big') , e.rts )         , ( bitarray('0001 0000', endian='big') , e.rti ),
			( bitarray('0000 1000', endian='big') , e.jsrAbsolute ) , ( bitarray('0000 0000', endian='big') , e.brk ),

			( bitarray('0011 1100', endian='big') , e.beq ) , ( bitarray('0011 0100', endian='big') , e.bne ),
			( bitarray('0010 1100', endian='big') , e.bcs ) , ( bitarray('0010 0100', endian='big') , e.bcc ),
			( bitarray('0001 1100', endian='big') , e.bvs ) , ( bitarray('0001 0100', endian='big') , e.bvc ),
			( bitarray('0000 1100', endian='big') , e.bmi ) , ( bitarray('0000 0100', endian='big') , e.bpl ),

			( bitarray('0011 1xxx', endian='big') , e.cpx )         , ( bitarray('0011 0xxx', endian='big') , e.cpy ), 
			( bitarray('0010 1xxx', endian='big') , e.ldy )         , ( bitarray('0010 0xxx', endian='big') , e.sty ), 
			( bitarray('0001 1xxx', endian='big') , e.jmpAbsolute ) , ( bitarray('0001 0xxx', endian='big') , e.jmp ),
			( bitarray('0000 1xxx', endian='big') , e.bit ),

			( bitarray('1011 1xxx', endian='big') , e.inc ) , ( bitarray('1011 0xxx', endian='big') , e.dec ),
			( bitarray('1010 1xxx', endian='big') , e.ldx ) , ( bitarray('1010 0xxx', endian='big') , e.stx ),
			( bitarray('1001 1xxx', endian='big') , e.ror ) , ( bitarray('1001 0xxx', endian='big') , e.lsr ),
			( bitarray('1000 1xxx', endian='big') , e.rol ) , ( bitarray('1000 0xxx', endian='big') , e.asl ),

			( bitarray('0111 1xxx', endian='big') , e.sbc )         , ( bitarray('0111 0xxx', endian='big') , e.cmp ),
			( bitarray('0110 1xxx', endian='big') , e.lda )         , ( bitarray('0110 0xxx', endian='big') , e.sta ),
			( bitarray('0101 1xxx', endian='big') , e.adc )         , ( bitarray('0101 0xxx', endian='big') , e.eor ),
			( bitarray('0100 1xxx', endian='big') , e.andInstruct ) , ( bitarray('0100 0xxx', endian='big') , e.ora ) ]
			'''
	# This array is the previous array but sorted
'''
		[( bitarray('0000 0000', endian='big') , e.brk ),( bitarray('0000 0010', endian='big') , e.php ),
		( bitarray('0000 0100', endian='big') , e.bpl ),( bitarray('0000 0110', endian='big') , e.clc ),
		( bitarray('0000 1000', endian='big') , e.jsrAbsolute ),( bitarray('0000 1010', endian='big') , e.plp ), 
		( bitarray('0000 1100', endian='big') , e.bmi ),( bitarray('0000 1110', endian='big') , e.sec ),
		( bitarray('0000 1xxx', endian='big') , e.bit ),

		( bitarray('0001 0000', endian='big') , e.rti ),( bitarray('0001 0010', endian='big') , e.pha ),
		( bitarray('0001 0100', endian='big') , e.bvc ),( bitarray('0001 0110', endian='big') , e.cli ),
		( bitarray('0001 0xxx', endian='big') , e.jmp ),( bitarray('0001 1000', endian='big') , e.rts ), 
		( bitarray('0001 1010', endian='big') , e.pla ),( bitarray('0001 1100', endian='big') , e.bvs ),
		( bitarray('0001 1110', endian='big') , e.sei ),( bitarray('0001 1xxx', endian='big') , e.jmpAbsolute ),

		( bitarray('0010 0010', endian='big') , e.dey ),( bitarray('0010 0100', endian='big') , e.bcc ),
		( bitarray('0010 0110', endian='big') , e.tya ),( bitarray('0010 0xxx', endian='big') , e.sty ),
		( bitarray('0010 1010', endian='big') , e.tay ),( bitarray('0010 1100', endian='big') , e.bcs ) ,
		( bitarray('0010 1110', endian='big') , e.clv ),( bitarray('0010 1xxx', endian='big') , e.ldy ) ,
		 
		( bitarray('0011 0010', endian='big') , e.iny ),( bitarray('0011 0100', endian='big') , e.bne ),
		( bitarray('0011 0xxx', endian='big') , e.cpy ),( bitarray('0011 1010', endian='big') , e.inx ) ,
		( bitarray('0011 1100', endian='big') , e.beq ),( bitarray('0011 1xxx', endian='big') , e.cpx ) ,

		( bitarray('0100 0xxx', endian='big') , e.ora ),( bitarray('0101 0xxx', endian='big') , e.eor ),
		( bitarray('0110 0xxx', endian='big') , e.sta ),( bitarray('0111 0xxx', endian='big') , e.cmp ),
		( bitarray('0100 1xxx', endian='big') , e.andInstruct ),( bitarray('0101 1xxx', endian='big') , e.adc ),
		( bitarray('0110 1xxx', endian='big') , e.lda ),( bitarray('0111 1xxx', endian='big') , e.sbc ),

		( bitarray('1000 0xxx', endian='big') , e.asl ),( bitarray('1000 1xxx', endian='big') , e.rol ) ,
		( bitarray('1001 0xxx', endian='big') , e.lsr ),( bitarray('1001 1xxx', endian='big') , e.ror ) ,
		( bitarray('1010 0010', endian='big') , e.txa ),( bitarray('1010 0110', endian='big') , e.txs ) ,
		( bitarray('1010 0xxx', endian='big') , e.stx ),( bitarray('1010 1110', endian='big') , e.tsx ) ,
		( bitarray('1010 1xxx', endian='big') , e.ldx ) ,
		( bitarray('1010 1010', endian='big') , e.tax ),( bitarray('1011 0010', endian='big') , e.dex ),
		( bitarray('1011 0xxx', endian='big') , e.dec ),( bitarray('1011 1xxx', endian='big') , e.inc ),


		( bitarray('1110 1010', endian='big') , e.nop )]
'''
	# This is the previous array but with x's swapped with 1's. We can just search and round up
'''[( bitarray('0000 0000', endian='big') , e.brk ),( bitarray('0000 0010', endian='big') , e.php ),
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
		'''


def search(instruction):
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
	print("KKKKKKKKKKKKKK",k)

	low = 0
	high = len(LUT)-1
	mid = (high+low)//2
	while(low<=high):
		key = LUT[mid]
		key = key[0]
		print('hopehope',LUT[mid])
		if(k == key):
			
			return(LUT[mid])
		if(k < key):
			print(k,' IS LESS THAN ',key)
			high = mid - 1
			mid = ( high + low ) // 2
		if(k > key):
			print(k, ' IS MORE THAN ', key)
			low = mid + 1
			mid = ( high + low ) // 2
	key = LUT[mid+1]
	key = key[0]
	print('no find', key)
	return(key)

def parseOPC():
	global r
	data = bitarray('0000 0000',endian='big')
	eight = bitarray('0000 1000',endian='big')
	if(r.stepCounter == bitarray('0000',endian='big')):
		print('fetchdatshi')
		print(r.eA,'\n')
		data = memMap()
		r.instructReg = data
		print('Step: ',r.stepCounter,'\n')
		discard, r.stepCounter = inc4bits(r.stepCounter)
		print('Step: ',r.stepCounter,'\n')
	if(r.stepCounter == bitarray('0001',endian='big')):
		print('in step 2')
		instr = bitarray('0000 0000',endian='big')
		instr = r.instructReg
		opc = bitarray('000',endian='big')
		grp = bitarray('00',endian='big')
		addrMode = bitarray('000',endian='big')
		opc = instr[:3]
		addrMode = instr[3:6]
		grp = instr[6:]
		print(opc,grp,addrMode)
		print('Step: ',r.stepCounter,'\n')
		discard, r.stepCounter = inc4bits(r.stepCounter)
		print('Step: ',r.stepCounter,'\n')
	opc1 = bitarray('0000 0000',endian='big')
	opc1[0:3] = opc
	opc1[3:6] = addrMode
	opc1[6:8] = grp

	if(addrMode==bitarray('010', endian='big')):
		print('using immediate addr')
		incPC()
		print('pc',r.PC)
		print('eA',r.eA)
	elif(addrMode==bitarray('100', endian='big')):
		print('using 0page + Y addr')
		incPC()
		print('eA: ',r.eA)
		data = memMap()
		r.eA[:9] = bitarray('0000 0000 0',endian='big')
		data, carryOut = megaAdder(cIn=0,zero=False,carry=False,overflow=False,neg=False,rA=data, rB=r.regY)
		r.eA[9:] = data
	elif(addrMode==bitarray('110', endian='big')):
		print('using absolute + Y addr')
		incPC()
		print('eA: ',r.eA)
		temp = memMap()
		incPC()
		print('eA: ',r.eA)
		data = memMap()
		r.PC[0:8] = temp
		r.PC[8:16] = data
		r.PC, carryOut = megaAdder(cIn=0,zero=False,carry=False,overflow=False,neg=False,rA=r.PC[8:16], rB=r.regY)
		r.PC, carryOut = megaAdder(cIn=carryOut,zero=False,carry=False,overflow=False,neg=False,rA=r.PC[0:8], rB=r.zeros)
		r.eA = r.PC

		r.eA[1] = r.eA[4]
		r.eA[2] = r.eA[5]
		r.eA[3] = r.eA[6]
		r.eA[4] = r.eA[7]
		r.eA[5] = r.eA[8]
		r.eA[6] = r.eA[9]
		r.eA[7] = r.eA[10]
		r.eA[8] = r.eA[11]
		r.eA[9] = r.eA[12]
		r.eA[10] = r.eA[13]
		r.eA[11] = r.eA[14]
		r.eA[12] = r.eA[15]
		r.eA[13] = r.eA[16]
		r.eA[14] = r.zeros[0]
		r.eA[15] = r.zeros[0]
		r.eA[16] = r.zeros[0]
		print('pc, ea ',r.PC,r.eA)
	elif(addrMode==bitarray('000', endian='big')):
		print('using 0page + X addr')
		incPC()
		print('r.eA: ',r.eA)
		data = memMap()
		r.eA[:9] = bitarray('0000 0000 0',endian='big')
		data, carryOut = megaAdder(cIn=0,zero=False,carry=False,overflow=False,neg=False,rA=data, rB=r.regX)
		r.eA[9:] = data
	elif(addrMode==bitarray('111', endian='big')):
		print('using absolute + X addr')
		incPC()
		print('r.eA: ',r.eA)
		temp = memMap()
		incPC()
		print('r.eA: ',r.eA)
		data = memMap()
		r.PC[0:8] = temp
		r.PC[8:16] = data
		r.PC, carryOut = megaAdder(cIn=0,zero=False,carry=False,overflow=False,neg=False,rA=r.PC[8:16], rB=r.regX)
		r.PC, carryOut = megaAdder(cIn=carryOut,zero=False,carry=False,overflow=False,neg=False,rA=r.PC[0:8], rB=r.zeros)
		r.eA = r.PC

		r.eA[1] = r.eA[4]
		r.eA[2] = r.eA[5]
		r.eA[3] = r.eA[6]
		r.eA[4] = r.eA[7]
		r.eA[5] = r.eA[8]
		r.eA[6] = r.eA[9]
		r.eA[7] = r.eA[10]
		r.eA[8] = r.eA[11]
		r.eA[9] = r.eA[12]
		r.eA[10] = r.eA[13]
		r.eA[11] = r.eA[14]
		r.eA[12] = r.eA[15]
		r.eA[13] = r.eA[16]
		r.eA[14] = r.zeros[0]
		r.eA[15] = r.zeros[0]
		r.eA[16] = r.zeros[0]
		print('pc, ea ',r.PC,r.eA)
	elif(addrMode==bitarray('001', endian='big')):
		print('using 0page addr')
		incPC()
		print('r.eA: ',r.eA)
		data = memMap()
		r.eA[:9] = bitarray('0000 0000 0',endian='big')
		r.eA[9:17] = data
		print('pc',r.PC)
		print('ea',r.eA)
	elif(addrMode==bitarray('010', endian='big')):
		print('using acc addr')
		incPC()
		r.eA[0] = r.ones[0]
		print('pc, ea ',r.PC,r.eA)
	elif(addrMode==bitarray('011', endian='big')):
		print('using absolute addr')
		incPC()
		print('r.eA: ',r.eA)
		temp = memMap()
		incPC()
		print('r.eA: ',r.eA)
		data = memMap()
		r.PC[0:8] = temp
		r.PC[8:16] = data
		r.eA = r.PC

		r.eA[1] = r.eA[4]
		r.eA[2] = r.eA[5]
		r.eA[3] = r.eA[6]
		r.eA[4] = r.eA[7]
		r.eA[5] = r.eA[8]
		r.eA[6] = r.eA[9]
		r.eA[7] = r.eA[10]
		r.eA[8] = r.eA[11]
		r.eA[9] = r.eA[12]
		r.eA[10] = r.eA[13]
		r.eA[11] = r.eA[14]
		r.eA[12] = r.eA[15]
		r.eA[13] = r.eA[16]
		r.eA[14] = r.zeros[0]
		r.eA[15] = r.zeros[0]
		r.eA[16] = r.zeros[0]
		print('pc, ea ',r.PC,r.eA)


	LUT = [ ( bitarray('1110 1010', endian='big') , e.nop ) , ( bitarray('1110 1010', endian='big') , e.dex ),
			( bitarray('1011 1010', endian='big') , e.tsx ) , ( bitarray('1110 1010', endian='big') , e.tax ),
			( bitarray('1001 1010', endian='big') , e.txs ) , ( bitarray('1000 1010', endian='big') , e.txa ),
			( bitarray('1011 1000', endian='big') , e.clv ) , ( bitarray('1001 1000', endian='big') , e.tya ),

			( bitarray('0111 1000', endian='big') , e.sei ) , ( bitarray('0101 1000', endian='big') , e.cli ),
			( bitarray('0011 1000', endian='big') , e.sec ) , ( bitarray('0001 1000', endian='big') , e.clc ),
			( bitarray('1110 1000', endian='big') , e.inx ) , ( bitarray('1100 1000', endian='big') , e.iny ),
			( bitarray('1010 1000', endian='big') , e.tay ) , ( bitarray('1000 1000', endian='big') , e.dey ),

			( bitarray('0110 1000', endian='big') , e.pla ) , ( bitarray('0100 1000', endian='big') , e.pha ),
			( bitarray('0010 1000', endian='big') , e.plp ) , ( bitarray('0000 1000', endian='big') , e.php ),
			( bitarray('0110 0000', endian='big') , e.rts ) , ( bitarray('0100 0000', endian='big') , e.rti ),
			( bitarray('0010 0000', endian='big') , e.jsrAbsolute ) , ( bitarray('0000 0000', endian='big') , e.brk ),

			( bitarray('1111 0000', endian='big') , e.beq ) , ( bitarray('1101 0000', endian='big') , e.bne ),
			( bitarray('1011 0000', endian='big') , e.bcs ) , ( bitarray('1001 0000', endian='big') , e.bcc ),
			( bitarray('0111 0000', endian='big') , e.bvs ) , ( bitarray('0101 0000', endian='big') , e.bvc ),
			( bitarray('0011 0000', endian='big') , e.bmi ) , ( bitarray('0001 0000', endian='big') , e.bpl ),

			( bitarray('111x xx00', endian='big') , e.cpx ) ,         ( bitarray('110x xx00', endian='big') , e.cpy ), 
			( bitarray('101x xx00', endian='big') , e.ldy ) ,         ( bitarray('100x xx00', endian='big') , e.sty ), 
			( bitarray('011x xx00', endian='big') , e.jmpAbsolute ) , ( bitarray('010x xx00', endian='big') , e.jmp ),
			( bitarray('001x xx00', endian='big') , e.bit ),

			( bitarray('111x xx10', endian='big') , e.inc ) , ( bitarray('110x xx10', endian='big') , e.dec ),
			( bitarray('101x xx10', endian='big') , e.ldx ) , ( bitarray('100x xx10', endian='big') , e.stx ),
			( bitarray('011x xx10', endian='big') , e.ror ) , ( bitarray('010x xx10', endian='big') , e.lsr ),
			( bitarray('001x xx10', endian='big') , e.rol ) , ( bitarray('000x xx10', endian='big') , e.asl ),

			( bitarray('111x xx01', endian='big') , e.sbc ) , ( bitarray('110x xx01', endian='big') , e.cmp ),
			( bitarray('101x xx01', endian='big') , e.lda ) , ( bitarray('100x xx01', endian='big') , e.sta ),
			( bitarray('011x xx01', endian='big') , e.adc ) , ( bitarray('010x xx01', endian='big') , e.eor ),
			( bitarray('001x xx01', endian='big') , e.andInstruct ) , ( bitarray('000x xx01', endian='big') , e.ora ) ]



	# tried to use match. it did not work
	'''if(grp == g1c):
		print('g1')
		if(opc==oraC):
			print('ora')
			print('effective address: ',r.eA)
			data = memMap()
			print('acc, data',r.acc,data)
			r.acc = r.acc | data
			print('ORA r.acc: ',r.acc)
			megaAdder(carry=False,overflow=False,rB=r.zeros)
			incPC()
			r.stepCounter = bitarray('0000',endian='big')
		elif(opc==andC):
			print('and')
			print('effective address: ',r.eA)
			data = memMap()
			print('r.acc, data',r.acc,data)
			r.acc = r.acc & data
			print('AND r.acc: ',r.acc)
			megaAdder(carry=False,overflow=False,rB=r.zeros)
			incPC()
			r.stepCounter = bitarray('0000',endian='big')
		elif(opc==eorC):
			print('eor')
			print('effective address: ',r.eA)
			data = memMap()
			print('r.acc, data',r.acc,data)
			r.acc = r.acc ^ data
			print('EOR r.acc: ',r.acc)
			megaAdder(carry=False,overflow=False,rB=r.zeros)
			incPC()
			r.stepCounter = bitarray('0000',endian='big')
		elif(opc==adcC):
			print('adc')
			print('effective address: ',r.eA)
			data = memMap()
			print('r.acc, data',r.acc,data)
			r.acc, carryOut = megaAdder(cIn=r.flagReg[7],rA=r.acc, rB=data)
			print('ADC r.acc: ',r.acc)
			incPC()
			r.stepCounter = bitarray('0000',endian='big')
		elif(opc==staC):
			print('staC')
			print('effective address: ',r.eA)
			memMap(write=True,data=r.acc)
			print('STA DONE')
			incPC()
			r.stepCounter = bitarray('0000',endian='big')
		elif(opc==ldaC):
			print('lda')
			print('effective address: ',r.eA)
			data = memMap()
			r.acc = data
			print('LDA r.acc: ',r.acc)
			incPC()
			r.stepCounter = bitarray('0000',endian='big')
		elif(opc==cmpC):
			print('cmp')
			print('effective address: ',r.eA)
			data = memMap()
			print('r.acc, data',r.acc,data)
			r.flagReg[7]=r.zeros[7]
			megaAdder(cIn=r.flagReg[7],rA=r.acc, rB=data, overflow=False, sub=True)
			print('CMP flags: ',r.flagReg)
			incPC()
			r.stepCounter = bitarray('0000',endian='big')
		elif(opc==sbcC):
			print('sbc')
			print('effective address: ',r.eA)
			data = memMap()
			print('r.acc, data',r.acc,data)
			r.acc, carryOut = megaAdder(cIn=r.flagReg[7],rA=r.acc, rB=data, sub=True)
			print('SBC r.acc: ',r.acc)
			incPC()
			r.stepCounter = bitarray('0000',endian='big')
		else:
			print('invalid opcode')
		r.stepCounter = bitarray('0000',endian='big')
	elif(grp == g2c):
		print('g2')
		if(opc==aslC):
			print('asl')
			print('effective address: ',r.eA)
			data = memMap()
			print('data',data)
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
			print('ASL data: ',data)
			incPC()
			r.stepCounter = bitarray('0000',endian='big')
		elif(opc==rolC):
			print('rol')
			print('effective address: ',r.eA)
			data = memMap()
			print('data',data)
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
			print('ROL data: ',data)
			incPC()
			r.stepCounter = bitarray('0000',endian='big')
		elif(opc==lsrC):
			print('lsr')
			print('effective address: ',r.eA)
			data = memMap()
			print('data',data)
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
			print('LSR data: ',data)
			incPC()
			r.stepCounter = bitarray('0000',endian='big')
		elif(opc==rorC):
			print('ror')
			print('effective address: ',r.eA)
			data = memMap()
			print('data',data)
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
			print('ROR data: ',data)
			incPC()
			r.stepCounter = bitarray('0000',endian='big')
		elif(opc==stxC):
			print('staC')
			print('effective address: ',r.eA)
			memMap(write=True,data=r.regX)
			print('STX DONE')
			incPC()
			r.stepCounter = bitarray('0000',endian='big')
		elif(opc==ldxC):
			print('ldx')
			print('effective address: ',r.eA)
			data = memMap()
			r.regX = data
			print('LDX r.acc: ',r.acc)
			incPC()
			r.stepCounter = bitarray('0000',endian='big')
		elif(opc==decC):
			print('dec')
			print('effective address: ',r.eA)
			data = memMap()
			print('data',data)
			megaAdder(cIn=r.zeros[7],rA=data, rB=bitarray('0000 0001',endian='big'), overflow=False, carry=False, sub=True)
			print('DEC data: ',data)
			incPC()
			r.stepCounter = bitarray('0000',endian='big')
		elif(opc==incC):
			print('inc')
			print('effective address: ',r.eA)
			data = memMap()
			print('data',data)
			megaAdder(cIn=r.zeros[7],rA=data, rB=bitarray('0000 0001',endian='big'), overflow=False, carry=False, sub=True)
			print('DEC data: ',data)
			incPC()
			r.stepCounter = bitarray('0000',endian='big')
		else:
			print('invalid opcode')
		r.stepCounter = bitarray('0000',endian='big')

	elif(grp == g3c):
		print('g3')
		if(opc==bitC):
			print('bit')
			print('effective address: ',r.eA)
			data = memMap()
			print('r.acc, data',r.acc,data)
		elif(opc==jmpC):
			pass
		elif(opc==jmpAbsoluteC):
			pass
		elif(opc==styC):
			pass
		elif(opc==ldyC):
			pass
		elif(opc==cpyC):
			print('cpy')
			print('effective address: ',r.eA)
			data = memMap()
			print('y, data',r.regY,data)
			r.flagReg[7]=r.zeros[7]
			megaAdder(cIn=r.flagReg[7],rA=r.regY, rB=data, overflow=False, sub=True)
			print('CPX flags: ',r.flagReg)
			incPC()
			r.stepCounter = bitarray('0000',endian='big')
		elif(opc==cpxC):
			print('cpx')
			print('effective address: ',r.eA)
			data = memMap()
			print('x, data',r.regX,data)
			r.flagReg[7]=r.zeros[7]
			megaAdder(cIn=r.flagReg[7],rA=r.regX, rB=data, overflow=False, sub=True)
			print('CPX flags: ',r.flagReg)
			incPC()
			r.stepCounter = bitarray('0000',endian='big')
		r.stepCounter = bitarray('0000',endian='big')

	elif(opc1==bitarray('0001 0000', endian='big')):
		e.bpl()
	elif(opc1==bitarray('0011 0000', endian='big')):
		e.bmi()
	elif(opc1==bitarray('0101 0000', endian='big')):
		e.bvc()
	elif(opc1==bitarray('0111 0000', endian='big')):
		e.bvs()
	elif(opc1==bitarray('1001 0000', endian='big')):
		e.bcc()
	elif(opc1==bitarray('1011 0000', endian='big')):
		e.bcs()
	elif(opc1==bitarray('1101 0000', endian='big')):
		e.bne()
	elif(opc1==bitarray('1111 0000', endian='big')):
		e.beq()
	elif(opc1==bitarray('0000 0000', endian='big')):
		e.brk()
	elif(opc1==bitarray('0010 0000', endian='big')):
		e.jsrAbsolute()
	elif(opc1==bitarray('0100 0000', endian='big')):
		e.rti()
	elif(opc1==bitarray('0110 0000', endian='big')):
		e.rts()
	elif(opc1==bitarray('0000 1000', endian='big')):
		e.php()
	elif(opc1==bitarray('0010 1000', endian='big')):
		e.plp()
	elif(opc1==bitarray('0100 1000', endian='big')):
		e.phaC()
	elif(opc1==bitarray('0110 1000', endian='big')):
		e.pla()
	elif(opc1==bitarray('1000 1000', endian='big')):
		e.dey()
	elif(opc1==bitarray('1010 1000', endian='big')):
		e.tay()
	elif(opc1==bitarray('1100 1000', endian='big')):
		e.iny()
	elif(opc1==bitarray('1110 1000', endian='big')):
		e.inx()
	elif(opc1==bitarray('0001 1000', endian='big')):
		e.clc()
	elif(opc1==bitarray('0011 1000', endian='big')):
		e.sec()
	elif(opc1==bitarray('0101 1000', endian='big')):
		e.cli()
	elif(opc1==bitarray('0111 1000', endian='big')):
		e.sei()
	elif(opc1==bitarray('1001 1000', endian='big')):
		e.tya()
	elif(opc1==bitarray('1011 1000', endian='big')):
		e.clv()
	elif(opc1==bitarray('1000 1010', endian='big')):   #no CLD/SED cuz no decimal mode
		e.txa()
	elif(opc1==bitarray('1001 1010', endian='big')):
		e.txs()
	elif(opc1==bitarray('1010 1010', endian='big')):
		e.tax()
	elif(opc1==bitarray('1011 1010', endian='big')):
		e.tsx()
	elif(opc1==bitarray('1100 1010', endian='big')):
		e.dex()
	elif(opc1==bitarray('1110 1010', endian='big')):
		e.nop()
'''


def pressEvent(callback):
	charBuff.append(callback.name)
def quitProg():
	print('tryna quit...')
	keyboard.unhook_all()
	os._exit(1)
ins1 = bitarray('00 111100', endian='big')
foundins = search(ins1)
print('DIS DA INSTRUCTION',foundins)
print('ACC: ',r.acc)
print('Step: ',r.stepCounter,'\n')
print('OPC')
#parseOPC()
#parseOPC()
print('mem: ',memMap())

keyboard.on_press(pressEvent)
keyboard.add_hotkey('ctrl+z', quitProg)
