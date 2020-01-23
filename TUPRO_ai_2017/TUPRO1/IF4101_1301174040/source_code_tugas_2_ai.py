import math
import csv
import numpy
import random


#suhu : 2bit, 
#waktu : 2bit, 
#cuaca : 2bit, 
#kelembaban : 2bit, 
#keputusan : 1bit


def datalatih():
    data = []
    with open('data_latih_opsi_1.csv') as dat:
        read = csv.reader(dat)
        for row in read:
            data.append(row)
    return data

def datauji():
    data = []
    with open('data_uji_opsi_1.csv') as dat:
        read = csv.reader(dat)
        for row in read:
            data.append(row)
    return data

#create a kromosom
def indv():
    ind = []
    for i in range(9):
        x = random.randint(0,1)
        ind.append(x)
    return ind

#create population
def pop(jml):
    pop = []
    for i in range(jml):
        ind = indv()
        pop.append(ind)
    return pop

#Penerjemah suhu
def transTemp(data,i):
    if(data[i][0]=='normal'):
        suhu = [1,1]
    elif(data[i][0]=='rendah'):
        suhu = [0,1]
    elif(data[i][0]=='tinggi'):
        suhu = [1,0]
    return suhu

#Penerjemah waktu
def transHari(data,i):
    if(data[i][1]=='pagi'):
        hari = [1,1]
    if(data[i][1]=='siang'):
        hari = [1,0]
    if(data[i][1]=='sore'):
        hari = [0,1]
    if(data[i][1]=='malam'):
        hari = [0,0]
    return hari

#Penerjemah kondisi langit
def transLangit(data,i):
    if(data[i][2]=='berawan'):
        langit = [1,1]
    if(data[i][2]=='cerah'):
        langit = [1,0]
    if(data[i][2]=='rintik'):
        langit = [0,1]
    if(data[i][2]=='hujan'):
        langit = [0,0]
    return langit

#Penerjemah kelembapan
def transLembab(data,i):
    if(data[i][3]=='normal'):
        lembab = [1,1]
    elif(data[i][3]=='rendah'):
        lembab = [0,1]
    elif(data[i][3]=='tinggi'):
        lembab = [1,0]
    return lembab

#Penerjemah keputusan terbang atau tidak
def buatKeputusan(data,i):
    if(data[i][4]=='ya'):
        dec = 1
    else:
        dec = 0
    return dec

#decode string to 2-bit biner
def translate(data):
    dec = []
    popcsv = []
    for i in range(len(data)):
        suhu = transTemp(data,i)
        hari = transHari(data,i)
        langit = transLangit(data,i)
        lembab = transLembab(data,i)
        keputusan = buatKeputusan(data,i)
        dec = suhu+hari+langit+lembab
        dec.append(keputusan)
        popcsv.append(dec)
    return popcsv

#calculating fitness
def fitness(pop,popcsv):
    cek = True
    fitneslist = []
    count = 0
    cek = True
    for i in range(len(pop)):
        for j in range(len(popcsv)):
            if (pop[i][:2] == [1,1]):
                
                if(pop[i][2:4] == popcsv[j][2:4]):
                   
                    if(pop[i][4:6] == popcsv[j][4:6]):
                        
                        if(pop[i][6:8] == popcsv[j][6:8]):
                            
                            if(pop[i][8:9] == popcsv[j][8:9]):
                                count += 1  
                                
                            else:
                                cek = False
                                
                        else:
                            cek = False
                            
                    else:
                        cek = False
                        
                else:
                    cek = False
                    
            elif (pop[i][:2] == [1,0]):

                if(pop[i][2:4] == popcsv[j][2:4]):
                  
                    if(pop[i][4:6] == popcsv[j][4:6]):
                        
                        if(pop[i][6:8] == popcsv[j][6:8]):
                           
                            if(pop[i][8:9] == popcsv[j][8:9]):
                                count += 1
                                
                            else:
                                cek = False
                                
                        else:
                            cek = False
                            
                    else:
                        cek = False
                        
                else:
                    cek = False
                    

            elif (pop[i][:2] == [0,1]):
               
                if(pop[i][2:4] == popcsv[j][2:4]):
                 
                    if(pop[i][4:6] == popcsv[j][4:6]):
                      
                        if(pop[i][6:8] == popcsv[j][6:8]):
                            
                            if(pop[i][8:9] == popcsv[j][8:9]):
                                count += 1
                                
                            else:
                                cek = False
                                
                        else:
                            cek = False
                            
                    else:
                        cek = False
                        
                else:
                    cek = False
            else:
                cek = False
        fitneslist.append(count/80)

    return fitneslist

