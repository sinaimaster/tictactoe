from django.shortcuts import render
from django.http import HttpResponse
from keras.models import Model,model_from_json
from keras.models import Sequential
from keras.layers import Activation, Dense, Dropout
from keras import regularizers
import random

def respuesta(modelo,X):
  res = modelo.predict([X])
  res = res.round()[0][0]
  return res

def recibe(request,x0,x1,x2,x3,x4,x5,x6,x7,x8):
  X = [int(x0),int(x1),int(x2),int(x3),int(x4),
       int(x5),int(x6),int(x7),int(x8)]
  from keras.models import Model,model_from_json
  json_file = open("tictactoe/modelo.json","r")
  modelo_cargado_json = json_file.read()
  json_file.close()
  modelo_cargado = model_from_json(modelo_cargado_json)
  modelo_cargado.load_weights("tictactoe/modelo.h5")
  modelo_cargado.compile(loss='mean_squared_error', 
                         optimizer= 'adam',
                         metrics = 'binary_accuracy')
  minimo = 1.0
  soluciones = []
  for i in range(9):
    if(X[i]==2):
      Xcopy = X[:]
      Xcopy[i] = 0
      result = modelo_cargado.predict([Xcopy])
      resultado = float(result[0][0])
      if(resultado<minimo):
        minimo = resultado
        soluciones = []
        soluciones.append(i)
      elif(resultado==minimo):
        soluciones.append(i)

  if(minimo>0.5):
    Xop = X[:]
    for i in range(9):
      if(Xop[i]==0):
        Xop[i] = 1
      elif(Xop[i]==1):
        Xop[i] = 0
    for i in range(9):
      if(Xop[i]==2):
        Xcopy = Xop[:]
        Xcopy[i] = 0
        result = modelo_cargado.predict([Xcopy])
        resultado = float(result[0][0])
        if(resultado<minimo):
          minimo = resultado
          soluciones = []
          soluciones.append(i)
        elif(resultado==minimo):
          soluciones.append(i)
  ######
  if(len(soluciones)==1):
    return HttpResponse(soluciones)
  elif(len(soluciones)>1):
    return HttpResponse(random.choice(soluciones))




    