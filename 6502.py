import keyboard
import os
from bitarray import bitarray


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
	def updateEA(self):
		self.eA[1:] = self.PC

		self.eA[1] = self.eA[4]
		self.eA[2] = self.eA[5]
		self.eA[3] = self.eA[6]
		self.eA[4] = self.eA[7]
		self.eA[5] = self.eA[8]
		self.eA[6] = self.eA[9]
		self.eA[7] = self.eA[10]
		self.eA[8] = self.eA[11]
		self.eA[9] = self.eA[12]
		self.eA[10] = self.eA[13]
		self.eA[11] = self.eA[14]
		self.eA[12] = self.eA[15]
		self.eA[13] = self.eA[16]
		self.eA[14] = self.zeros[0]
		self.eA[15] = self.zeros[0]
		self.eA[16] = self.zeros[0]


r = registers(PC,stackPoint,eA,acc,regX,regY,flagReg,ones,zeros,stepCounter,instructReg)

zeroPage = bitarray(2048)
stack = bitarray(2048)
IO = bitarray(2048)
vectors = bitarray(48)
rom = bitarray(32768)
ram = bitarray(28624)

#LDY immediate  1010 0000
#1010 0101      1010 0101
#STY Y->64 		1000 0100
#64             0100 0000
#INC z64        1110 0110
#64             0100 0000
#STY Y->64 		1000 0100
#64             0100 0000
#JMP to inc     0110 1100

prog = bitarray('1010 0000 1010 0101 1000 0100 0100 0000 1110 0110 0100 0000 1000 0100 0100 0000 0110 1100 0000 0000 0000 0100',endian='big')
i1 = 0
while(i1<72):
	zeroPage[i1] = prog[i1]
	i1+=1

