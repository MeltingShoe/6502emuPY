import keyboard
import os
from bitarray import bitarray
#ba = bitarray

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
eAddy = bitarray('0000 0000 0000 0000', endian='big')
stepCounter = bitarray('0000', endian='big')
instructReg = bitarray('0000 0000', endian='big')
physicalAddy = bitarray('1111 1111 1111 1111')
accC = bitarray('010', endian='big')

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
print(zeroPage)
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

bplC = bitarray('0001 0000', endian='big')
bmiC = bitarray('0011 0000', endian='big')
bvcC = bitarray('0101 0000', endian='big')
bvsC = bitarray('0111 0000', endian='big')
bccC = bitarray('1001 0000', endian='big')
bcsC = bitarray('1011 0000', endian='big')
bneC = bitarray('1101 0000', endian='big')
beqC = bitarray('1111 0000', endian='big')

brkC = bitarray('0000 0000', endian='big')
jsrAbsoluteC = bitarray('0010 0000', endian='big')
rtiC = bitarray('0100 0000', endian='big')
rtsC = bitarray('0110 0000', endian='big')

phpC = bitarray('0000 1000', endian='big')
plpC = bitarray('0010 1000', endian='big')
phaC = bitarray('0100 1000', endian='big')
plaC = bitarray('0110 1000', endian='big')
deyC = bitarray('1000 1000', endian='big')
tayC = bitarray('1010 1000', endian='big')
inyC = bitarray('1100 1000', endian='big')
inxC = bitarray('1110 1000', endian='big')

clcC = bitarray('0001 1000', endian='big')
secC = bitarray('0011 1000', endian='big')
cliC = bitarray('0101 1000', endian='big')
seiC = bitarray('0111 1000', endian='big')
tyaC = bitarray('1001 1000', endian='big')
clvC = bitarray('1011 1000', endian='big')
cldC = bitarray('1101 1000', endian='big')
sedC = bitarray('1111 1000', endian='big')

txaC = bitarray('1000 1010', endian='big')
txsC = bitarray('1001 1010', endian='big')
taxC = bitarray('1010 1010', endian='big')
tsxC = bitarray('1011 1010', endian='big')
dexC = bitarray('1100 1010', endian='big')
nopC = bitarray('1110 1010', endian='big')

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
zeroPageC = bitarray('001', endian='big')
immediateC = bitarray('010', endian='big')
absoluteC = bitarray('011', endian='big')
zeroPageYC = bitarray('100', endian='big')
directZeroPageXC = bitarray('101', endian='big')
absoluteYC = bitarray('110', endian='big')
absoluteXC = bitarray('111', endian='big')

def addEight(count, cIn=0):
	count, carryOut = megaAdder(cIn=0, carry=False, zero=False, neg=False, overflow = False, rA = count, rB = bitarray('0000 1000',endian='big'))
	return count
def inc4bits(count):
	if(count[3]==ones[3]):
		count[3]=zeros[3]
		if(count[2]==ones[2]):
			count[2]=zeros[2]
			if(count[1]==ones[1]):
				count[1]=zeros[1]
				if(count[0]==ones[0]):
					count[0]=zeros[0]
					return True, count
				else:
					count[0]=ones[0]
			else:	
				count[1]=ones[1]
		else:
			count[2]=ones[2]
	else:	
		count[3]=ones[3]
	return False, count

def incStep(count):
	f, count = inc4bits(count)
	return count

