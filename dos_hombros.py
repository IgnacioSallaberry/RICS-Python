# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 20:25:06 2019
@author: Ignacio Sallaberry
"""

import numpy as np
import matplotlib.pyplot as plt


#==============================================================================
#                                  Parametros globales iniciales
#==============================================================================   
box_size = 512
roi = 128
tp = 1e-6             #seg    
tl = box_size * tp    #seg
dr = 0.05             # delta r = pixel size =  micrometros
w0 = 0.5              #radio de la PSF  = micrometros    
wz = 1.5              #alto de la PSF desde el centro  = micrometros
a = w0/wz
gamma = 0.3536
num_de_partic = 4000
v_eff=(w0**2)*wz*((np.pi)**(1.5))
concentracion = num_de_partic/((box_size*dr)**3)
N = v_eff * concentracion
print(f'N en PSF ={N}')
G_0 = 1/N
print(f'G0={G_0}')


        #gamma factor de la 3DG
#N = 0.05         #Numero total de particulas en la PSF





At= 0                 #Amplitud de triplete
#t_triplet = .16       #segundos    #Tiempo caracteristico de triplete 

Ab= 0.9                #Amplitud de binding
#t_binding= .16        #segundos     #Tiempo caracteristico de binding

D=90
#print('D = {}'.format(D))
t_diff = w0**2/(4*D)    
print(f'tiempo de difusion = {t_diff} segundos')
#D=90
#D=[0.1,1,10,100,1000]
#D=np.arange(1,1050,200)   #micrones^2/seg

#==============================================================================
#                                Inicializo tau = valores del eje x
#==============================================================================    
## acá exploro distintas formas para ver como puedo hacer para tener más valores al ppio (ie: tau=0) y no tantos al final

#tau = np.arange(1e-6,1,1e-6)
#tau1 = np.logspace(1e-6, 1, num=50)
#plt.figure()
#plt.plot(tau, label='tau')
#plt.plot(tau1, label='tau1')
#plt.legend()
#plt.show()



#defino tau
#tau = np.logspace(0, 8, num=1000)/10000000
#tau = np.geomspace(tp, tp*box_size**2)
#tau = np.linspace(1,1e7,num=1000000)/1000000
tau = np.geomspace(1e-6,10,num=1000)

#==============================================================================
#                                Defino tiempo de difusión de acuerdo a los parametros de arriba
#==============================================================================    

#t_diff = w0**2/(4*D) 
#print(f'tiempo de difusion = {t_diff} segundos')

#==============================================================================
#                                Inicializo T= t_diff / t_bind 
#==============================================================================    
#T=[0.01,1,100]
#T=[0.01,1,30]
#T=[30]
T=[1]

t_binding=0.5



#==============================================================================
#                                Creo el ruido para añadirle a las curvas
#==============================================================================    

#Ruido = np.random.randn(len(tau),1)
i=0
ruido1 = []
ruido2 = []
ruido3 = []

#ruido = np.arange()
for i in tau:

    ruido1.append(np.random.uniform(0,1)-np.random.uniform(0,1))
    ruido2.append(np.random.uniform(0,1)-np.random.uniform(0,1))
    ruido3.append(np.random.uniform(0,1)-np.random.uniform(0,1))

numero_random_para_modular=np.arange(0,1,0.001)
modulacion1=[]
modulacion2=[]
modulacion3=[]

i=0
#while i<len(ruido1):
#    modulacion1.append(np.exp(-numero_random_para_modular[i])*ruido1[i])
#    modulacion2.append(np.exp(-numero_random_para_modular[i])*ruido2[i])
#    modulacion3.append(np.exp(-numero_random_para_modular[i])*ruido3[i])
#    i+=1

s=1000
plt.figure()
plt.plot(modulacion1, label='modulacion')
#plt.plot(tau1, label='tau1')
plt.legend()
plt.show()

#def sigmoid(x, derivative=False):
#    sigm = 1. / (1. + np.exp(-x))
#

#==============================================================================
#                                Tipografía de los gráficos
#==============================================================================    
SMALL_SIZE = 28
MEDIUM_SIZE = 36
BIGGER_SIZE = 39
plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
#==============================================================================
#                                  
#                           GRAFICOS
#
#==============================================================================    
fig = plt.figure()    
plt.close('all') # amtes de graficar, cierro todos las figuras que estén abiertas
    
guardar_imagenes = False    

for t in T:
    if t==T[0]:
        ruido=ruido1
        modulacion = modulacion1
    elif t==T[1]:
        ruido=ruido2
        modulacion = modulacion2
    else:
        ruido=ruido3
        modulacion = modulacion3
    
#    t_binding=t_diff/t
#    print(f'tiempo de binding= {t_binding} segundos')
    t_triplet=t_diff/t
#    if d==D[-1]:
#        guardar_imagenes = True
#    else:
#        guardar_imagenes = False
#    
    i=1   #con este indice voy a numerar las imagenes. Lo pongo dado que si quiero modificar el codigo tengo que modificar el plt.figure(3) por ejemplo.En cambio con esto es automático
#
#==============================================================================
#                                  G(tau)
#==============================================================================    

    ###termino de difusion
    G_diff = (gamma/N)*( 1 + tau/t_diff)**(-1) * ( 1 + tau*(a**2)/(t_diff))**(-1/2)
    ###termino de triplete
    G_triplet = 1+ At * np.exp(-tau/t_triplet)
    ###termino de binding
    G_bind =Ab * np.exp(-tau/t_binding)


    ####   Esto es para usar la version de la tesis de Laura.
    G_diff_moño = G_diff + 1
    G_bind_moño = G_bind + 1
    G_triplet_moño = G_triplet + 1


    ###Normalización de factores de la ACF    
    G_diff_norm = G_diff_moño/max(G_diff_moño)
    G_triplet_norm = G_triplet_moño/max(G_triplet_moño)
    G_bind_norm = G_bind_moño/max(G_bind_moño)  


    ###-------- TOTAL ACF ------    
    Gtotal_moño = G_diff_moño * G_bind_moño 
    Gtotal = Gtotal_moño - 1
    Gtotal_normalizada = Gtotal/max(Gtotal)
    Gtotal_moño2 = G_diff * G_bind + G_diff + G_bind +1


#==============================================================================
#                                Ruido para las señales
#==============================================================================    
#    Gtotal_ruido = Gtotal  + modulacion
#    Gtotal_ruido_normalizada = Gtotal_ruido/max(Gtotal_ruido)
#    
   
#    ###  Grafico solo termino difussivo
#    plt.figure(i)
##    plt.plot((dr*x), G_norm,'-.',label=f'D={d}',linewidth=1)
#    plt.semilogx(tau, G_diff_norm,'-.',label=f'T={t} \n tb={t_binding}, td={t_diff}')
#    plt.legend()
#    plt.xlabel(r'$\tau$ - ($s$)',fontsize=14)
#    plt.ylabel(r'Gdiff($\tau$)',fontsize=14)
##    plt.title('H-line G diff  \n tp = {}$\mu$  - pix size = {} $\mu$- box size = {} pix'.format(tp*1e6,dr,box_size),fontsize=18)
#    plt.title('H-line G diff')
#    plt.show()
#    plt.tight_layout() #hace que no me corte los márgenes
#    
#    if guardar_imagenes:
#        plt.savefig('C:\\Users\\LEC\\Desktop')
#    i+=1
#
#
#    ###  Grafico solo termino triplete
#    plt.figure(i)
##    plt.plot((dr*x), G_norm,'-.',label=f'D={d}',linewidth=1)
#    plt.semilogx(tau, G_triplet_norm,'-.',label=f'T={t} \n tb={t_binding}, td={t_diff}')
#    plt.legend()
#    plt.xlabel(r'pixel shift $\xi$ - $\mu m$',fontsize=14)
#    plt.ylabel(r'Gtriplet($\xi$)',fontsize=14)
##    plt.title('H-line G diff  \n tp = {}$\mu$  - pix size = {} $\mu$- box size = {} pix'.format(tp*1e6,dr,box_size),fontsize=18)
#    plt.title('H-line G triplete')
#    plt.show()
#    plt.tight_layout() #hace que no me corte los márgenes
#    
#    if guardar_imagenes:
#        plt.savefig('C:\\Users\\LEC\\Desktop')
#    i+=1
#    
#    
#    ###  Grafico solo termino binding
#    plt.figure(i)
##    plt.plot((dr*x), G_norm,'-.',label=f'D={d}',linewidth=1)
#    plt.semilogx(tau, G_bind_norm,'-.',label=f'T={t} \n tb={t_binding}, td={t_diff}')
#    plt.legend()
#    plt.xlabel(r'$\tau$ - ($s$)',fontsize=14)
#    plt.ylabel(r'Gbind($\tau$)',fontsize=14)
##    plt.title('H-line G diff  \n tp = {}$\mu$  - pix size = {} $\mu$- box size = {} pix'.format(tp*1e6,dr,box_size),fontsize=18)
#    plt.title('H-line G binding')
#    plt.show()
#    plt.tight_layout() #hace que no me corte los márgenes
#    
#    if guardar_imagenes:
#        plt.savefig('C:\\Users\\LEC\\Desktop')
#    i+=1
#    
    ###  Grafico funcion de correlación  total  CON RUIDO
#    plt.figure(i)
#    plt.semilogx(tau, Gtotal_ruido_normalizada,'-',label=f'T={t} \n tb={t_binding}, td={t_diff}')
#    plt.legend()
#    plt.xlabel(r'$\tau$ - ($s$)')
#    plt.ylabel(r'Gtot($\tau$)')
#    plt.title('tp = {}$\mu$s  - pix size = {} $\mu$m- box size = {} pix'.format(tp*1e6,dr,box_size),fontsize=18)
##    plt.title('H-line  G total')
#    plt.show()
#    plt.tight_layout() #hace que no me corte los márgenes
#    
#    if guardar_imagenes:
#        plt.savefig('C:\\Users\\LEC\\Desktop')
#    i+=1
    
#    ##  Grafico funcion de correlación  total
#    plt.figure(i)
##    plt.plot((dr*x), Gtotal_normalizada,'-.',label=f'D={d}',linewidth=1)
#    plt.semilogx(tau, Gtotal,'-',label='T={} \n t bind={} \n t dif={}'.format(t,'%.2E' % t_binding,'%.2E' % t_diff))
#    plt.legend()
#    plt.xlabel(r'$\tau$ - ($s$)')
#    plt.ylabel(r'Gtot($\tau$)')
#    plt.title('tp = {}$\mu$s - pix size = {} $\mu$m \n box size = {} pix - D={}'.format(tp*1e6,dr,box_size,D))
##    plt.title('H-line  G total')
#    plt.show()
#    plt.tight_layout() #hace que no me corte los márgenes
#    
#    if guardar_imagenes:
#        plt.savefig('C:\\Users\\LEC\\Desktop')
#    i+=1
  
  
    ##  Grafico funcion de correlación  total
    plt.figure(i)
#    plt.plot((dr*x), Gtotal_normalizada,'-.',label=f'D={d}',linewidth=1)
#    plt.semilogx(tau, Gtotal_normalizada,'-',label='Gtot \n tb={} \n td={}'.format('%.2E' % t_binding,'%.2E' % t_diff),linewidth=2)
    plt.semilogx(tau, Gtotal_normalizada,'-',label='difusión y asoc-disoc',linewidth=3)
    plt.semilogx(tau, G_diff/max(G_diff),'-',label='difusión',linewidth=3)
    plt.semilogx(tau, G_bind/max(G_bind),'-',label=r'asoc-disoc',linewidth=3)
    plt.legend()
    plt.xlabel(r'$\tau$ - ($s$)')
    plt.ylabel(r'G($\tau$)')
    plt.tight_layout() #hace que no me corte los márgenes
    plt.tick_params(which='minor', length=2, width=1.5)
    plt.tick_params(which='major', length=4, width=2)
    plt.show()    
    if guardar_imagenes:
        plt.savefig('C:\\Users\\LEC\\Desktop')
    i+=1


#    ##  Grafico funcion de correlación  total
#    plt.figure(i)
##    plt.plot((dr*x), Gtotal_normalizada,'-.',label=f'D={d}',linewidth=1)
#    plt.semilogx(tau, Gtotal_normalizada,'-',label=f'T={t} \n tb={t_binding}, td={t_diff}')
#    plt.semilogx(tau, G_diff_moño/max(G_bind_moño),'k')
#    plt.legend()
#    plt.xlabel(r'$\tau$ - ($s$)')
#    plt.ylabel(r'Gtot($\tau$)')
#    plt.title('G$(\tau) \_total$ \n tp = {}$\mu$  - pix size = {} $\mu$- box size = {} pix'.format(tp*1e6,dr,box_size),fontsize=18)
##    plt.title('H-line  G total')
#    plt.show()
#    plt.tight_layout() #hace que no me corte los márgenes
#    
#    if guardar_imagenes:
#        plt.savefig('C:\\Users\\LEC\\Desktop')
#    i+=1

#    
#    ###  Grafico funcion de correlación  total MOÑO
#    plt.figure(i)
##    plt.plot((dr*x), Gtotal_normalizada,'-.',label=f'D={d}',linewidth=1)
#    plt.semilogx(tau, Gtotal_moño,'-',label=f'T={t} \n tb={t_binding}, td={t_diff}')
#    plt.legend()
#    plt.xlabel(r'$\tau$ - ($s$)',fontsize=14)
#    plt.ylabel(r'Gtot MOÑO  ($\tau$)',fontsize=14)
#    plt.title('H-line G total \n tp = {}$\mu$  - pix size = {} $\mu$- box size = {} pix'.format(tp*1e6,dr,box_size),fontsize=18)
#    plt.title('H-line  G total')
#    plt.show()
#    plt.tight_layout() #hace que no me corte los márgenes
#    
#    if guardar_imagenes:
#        plt.savefig('C:\\Users\\LEC\\Desktop')
#    i+=1
#        
#    
#  ###  Grafico funcion de correlación  total MOÑO 2
#    plt.figure(i)
##    plt.plot((dr*x), Gtotal_normalizada,'-.',label=f'D={d}',linewidth=1)
#    plt.semilogx(tau, Gtotal_moño2,'-',label=f'T={t} \n tb={t_binding}, td={t_diff}')
#    plt.legend()
#    plt.xlabel(r'$\tau$ - ($s$)',fontsize=14)
#    plt.ylabel(r'Gtot MOÑO2 ($\tau$)',fontsize=14)
#    plt.title('H-line G total \n tp = {}$\mu$  - pix size = {} $\mu$- box size = {} pix'.format(tp*1e6,dr,box_size),fontsize=18)
#    plt.title('H-line  G total')
#    plt.show()
#    plt.tight_layout() #hace que no me corte los márgenes
#    
#    if guardar_imagenes:
#        plt.savefig('C:\\Users\\LEC\\Desktop')
#    i+=1
#            
#    
#    j=0
#    while Gtotal_normalizada[j]>0.60:
#        j+=1
#    plt.semilogx(tau[j],Gtotal_normalizada[j], 'r*', label=f'{round(tau[j],5)}$s$')      ###---> para graficar punto donde cae a la mitad la curva de correlación
###    plt.semilogx(dr*x[j],0, 'g*', label=f'dist para Gtotal/2 = {round(dr*x[j],5)}$\mu m$')      ###---> para graficar punto en x donde cae a la mitad la curva de correlación
#    plt.text(tau[j], Gtotal_normalizada[j], r'$\tau$ = {} $s$'.format(round(tau[j],3)), bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=1'))
#    plt.arrow(tau[j], Gtotal_normalizada[j], 0, -Gtotal_normalizada[j])
#
#
#    t+=1


#    j=0
#    while tau[j]<t_diff:
#        j+=1
#    plt.semilogx(tau[j],Gtotal_normalizada[j], 'm*')#, label=r'$\t_dif$ = {}$s$'.format(round(tau[j],5)))      ###---> para graficar punto donde cae a la mitad la curva de correlación
#    j=0
#    while tau[j]<t_binding:
#        j+=1
#    plt.semilogx(tau[j],Gtotal_normalizada[j], 'c*')#, label=r'$\t_bind$ = {}$s$'.format(round(tau[j],5)))#, label=f'{round(tau[j],5)}$s$')      ###---> para graficar punto donde cae a la mitad la curva de correlación
    ##    plt.semilogx(dr*x[j],0, 'g*', label=f'dist para Gtotal/2 = {round(dr*x[j],5)}$\mu m$')      ###---> para graficar punto en x donde cae a la mitad la curva de correlación
#    plt.text(tau[j], Gtotal_normalizada[j], r'$\tau$ = {} $s$'.format(round(tau[j],3)), bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=1'))
#    plt.arrow(tau[j], Gtotal_normalizada[j], 0, -Gtotal_normalizada[j])
    t+=1



#plt.semilogx(tau, G_diff_moño - 1,'k')    #Grafico la correlacion de DIFUSION 
###busco el valor de tau para el t_diff
#j=0
#while tau[j]<t_diff:
#    j+=1
#plt.semilogx(tau[j],G_diff_moño[j]-1, 'ko')   #marco el t_diff
#plt.axvline(x=t_diff)  #linea que marca el valor del t_diff
#plt.show()




#plt.figure(i)
##    plt.plot((dr*x), Gtotal_normalizada,'-.',label=f'D={d}',linewidth=1)
#plt.semilogx(tau, Gtotal_normalizada  + ruido,'-',label=f'T={t} \n tb={t_binding}, td={t_diff}')
#plt.legend()
#plt.xlabel(r'$\tau$ - ($s$)',fontsize=14)
#plt.ylabel(r'Gtot($\tau$)',fontsize=14)
#plt.title('G$(\tau) \_total$ \n tp = {}$\mu$  - pix size = {} $\mu$- box size = {} pix'.format(tp*1e6,dr,box_size),fontsize=18)
##    plt.title('H-line  G total')
#plt.show()
#plt.tight_layout() #hace que no me corte los márgenes