class execute():
	def __init__(self):
		global r

	def bpl(self):
		if(flagReg[0]==zeros[1]):
			incPC()
			data = memMap()
			sumReg, c3 = megaAdder(cIn=0, rA = PC[8:], rB = data, carry=0,zeros=0,overflow=0,neg=0)
			sumReg1, c3 = megaAdder(cIn=c3, rA = PC[:8], rB = zeros, carry=0,zeros=0,overflow=0,neg=0)
			r.PC[8:] = sumReg
			r.PC[:8] = sumReg1
			r.updateEA()
	def bmi(self):
		if(flagReg[0]==ones[1]):
			incPC()
			data = memMap()
			sumReg, c3 = megaAdder(cIn=0, rA = PC[8:], rB = data, carry=0,zeros=0,overflow=0,neg=0)
			sumReg1, c3 = megaAdder(cIn=c3, rA = PC[:8], rB = zeros, carry=0,zeros=0,overflow=0,neg=0)
			r.PC[8:] = sumReg
			r.PC[:8] = sumReg1
			r.updateEA()
	def bvc(self):
		if(flagReg[1]==zeros[1]):
			incPC()
			data = memMap()
			sumReg, c3 = megaAdder(cIn=0, rA = PC[8:], rB = data, carry=0,zeros=0,overflow=0,neg=0)
			sumReg1, c3 = megaAdder(cIn=c3, rA = PC[:8], rB = zeros, carry=0,zeros=0,overflow=0,neg=0)
			r.PC[8:] = sumReg
			r.PC[:8] = sumReg1
			r.updateEA()
	def bvs(self):
		if(flagReg[1]==ones[1]):
			incPC()
			data = memMap()
			sumReg, c3 = megaAdder(cIn=0, rA = PC[8:], rB = data, carry=0,zeros=0,overflow=0,neg=0)
			sumReg1, c3 = megaAdder(cIn=c3, rA = PC[:8], rB = zeros, carry=0,zeros=0,overflow=0,neg=0)
			r.PC[8:] = sumReg
			r.PC[:8] = sumReg1
			r.updateEA()
	def bcc(self):
		if(flagReg[7]==zeros[7]):
			incPC()
			data = memMap()
			sumReg, c3 = megaAdder(cIn=0, rA = PC[8:], rB = data, carry=0,zeros=0,overflow=0,neg=0)
			sumReg1, c3 = megaAdder(cIn=c3, rA = PC[:8], rB = zeros, carry=0,zeros=0,overflow=0,neg=0)
			r.PC[8:] = sumReg
			r.PC[:8] = sumReg1
			r.updateEA()
	def bcs(self):
		if(flagReg[7]==ones[7]):
			incPC()
			data = memMap()
			sumReg, c3 = megaAdder(cIn=0, rA = PC[8:], rB = data, carry=0,zeros=0,overflow=0,neg=0)
			sumReg1, c3 = megaAdder(cIn=c3, rA = PC[:8], rB = zeros, carry=0,zeros=0,overflow=0,neg=0)
			r.PC[8:] = sumReg
			r.PC[:8] = sumReg1
			r.updateEA()
	def bne(self):
		if(flagReg[6]==zeros[6]):
			incPC()
			data = memMap()
			sumReg, c3 = megaAdder(cIn=0, rA = PC[8:], rB = data, carry=0,zeros=0,overflow=0,neg=0)
			sumReg1, c3 = megaAdder(cIn=c3, rA = PC[:8], rB = zeros, carry=0,zeros=0,overflow=0,neg=0)
			r.PC[8:] = sumReg
			r.PC[:8] = sumReg1
			r.updateEA()
	def beq(self):
		if(flagReg[6]==ones[6]):
			incPC()
			data = memMap()
			sumReg, c3 = megaAdder(cIn=0, rA = PC[8:], rB = data, carry=0,zeros=0,overflow=0,neg=0)
			sumReg1, c3 = megaAdder(cIn=c3, rA = PC[:8], rB = zeros, carry=0,zeros=0,overflow=0,neg=0)
			r.PC[8:] = sumReg
			r.PC[:8] = sumReg1
			r.updateEA()
	def brk(self):
		pass
	def jsrAbsolute(self):   #THIS ISNT FINISHED IT DOESNT PUT ANYTHING ONTO STACK
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
		#print('lda')
		#print('effective address: ',r.eA)
		data = memMap()
		r.acc = data
		#print('LDA r.acc: ',r.acc)
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
e = execute()


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
	aaa = count[:4]
	bbb = count[4:]
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

	#print('PC: ',r.PC)
