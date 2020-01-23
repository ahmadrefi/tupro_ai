import random
import numpy
import pandas
import csv

def readCSV():
    data = open("influencers.csv", "r")
    datata = data.readlines()
    
    array = []


    for i in range(1, len(datata)):
      array.append(datata[i].replace('\n','').split(','))
    return array

def fuzzificationFollowers():
  data = readCSV()
  followers = []
  Upper = 70000
  NotUpper = 55000
  Middle1 = 40000
  Middle2 = 50000
  Bottom = 20000
  NotBottom = 45000

  for i in range(len(data)):
    
    x = int(data[i][1])
    #UPPER
    if (x > Upper):
      Up = 1
    elif (x <= NotUpper):
      Up = 0
    else:
      Up = round((x-NotUpper)/(Upper-NotUpper),2)
	  
	  #MIDDLE
    if ((x > Middle1) & (x <= Middle2)):
      Mid = 1
    elif ((x <= Bottom) or (x > Upper)):
      Mid = 0
    else:
      if (x > Middle2):
        Mid = round((Upper-x)/(Upper-Middle2),2)
      elif (x <= Middle1):
        Mid = round((x-Bottom)/(Middle1-Bottom),2)

    #BOTTOM
    if (x <= Bottom):
      Bot = 1
    elif (x > NotBottom):
      Bot = 0
    else:
      Bot = round((NotBottom-x)/(NotBottom-Bottom),2)

     
    
    fol = []
    foll = []
    fol.append(Up)
    fol.append('upper')
    foll.append(fol)
    fol = []
    fol.append(Mid)
    fol.append('middle')
    foll.append(fol)
    fol = []
    fol.append(Bot)
    fol.append('bottom')
    foll.append(fol)
    fol = []
    followers.append(foll)
  return followers

def fuzzificationEngagementRate():
  data = readCSV()
  EngagementRate = []

  High = 7.5
  NotHigh = 5
  Average1 = 4
  Average2 = 5
  Low = 2
  NotLow = 4.5

  for i in range(len(data)):
    # for j in range(len(data[i])):
    x = float(data[i][2])
    #high
    if (x > High):
      Hi = 1
    elif (x <= NotHigh):
      Hi = 0
    else:
      Hi = round((x-NotHigh)/(High-NotHigh),2)
	  
	#avg
    if ((x > Average1) & (x <= Average2)):
      Avg = 1
    elif ((x <= Low) or (x > High)):
      Avg = 0
    else:
      if (x > Average2):
        Avg = round((High-x)/(High-Average2),2)
      elif (x <= Average1):
        Avg = round((x-Low)/(Average1-Low),2)

    #low
    if (x <= Low):
      Lo = 1
    elif (x > NotLow):
      Lo = 0
    else:
      Lo = round((NotLow-x)/(NotLow-Low),2)
    
    rat = []
    rate = []
    rat.append(Hi)   #HIGH     (index0)
    rat.append('high')
    rate.append(rat)
    rat = []
    rat.append(Avg)  #AVERAGE  (index1)
    rat.append('average')
    rate.append(rat)
    rat = []
    rat.append(Lo)   #LOW      (index2)
    rat.append('low')
    rate.append(rat)
    rat = []
    EngagementRate.append(rate)
  
  return EngagementRate

def inferensi():

  followers = fuzzificationFollowers()
  engagementRate = fuzzificationEngagementRate()
  concs = []

  for i in range(len(followers)):
    rules = [[followers[i][0],engagementRate[i][0]],
             [followers[i][0],engagementRate[i][1]],
             [followers[i][0],engagementRate[i][2]],
             [followers[i][1],engagementRate[i][0]],
             [followers[i][1],engagementRate[i][1]],
             [followers[i][1],engagementRate[i][2]],
             [followers[i][2],engagementRate[i][0]],
             [followers[i][2],engagementRate[i][1]],
             [followers[i][2],engagementRate[i][2]]]
    
    Chosen = []
    Considered = []
    Rejected = []
    for z in range(len(rules)):
      if (rules[z][0][1] == 'upper'):
        if (rules[z][1][1] == 'high'):
          Chosen.append(z)
        elif (rules[z][1][1] == 'average'):
          Chosen.append(z)
        elif (rules[z][1][1] == 'low'):
          Considered.append(z)

      elif (rules[z][0][1] == 'middle'):
        if (rules[z][1][1] == 'high'):
          Chosen.append(z)
        elif (rules[z][1][1] == 'average'):
          Considered.append(z)
        elif (rules[z][1][1] == 'low'):
          Rejected.append(z)

      elif (rules[z][0][1] == 'bottom'):
        if (rules[z][1][1] == 'high'):
          Considered.append(z)
        elif (rules[z][1][1] == 'average'):
          Rejected.append(z)
        elif (rules[z][1][1] == 'low'):
          Rejected.append(z)
    
    for x in range(len(rules)):
      minn = min(rules[x])
      rules[x].append(minn)

    ch = max(rules[Chosen[0]][2][0],rules[Chosen[1]][2][0],rules[Chosen[2]][2][0])
    co = max(rules[Considered[0]][2][0],rules[Considered[1]][2][0],rules[Considered[2]][2][0])
    re = max(rules[Rejected[0]][2][0],rules[Rejected[1]][2][0],rules[Rejected[2]][2][0])
    conc = []
    conc.append(ch)
    conc.append(co)
    conc.append(re)
    concs.append(conc)

  return concs

def defuzzification():
  inf = inferensi()
  hasilDef = []

  Chosen = 50
  Considered = 70
  Rejected = 100

  for i in range(len(inf)):
    Z = (100*inf[i][0])+(70*inf[i][1])+(50*inf[i][2])
    hasilDef.append(round(Z/sum(inf[i]),2))

  return hasilDef

def best_influencer():
  defuzzi = defuzzification()
  data = readCSV()
  
  Best = []

  sorted = numpy.argsort(defuzzi)[::-1]
  for i in range(20):
    best = []
    best.append(data[sorted[i]][0])
    Best.append(best)
  for k in range(20):
    Best[k].insert(0,k+1)
  for j in range(20):
    print(j+1,data[sorted[j]])
  return Best

def hasil_keCSV():
  best = best_influencer()
  f = open('chosen.csv', 'w')
  w = csv.writer(f)
  w.writerow(('Urutan','No.Record'))
  w.writerows(best)

hasil_keCSV()