#parents with roulette wheel 
def pilih_parent(fitness,pop):
    total=0
    for i in fitness:
        total += i
    idx_parent = []
    for j in range(2):
        r = random.random()
        idx = 0
        while (r>0) and (idx<19):
            r -= fitness[idx]/total
            idx = idx + 1
        idx_parent.append(idx)
    return idx_parent


def search(pop,index):
    i1 = index[0]   
    i2 = index[1]   
    p1 = pop[i1]    
    p2 = pop[i2]    
    return p1,p2

def crossover(p1,p2):
    prob = random.random()
    anak1 =[]
    anak2 =[]
    cek = True
    if prob > 0.1:
        while (cek != False):
            a =random.randint(0,len(p1))
            b =random.randint(0,len(p1))
            if (a<b):
                tipotlist = [a,b]
                cek = False
            else:
                cek = True

        #create first child
        a =p1[:tipotlist[0]]
        b =p2[tipotlist[0]:tipotlist[1]]
        c =p1[(tipotlist[1]):len(p1)]


        #create second child
        d =p2[:tipotlist[0]]
        e =p1[tipotlist[0]:tipotlist[1]]
        f =p2[tipotlist[1]:len(p2)]

        anak1 = a+b+c       
        anak2 = d+e+f
        return anak1,anak2
        
    else :
        return p1,p2

#mutasi biasa
def mutasi(p1,p2):
    hasil_mutasi = []
    for i in range(len(p1)):
        chance = random.random()
        if chance < 0.1:
            p1[i]=random.randint(0,1)

    for j in range(len(p2)):
        chance1 = random.random()
        if chance1 < 0.1:
            p2[j]=random.randint(0,1)   
    hasil_mutasi.append(p1)
    hasil_mutasi.append(p2)
    return hasil_mutasi

#fitness terbaik
def bestFitness(fitness):
   max = 0
   idx = 0
   for i in range(len(fitness)):
     if fitness[i] > max:
        max = fitness[i]
        idx = i
   return max,idx 

#kromosom terbaik
def bestKromosom(max,fitnesslist,pop):
    idx=-1
    for i in range(len(fitnesslist)):
        if max == fitnesslist[i]:
            idx = i
    return pop[idx]

#data ke csv sekalian ditranslate
def encSuhu (data,i):
    if(data[i][:2]==[1,1]):
        suhu = "Normal"
    elif(data[i][:2]==[0,1]):
        suhu = "Tinggi"
    elif(data[i][:2]==[1,0]):
        suhu = "Rendah"
    else:
        suhu = 'tidak diketahui'
    return suhu

def encHari (data,i):
    if(data[i][2:4]==[1,1]):
        hari = "Pagi"
    elif(data[i][2:4]==[1,0]):
        hari = "Siang"
    elif(data[i][2:4]==[0,1]):
        hari = "Sore"
    elif(data[i][2:4]==[0,0]):
        hari = 'Malam'
    return hari

def encLangit(data,i):
    if(data[i][4:6]==[1,1]):
        langit = "Berawan"
    elif(data[i][4:6]==[1,0]):
        langit = "Cerah"
    elif(data[i][4:6]==[0,1]):
        langit = "Rintik"
    elif(data[i][4:6]==[0,0]):
        langit = 'Hujan'
    return langit

