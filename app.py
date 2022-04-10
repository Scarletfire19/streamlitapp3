import streamlit as st
from threading import activeCount
import matplotlib.pyplot as plt
import pickle
import umap
import io
import numpy as np
import pandas as pd

page_bg_img = '''
<style>
body {
background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
background-size: cover;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("Machine Learning Genomics App")


dfcurrent=pd.read_csv("G25_Current_DNA.csv")
Xcurrent=dfcurrent.drop(columns=['DNA sample ethnicity and id','DNA sample ethnicity','sample id'])

dfancient=pd.read_csv("G25_Ancient_DNA.csv")
Xancient=dfancient.drop(columns=['DNA sample ethnicity and id','DNA sample ethnicity','sample id'])
#Xcurrent

c=pd.read_csv('clustergmm15.csv')
c=c.drop(columns=['Unnamed: 0'])

frames = [dfcurrent, dfancient]
dfcombined = pd.concat(frames)
Xcombined=dfcombined.drop(columns=['DNA sample ethnicity and id','DNA sample ethnicity','sample id'])
#dfcombined

dfcurrentgroup=dfcurrent.groupby(['DNA sample ethnicity']).mean().reset_index()
Xcurrentgroup=dfcurrentgroup.drop(columns=['DNA sample ethnicity'])

dfadnalineages=pd.read_csv("adnalineages.csv")
dfancientpcadna = pd.merge(dfadnalineages,dfancient)
dfancienthpg=dfancientpcadna.groupby(['Assigned Mutation']).mean().reset_index()


uploaded_file = st.file_uploader("Enter G25 co-ordinates")
if uploaded_file is not None:
     input = pd.read_csv(uploaded_file)
     st.write(input)
      
          
inputhaplogroup = st.text_input("Enter Y Haplogroup")

def euclidean_distance(w, q):
    n = 25 
    return sum([(w[i] - q[i]) ** 2 for i in range(n)]) ** 0.5

p=Xcombined.iloc[735:740]
dfdistances=dfcombined
distances=[]



import numpy as np
p1 = np.zeros((len(p),len(c)))
p2 = np.zeros((len(p),len(c)))

for i in range(len(p)):
  for j in range(len(c)):
     p1[i][j]=euclidean_distance(c.iloc[j],p.iloc[i])
distmat=pd.DataFrame(p1)

for q in range(len(p)):
  tot=distmat.iloc[q].sum()

  for w in range(len(c)):
    p2[q,w]=1-((tot-distmat.iloc[q,w])/tot)

ancestry=pd.DataFrame(p2)
k=0


#dfdistances
#print(dfdistances['DNA sample ethnicity and id'].iloc[:3])

Tools = st.selectbox("Choose your Tool", ["Genetic Distance Tool", "PCA(Principal Component Analysis) Tool","ML Ancestry Tool","Ancient DNA Lineage Tool"]) 

if Tools == "Genetic Distance Tool":

     st.title("Genetic Distance Tool")
     Xinput=input.drop(columns=['DNA sample ethnicity and id'])


     for i in range(len(Xcombined)):
          distances.append(euclidean_distance(Xcombined.iloc[i],Xinput.iloc[3]))
     dfdistances['distances']=distances

     dfdistances=dfdistances.sort_values(by=['distances'])
     st.dataframe(dfdistances)


elif Tools == "ML Ancestry Tool":
     st.title("ML Ancestry Tool")
     st.dataframe(ancestry)


elif Tools == "PCA(Principal Component Analysis) Tool":
     st.title("PCA(Principal Component Analysis) Tool")

     fig, ax = plt.subplots(figsize=(45, 99))
     ax.scatter(dfcurrentgroup['1'], dfcurrentgroup['2'],s = 1)
     ax.scatter(input['1'], input['2'],s = 5)
  #ax.scatter(point['1'],point['2'],s=500)

     for i in range(len(dfcurrentgroup)):
          ax.annotate(dfcurrentgroup['DNA sample ethnicity'][i], (dfcurrentgroup['1'][i], dfcurrentgroup['2'][i]))
     st.pyplot()


elif Tools == "Ancient DNA Lineage Tool":
     ancienthaplogroup = dfancienthpg[dfancienthpg['Assigned Mutation'].str.contains(inputhaplogroup)]     
     st.title("Ancient DNA Lineage Tool")

     fig2, ax2 = plt.subplots(figsize=(30, 24))
     ax2.scatter(dfancienthpg['1'], dfancienthpg['2'],s = 1)
     ax2.scatter(input['1'], input['2'],s = 5)
     ax2.scatter(ancienthaplogroup['1'], ancienthaplogroup['2'],s = 100)

     #ax.scatter(point['1'],point['2'],s=500)
     for i in range(len(dfancienthpg)):
          ax2.annotate(dfancienthpg['Assigned Mutation'][i], (dfancienthpg['1'][i], dfancienthpg['2'][i]))
     st.pyplot()