def inc8bits(count):
	aaa = bitarray('0000',endian='big')
	bbb = bitarray('0000',endian='big')
	ooo = bitarray('0000 0000',endian='big')
	aaa = PC[:4]
	bbb = PC[4:]
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
	global PC
	global eA
	aaa = bitarray('0000',endian='big')
	bbb = bitarray('0000',endian='big')
	ccc = bitarray('0000',endian='big')
	ddd = bitarray('0000',endian='big')
	aaa = PC[:4]
	bbb = PC[4:8]
	ccc = PC[8:12]
	ddd = PC[12:16]
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
	PC[0]=aaa[0]
	PC[1]=aaa[1]
	PC[2]=aaa[2]
	PC[3]=aaa[3]
	PC[4]=bbb[0]
	PC[5]=bbb[1]
	PC[6]=bbb[2]
	PC[7]=bbb[3]
	PC[8]=ccc[0]
	PC[9]=ccc[1]
	PC[10]=ccc[2]
	PC[11]=ccc[3]
	PC[12]=ddd[0]
	PC[13]=ddd[1]
	PC[14]=ddd[2]
	PC[15]=ddd[3]

	eA = PC

	eA[1] = eA[4]
	eA[2] = eA[5]
	eA[3] = eA[6]
	eA[4] = eA[7]
	eA[5] = eA[8]
	eA[6] = eA[9]
	eA[7] = eA[10]
	eA[8] = eA[11]
	eA[9] = eA[12]
	eA[10] = eA[13]
	eA[11] = eA[14]
	eA[12] = eA[15]
	eA[13] = eA[16]
	eA[14] = zeros[0]
	eA[15] = zeros[0]
	eA[16] = zeros[0]

	print('PC: ',PC)


def memMap(write=False, data=zeros):
	if(eA[0] == ones[0] and write==False):
		return acc
	elif(eA[0] == ones[0] and write==True):
		acc = data
	mapLen = 0
	eAddy = eA[1:17]
	print('memmap eA: ',eA)
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

def megaAdder(cIn=0, carry=True, zero=True, neg=True, overflow = True, rA = acc, rB = regB, sub = False):
	x = zeros[0]
	y=True
	if sub:
		cIn = cIn^ones[0]
		#rA = rA^ones
		rB = rB^ones
		print("ra: ",rA,cIn)
	if((rA[0]^rB[0])^ones[0]):
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
			flagReg[1] = ones[1]
		else:
			flagReg[1] = zeros[1]
	sumReg[0] = s7
	sumReg[1] = s6
	sumReg[2] = s5
	sumReg[3] = s4
	sumReg[4] = s3
	sumReg[5] = s2
	sumReg[6] = s1
	sumReg[7] = s
	if(carry):
		flagReg[7] = cOut
	if(s7):
		flagReg[0] = s7
	#if(zero):
	zF = (s|s1|s2|s3|s4|s5|s6|s7) ^ ones[1]
	print('zF: ',(zF))
	flagReg[6] = (zF)
	return sumReg, cOut