def encLembab(data,i):
    if(data[i][6:8]==[1,1]):
        lembab = "Normal"
    elif(data[i][6:8]==[0,1]):
        lembab = "Tinggi"
    elif(data[i][6:8]==[1,0]):
        lembab = "Rendah"
    else:
        lembab = 'tidak diketahui'
    return lembab

def encDecision(data,i):
    if(data[i][8:9]==[1]):
        decision = 'ya'
    else:
        decision = 'tidak'
    return decision

def encode(data):
    enc = []
    dat_enc = []
    for i in range(len(data)):
        suhu = encSuhu(data,i)
        hari = encHari(data,i)
        langit = encLangit(data,i)
        lembab = encLembab(data,i)
        keputusan = encDecision(data,i)
        enc = [suhu,hari,langit,lembab,keputusan]
        dat_enc.append(enc)
    return dat_enc


def testPop(pop,test):
    testlist = []
    for i in range(len(pop)):
        for j in range(len(test)):
            if (pop[i][0]=='Tinggi'):                   
                if(pop[i][1] == test[j][1]):                  
                    if(pop[i][2] == test[j][2]):                       
                        if(pop[i][3] == test[j][3]):
                            decision = pop[i][4]
                            testlist.append([decision,i])
                        else:
                            decision = 'tidak diketahui'                           
                    else:
                        decision = 'tidak diketahui'                      
                else:
                    decision = 'tidak diketahui'                   
            elif (pop[i][0]=='Normal'):
                if(pop[i][1] == test[j][1]):               
                    if(pop[i][2] == test[j][2]):                     
                        if(pop[i][3] == test[j][3]):
                            decision = pop[i][4]   
                            testlist.append([decision,i])
                        else:
                            decision = 'tidak diketahui'                            
                    else:
                        decision = 'tidak diketahui'                        
                else:
                    decision = 'tidak diketahui'                   
            elif (pop[i][0]=='Rendah'):      
                if(pop[i][1] == test[j][1]):                
                    if(pop[i][2] == test[j][2]):                     
                        if(pop[i][3] == test[j][3]):                           
                            decision = pop[i][4] 
                            testlist.append([decision,i])                                                               
                        else:
                            decision = 'tidak diketahui'                            
                    else:
                        decision = 'tidak diketahui'                       
                else:
                    decision = 'tidak diketahui'
            else:
                decision = 'tidak diketahui' 
        
    return testlist

##MAIN PROGRAM##
data = datalatih() #--import data dari csv ke array
ind = indv() #--buat generate 1 individu
#generate 1 populasi 20 individu
populasi = pop(20) #inisialisasi populasi 20 individu
popcsv=translate(data) #translating data dari csv
fit = fitness(populasi,popcsv)
gen = 0
fitnessGlobal = []
bestGlobal = bestFitness(fit)
while gen <= 20: #independent variable
    save = []
    #create new population
    for x in range (10):
        fit = fitness(populasi,popcsv)
        idx = pilih_parent(fit,populasi)
        p1,p2 = search(populasi,idx)
        anak1,anak2 = crossover(p1,p2)
        hasil_mutasi = mutasi(anak1,anak2)
        save.append(hasil_mutasi[0])
        save.append(hasil_mutasi[1])
    popLokal = save                     
    fitLokal = fitness(popLokal,popcsv)
    bestLokal = bestFitness(fitLokal)   
    
    if  bestLokal[0] > bestGlobal[0]:   
        bestGlobal = bestLokal
        populasi = popLokal             
        fitnessGlobal = fitness(populasi,popcsv) 
    print("generasi : ",gen)
    gen+=1
	
print('list populasi    : ',populasi)
print('fitness baik    : ',fitnessGlobal)
print('fitness terbaik  : ',bestGlobal[0])
print('kromosom terbaik : ',populasi[bestGlobal[1]])

#bandingkan dengan data uji
encoding = encode(populasi)
data_test = datauji()
keputusan = testPop(encoding,data_test)
print(keputusan)

with open("hasil.csv","w+") as csv_hasil:
    csvWriter = csv.writer(csv_hasil,delimiter=',')
    csvWriter.writerows(keputusan)