def memMap(write=False, data=r.zeros):
	if(r.eA[0] == r.ones[0] and write==False):
		return r.acc
	elif(r.eA[0] == r.ones[0] and write==True):
		r.acc = data
	mapLen = 0
	eAddy = r.eA[1:17]
	#print('memmap eA: ',r.eA)
	address = eAddy.tobytes()
	address = int.from_bytes(address, "big")
	#print('addy: ',address)
	addressStart = address
	#print('aStart: ',addressStart)
	endAddress = address + 8
	#print('endAddress: ', endAddress)
	if(address<2048):
		if(write != True):	
			data = zeroPage[addressStart:endAddress]
			#print('0 page data: ',data)
			return data
		zeroPage[addressStart:endAddress] = data
		#print('write 0 page: ',zeroPage[addressStart:endAddress],data)
		return data
	mapLen+=2048
	if(address>=mapLen and address < (mapLen+2048)):
		if(write != True):	
			data = stack[(addressStart-mapLen):(endAddress-mapLen)]
			#print('stack data: ', data)
			return data
		stack[(addressStart-mapLen):(endAddress-mapLen)] = data
		#print('write stack: ',stack[(addressStart-mapLen):(endAddress-mapLen)])
		return data
	mapLen+=2048
	if(address>=mapLen and address < (mapLen+28624)):
		if(write != True):	
			data = ram[(addressStart-mapLen):(endAddress-mapLen)]
			#print('ram data: ', data)
			return data
		ram[(addressStart-mapLen):(endAddress-mapLen)] = data
		#print('write ram: ',ram[(addressStart-mapLen):(endAddress-mapLen)])
		return data
	mapLen+=28624
	if(address>=mapLen and address < (mapLen+48)):
		if(write != True):	
			data = vectors[(addressStart-mapLen):(endAddress-mapLen)]
			#print('vectors data: ', data)
			return data
		vectors[(addressStart-mapLen):(endAddress-mapLen)] = data
		#print('write vectors: ',vectors[(addressStart-mapLen):(endAddress-mapLen)])
		return data
	mapLen+=48
	if(address>=mapLen and address < (mapLen+32768)):
		if(write != True):	
			data = rom[(addressStart-mapLen):(endAddress-mapLen)]
			#print('rom data: ', data)
			return data
		rom[(addressStart-mapLen):(endAddress-mapLen)] = data
		#print('write rom: ',rom[(addressStart-mapLen):(endAddress-mapLen)])
		return data
	mapLen+=32768
	if(address>=mapLen):
		print('address out of range')
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
		#print("ra: ",rA,cIn)
	if((rA[0]^rB[0])^r.ones[0]):
		#print('set x',rA[0])
		x = rA[0]
		y = True

	s, cIn = fullAdder(rA[7],rB[7],cIn)
	#print(cIn)
	s1, cIn = fullAdder(rA[6],rB[6],cIn)
	#print(cIn)
	s2, cIn = fullAdder(rA[5],rB[5],cIn)
	#print(cIn)
	s3, cIn = fullAdder(rA[4],rB[4],cIn)
	#print(cIn)
	s4, cIn = fullAdder(rA[3],rB[3],cIn)
	#print(cIn)
	s5, cIn = fullAdder(rA[2],rB[2],cIn)
	#print(cIn)
	s6, cIn = fullAdder(rA[1],rB[1],cIn)
	#print(cIn)
	s7, cOut = fullAdder(rA[0],rB[0],cIn)
	#print(cOut)
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
	#print('zF: ',(zF))
	r.flagReg[6] = (zF)
	return sumReg, cOut
def fetch():
	global r
	#print('fetchdatshi')
	#print(r.eA,'\n')
	data = memMap()
	r.instructReg = data


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
	#print("KKKKKKKKKKKKKK",k)

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

class doAddressMode:
	def zeroPageX(self):
		r.eA[0] = r.zeros[0]
		incPC()
		data = memMap()
		r.eA[1:9] = r.zeros
		data, carry = megaAdder(cIn=0,carry=0,overflow=0,neg=0,zero=0,rA=data,rB=regX)
		r.eA[9:] = data
		r.updateEA()
	def zeroPage(self):	
		r.eA[0] = r.zeros[0]
		incPC()
		data = memMap()
		r.eA[1:9] = r.zeros
		r.eA[9:] = data
		r.updateEA()
	def absoluteX(self):
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
		incPC()
	def absolute(self):
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
		r.eA[0] = r.zeros[0]
		incPC()
		data = memMap()
		r.eA[1:9] = r.zeros
		data, carry = megaAdder(cIn=0,carry=0,overflow=0,neg=0,zero=0,rA=data,rB=regY)
		r.eA[9:] = data
		r.updateEA()
	def zeroPageXOther(self):
		r.eA[0] = r.zeros[0]
		#literally fuck this shit lmao
		incPC()
	def absoluteY(self):
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
		r.eA[0] = r.ones[0]
dam = doAddressMode()
def getAddr(instruction):
	found = search(instruction)
	foundIns = found[0]
	addrM = foundIns[5:]
	grp = foundIns[:2]
	if(addrM==bitarray('111',endian='big')):
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
	fetch()
	getAddr(r.instructReg)
	#print("ACC: ",r.acc)



def pressEvent(callback):
	charBuff.append(callback.name)
def quitProg():
	#print('tryna quit...')
	keyboard.unhook_all()
	os._exit(1)


while True:
	cycle()
	print(acc)

keyboard.on_press(pressEvent)
keyboard.add_hotkey('ctrl+z', quitProg)