def parseOPC():
	global stepCounter
	global PC
	global instructReg
	global acc
	global flagReg
	global immediateC
	global zeroPageC
	global accC
	global absoluteC
	global eA
	global zeroPageYC
	global zeroPageXC
	global absoluteYC
	global absoluteXC
	data = bitarray('0000 0000',endian='big')
	eight = bitarray('0000 1000',endian='big')
	if(stepCounter == bitarray('0000',endian='big')):
		print('fetchdatshi')
		print(eA,'\n')
		data = memMap()
		instructReg = data
		print('Step: ',stepCounter,'\n')
		discard, stepCounter = inc4bits(stepCounter)
		print('Step: ',stepCounter,'\n')
	if(stepCounter == bitarray('0001',endian='big')):
		print('in step 2')
		instr = bitarray('0000 0000',endian='big')
		instr = instructReg
		opc = bitarray('000',endian='big')
		grp = bitarray('00',endian='big')
		addrMode = bitarray('000',endian='big')
		opc = instr[:3]
		addrMode = instr[3:6]
		addrMode = instr[6:]
		print(opc,grp,addrMode)
		print('Step: ',stepCounter,'\n')
		discard, stepCounter = inc4bits(stepCounter)
		print('Step: ',stepCounter,'\n')
	opc1 = bitarray('0000 0000',endian='big')
	opc1[0:3] = opc
	opc1[3:6] = addrMode
	opc1[6:8] = grp
	if(grp == g1c):
		zeroPageXC = bitarray('000', endian='big')
		zeroPageC = bitarray('001', endian='big')
		immediateC = bitarray('010', endian='big')
		absoluteC = bitarray('011', endian='big')
		zeroPageYC = bitarray('100', endian='big')

		absoluteYC = bitarray('110', endian='big')
		absoluteXC = bitarray('111', endian='big')
	elif(grp == g2c | g3c):
		immediateC = bitarray('000', endian='big')
		zeroPageC = bitarray('001', endian='big')
		accC = bitarray('010', endian='big')
		absoluteC = bitarray('011', endian='big')

		absoluteXC = bitarray('111', endian='big')

	if(addrMode==immediateC):
		print('using immediate addr')
		incPC()
		print('pc',PC)
		print('eA',eA)
	elif(addrMode==zeroPageYC):
		print('using 0page + Y addr')
		incPC()
		print('eA: ',eA)
		data = memMap()
		eA[:9] = bitarray('0000 0000 0',endian='big')
		data, carryOut = megaAdder(cIn=0,zero=False,carry=False,overflow=False,neg=False,rA=data, rB=regY)
		eA[9:] = data
	elif(addrMode==absoluteYC):
		print('using absolute + Y addr')
		incPC()
		print('eA: ',eA)
		temp = memMap()
		incPC()
		print('eA: ',eA)
		data = memMap()
		PC[0:8] = temp
		PC[8:16] = data
		PC, carryOut = megaAdder(cIn=0,zero=False,carry=False,overflow=False,neg=False,rA=PC[8:16], rB=regY)
		PC, carryOut = megaAdder(cIn=carryOut,zero=False,carry=False,overflow=False,neg=False,rA=PC[0:8], rB=zeros)
		eA = PC

		eA[1] = eA[4]
		eA[2] = eA[5]
		eA[3] = eA[6]
		eA[4] = eA[7]
		eA[5] = eA[8]
		eA[6] = eA[9]
		eA[7] = eA[10]
		eA[8] = eA[11]
		eA[9] = eA[12]
		eA[10] = eA[13]
		eA[11] = eA[14]
		eA[12] = eA[15]
		eA[13] = eA[16]
		eA[14] = zeros[0]
		eA[15] = zeros[0]
		eA[16] = zeros[0]
		print('pc, ea ',PC,eA)
	elif(addrMode==zeroPageXC):
		print('using 0page + X addr')
		incPC()
		print('eA: ',eA)
		data = memMap()
		eA[:9] = bitarray('0000 0000 0',endian='big')
		data, carryOut = megaAdder(cIn=0,zero=False,carry=False,overflow=False,neg=False,rA=data, rB=regX)
		eA[9:] = data
	elif(addrMode==absoluteXC):
		print('using absolute + X addr')
		incPC()
		print('eA: ',eA)
		temp = memMap()
		incPC()
		print('eA: ',eA)
		data = memMap()
		PC[0:8] = temp
		PC[8:16] = data
		PC, carryOut = megaAdder(cIn=0,zero=False,carry=False,overflow=False,neg=False,rA=PC[8:16], rB=regX)
		PC, carryOut = megaAdder(cIn=carryOut,zero=False,carry=False,overflow=False,neg=False,rA=PC[0:8], rB=zeros)
		eA = PC

		eA[1] = eA[4]
		eA[2] = eA[5]
		eA[3] = eA[6]
		eA[4] = eA[7]
		eA[5] = eA[8]
		eA[6] = eA[9]
		eA[7] = eA[10]
		eA[8] = eA[11]
		eA[9] = eA[12]
		eA[10] = eA[13]
		eA[11] = eA[14]
		eA[12] = eA[15]
		eA[13] = eA[16]
		eA[14] = zeros[0]
		eA[15] = zeros[0]
		eA[16] = zeros[0]
		print('pc, ea ',PC,eA)
	elif(addrMode==zeroPageC):
		print('using 0page addr')
		incPC()
		print('eA: ',eA)
		data = memMap()
		eA[:9] = bitarray('0000 0000 0',endian='big')
		eA[9:17] = data
		print('pc',PC)
		print('ea',eA)
	elif(addrMode==accC):
		print('using acc addr')
		incPC()
		eA[0] = ones[0]
		print('pc, ea ',PC,eA)
	elif(addrMode==absoluteC):
		print('using absolute addr')
		incPC()
		print('eA: ',eA)
		temp = memMap()
		incPC()
		print('eA: ',eA)
		data = memMap()
		PC[0:8] = temp
		PC[8:16] = data
		eA = PC

		eA[1] = eA[4]
		eA[2] = eA[5]
		eA[3] = eA[6]
		eA[4] = eA[7]
		eA[5] = eA[8]
		eA[6] = eA[9]
		eA[7] = eA[10]
		eA[8] = eA[11]
		eA[9] = eA[12]
		eA[10] = eA[13]
		eA[11] = eA[14]
		eA[12] = eA[15]
		eA[13] = eA[16]
		eA[14] = zeros[0]
		eA[15] = zeros[0]
		eA[16] = zeros[0]
		print('pc, ea ',PC,eA)

	# tried to use match. it did not work
	if(grp == g1c):
		print('g1')
		if(opc==oraC):
			print('ora')
			print('effective address: ',eA)
			data = memMap()
			print('acc, data',acc,data)
			acc = acc | data
			print('ORA acc: ',acc)
			megaAdder(carry=False,overflow=False,rB=zeros)

			incPC()
			stepCounter = bitarray('0000',endian='big')
		elif(opc==andC):
			print('and')
			print('effective address: ',eA)
			data = memMap()
			print('acc, data',acc,data)
			acc = acc & data
			print('AND acc: ',acc)
			megaAdder(carry=False,overflow=False,rB=zeros)

			incPC()
			stepCounter = bitarray('0000',endian='big')
		elif(opc==eorC):
			print('eor')
			print('effective address: ',eA)
			data = memMap()
			print('acc, data',acc,data)
			acc = acc ^ data
			print('EOR acc: ',acc)
			megaAdder(carry=False,overflow=False,rB=zeros)

			incPC()
			stepCounter = bitarray('0000',endian='big')
		elif(opc==adcC):
			print('adc')
			print('effective address: ',eA)
			data = memMap()
			print('acc, data',acc,data)
			acc, carryOut = megaAdder(cIn=flagReg[7],rA=acc, rB=data)
			print('ADC acc: ',acc)

			incPC()
			stepCounter = bitarray('0000',endian='big')
		elif(opc==staC):
			print('staC')
			print('effective address: ',eA)
			memMap(write=True,data=acc)
			print('STA DONE')
			incPC()
			stepCounter = bitarray('0000',endian='big')
		elif(opc==ldaC):
			print('lda')
			print('effective address: ',eA)
			data = memMap()
			acc = data
			print('LDA acc: ',acc)
			incPC()
			stepCounter = bitarray('0000',endian='big')
		elif(opc==cmpC):
			print('cmp')
			print('effective address: ',eA)
			data = memMap()
			print('acc, data',acc,data)
			flagReg[7]=zeros[7]
			megaAdder(cIn=flagReg[7],rA=acc, rB=data, overflow=False, sub=True)
			print('CMP flags: ',flagReg)

			incPC()
			stepCounter = bitarray('0000',endian='big')
		elif(opc==sbcC):
			print('sbc')
			print('effective address: ',eA)
			data = memMap()
			print('acc, data',acc,data)
			acc, carryOut = megaAdder(cIn=flagReg[7],rA=acc, rB=data, sub=True)
			print('SBC acc: ',acc)

			incPC()
			stepCounter = bitarray('0000',endian='big')
		else:
			print('invalid opcode')
		stepCounter = bitarray('0000',endian='big')

	elif(grp == g2c):
		print('g2')
		if(opc==aslC):
			print('asl')
			print('effective address: ',eA)
			data = memMap()
			print('data',data)
			flagReg[7]=data[0]
			data[0]=data[1]
			data[1]=data[2]
			data[2]=data[3]
			data[3]=data[4]
			data[4]=data[5]
			data[5]=data[6]
			data[6]=data[7]
			data[7]=zeros[7]

			megaAdder(cIn=flagReg[7],rA=data, rB=zeros, overflow=False)
			print('ASL data: ',data)

			incPC()
			stepCounter = bitarray('0000',endian='big')
		elif(opc==rolC):
			print('rol')
			print('effective address: ',eA)
			data = memMap()
			print('data',data)
			temp = flagReg[7]
			flagReg[7]=data[0]
			data[0]=data[1]
			data[1]=data[2]
			data[2]=data[3]
			data[3]=data[4]
			data[4]=data[5]
			data[5]=data[6]
			data[6]=data[7]
			data[7]=temp

			megaAdder(cIn=flagReg[7],rA=data, rB=zeros, overflow=False)
			print('ROL data: ',data)

			incPC()
			stepCounter = bitarray('0000',endian='big')
		elif(opc==lsrC):
			print('lsr')
			print('effective address: ',eA)
			data = memMap()
			print('data',data)
			flagReg[7]=data[7]
			data[7]=data[6]
			data[6]=data[5]
			data[5]=data[4]
			data[4]=data[3]
			data[3]=data[2]
			data[2]=data[1]
			data[1]=data[0]
			data[0]=zeros[0]

			megaAdder(cIn=flagReg[7],rA=data, rB=zeros, overflow=False)
			print('LSR data: ',data)

			incPC()
			stepCounter = bitarray('0000',endian='big')
		elif(opc==rorC):
			print('ror')
			print('effective address: ',eA)
			data = memMap()
			print('data',data)
			temp = flagReg[7]
			flagReg[7]=data[7]
			data[7]=data[6]
			data[6]=data[5]
			data[5]=data[4]
			data[4]=data[3]
			data[3]=data[2]
			data[2]=data[1]
			data[1]=data[0]
			data[0]=temp

			megaAdder(cIn=flagReg[7],rA=data, rB=zeros, overflow=False)
			print('ROR data: ',data)

			incPC()
			stepCounter = bitarray('0000',endian='big')
		elif(opc==stxC):
			print('staC')
			print('effective address: ',eA)
			memMap(write=True,data=regX)
			print('STX DONE')
			incPC()
			stepCounter = bitarray('0000',endian='big')
		elif(opc==ldxC):
			print('ldx')
			print('effective address: ',eA)
			data = memMap()
			regX = data
			print('LDX acc: ',acc)
			incPC()
			stepCounter = bitarray('0000',endian='big')
		elif(opc==decC):
			print('dec')
			print('effective address: ',eA)
			data = memMap()
			print('data',data)
			megaAdder(cIn=zeros[7],rA=data, rB=bitarray('0000 0001',endian='big'), overflow=False, carry=False, sub=True)
			print('DEC data: ',data)

			incPC()
			stepCounter = bitarray('0000',endian='big')
		elif(opc==incC):
			print('inc')
			print('effective address: ',eA)
			data = memMap()
			print('data',data)
			megaAdder(cIn=zeros[7],rA=data, rB=bitarray('0000 0001',endian='big'), overflow=False, carry=False, sub=True)
			print('DEC data: ',data)

			incPC()
			stepCounter = bitarray('0000',endian='big')
		else:
			print('invalid opcode')
		stepCounter = bitarray('0000',endian='big')


	elif(grp == g3c):
		print('g3')
		if(opc==bitC):
			print('bit')
			print('effective address: ',eA)
			data = memMap()
			print('acc, data',acc,data)
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
			print('effective address: ',eA)
			data = memMap()
			print('y, data',regY,data)
			flagReg[7]=zeros[7]
			megaAdder(cIn=flagReg[7],rA=regY, rB=data, overflow=False, sub=True)
			print('CPX flags: ',flagReg)

			incPC()
			stepCounter = bitarray('0000',endian='big')
		elif(opc==rolC):
			pass
		elif(opc==cpxC):
			print('cpx')
			print('effective address: ',eA)
			data = memMap()
			print('x, data',regX,data)
			flagReg[7]=zeros[7]
			megaAdder(cIn=flagReg[7],rA=regX, rB=data, overflow=False, sub=True)
			print('CPX flags: ',flagReg)

			incPC()
			stepCounter = bitarray('0000',endian='big')
		elif(opc==rolC):
			pass
		stepCounter = bitarray('0000',endian='big')
	
	elif(opc1==bplC):
		pass
	elif(opc1==bmiC):
		pass
	elif(opc1==bvcC):
		pass
	elif(opc1==bvsC):
		pass
	elif(opc1==bccC):
		pass
	elif(opc1==bcsC):
		pass
	elif(opc1==bneC):
		pass
	elif(opc1==beqC):
		pass

	elif(opc1==brkC):
		pass
	elif(opc1==jsrAbsoluteC):
		pass
	elif(opc1==rtiC):
		pass
	elif(opc1==rtsC):
		pass

	elif(opc1==phpC):
		pass
	elif(opc1==plpC):
		pass
	elif(opc1==phaC):
		pass
	elif(opc1==plaC):
		pass
	elif(opc1==deyC):
		print('dey')
		regY= megaAdder(cIn=zeros[7],rA=regY, rB=bitarray('0000 0001',endian='big'), overflow=False, carry=False, sub=True)
		print('DEY data: ',regX)

		incPC()
		stepCounter = bitarray('0000',endian='big')
	elif(opc1==tayC):
		print('tay')
		regY = acc
		print('TAY regY: ',regY)
		incPC()
		stepCounter = bitarray('0000',endian='big')
	elif(opc1==inyC):
		print('iny')
		regY= megaAdder(cIn=zeros[7],rA=regY, rB=bitarray('0000 0001',endian='big'), overflow=False, carry=False)
		print('INY data: ',regY)

		incPC()
		stepCounter = bitarray('0000',endian='big')
	elif(opc1==inxC):
		print('inx')
		regX= megaAdder(cIn=zeros[7],rA=regX, rB=bitarray('0000 0001',endian='big'), overflow=False, carry=False)
		print('INX data: ',regX)

		incPC()
		stepCounter = bitarray('0000',endian='big')

	elif(opc1==clcC):
		print('clc')
		flagReg[7] = zeros[7]
		print('CLC flags: ',flagReg)
		incPC()
		stepCounter = bitarray('0000',endian='big')
	elif(opc1==secC):
		print('sec')
		flagReg[7] = ones[7]
		print('SEC flags: ',flagReg)
		incPC()
		stepCounter = bitarray('0000',endian='big')
	elif(opc1==cliC):
		print('cli')
		flagReg[5] = zeros[7]
		print('CLI flags: ',flagReg)
		incPC()
		stepCounter = bitarray('0000',endian='big')
	elif(opc1==seiC):
		print('sei')
		flagReg[5] = ones[7]
		print('SEI flags: ',flagReg)
		incPC()
		stepCounter = bitarray('0000',endian='big')
	elif(opc1==tyaC):
		print('tya')
		acc = regY
		print('TYA acc: ',acc)
		incPC()
		stepCounter = bitarray('0000',endian='big')
	elif(opc1==clvC):
		print('clv')
		flagReg[1] = zeros[7]
		print('CLV flags: ',flagReg)
		incPC()
		stepCounter = bitarray('0000',endian='big')
#no CLD/SED cuz no decimal mode
	elif(opc1==txaC):
		print('txa')
		acc = regX
		print('TXA acc: ',acc)
		incPC()
		stepCounter = bitarray('0000',endian='big')
	elif(opc1==txsC):
		print('txs')
		stackPoint = regX
		print('TXS stack: ',stackPoint)
		incPC()
		stepCounter = bitarray('0000',endian='big')
	elif(opc1==taxC):
		print('tax')
		regX = acc
		print('TAX regX: ',regX)
		incPC()
		stepCounter = bitarray('0000',endian='big')
	elif(opc1==tsxC):
		print('tsx')
		regX = stackPoint
		print('TSX regX: ',regX)
		incPC()
		stepCounter = bitarray('0000',endian='big')
	elif(opc1==dexC):
		print('dex')
		regX= megaAdder(cIn=zeros[7],rA=regX, rB=bitarray('0000 0001',endian='big'), overflow=False, carry=False, sub=True)
		print('DEX data: ',regX)

		incPC()
		stepCounter = bitarray('0000',endian='big')
	elif(opc1==nopC):
		print('nop')
		incPC()
		stepCounter = bitarray('0000',endian='big')



def pressEvent(callback):
	charBuff.append(callback.name)
def quitProg():
	print('tryna quit...')
	keyboard.unhook_all()
	os._exit(1)




print('ACC: ',acc)
print('Step: ',stepCounter,'\n')
print('OPC')
parseOPC()
parseOPC()
print('mem: ',memMap())



keyboard.on_press(pressEvent)
keyboard.add_hotkey('ctrl+z', quitProg)