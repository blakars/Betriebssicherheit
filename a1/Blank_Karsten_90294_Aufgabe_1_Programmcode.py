#!/usr/bin/env python
# coding: utf-8

# A1

# A1.1: "Aufgabe1_data"
# 
# a) Kaplan-Meier

# In[2]:


from lifelines import KaplanMeierFitter


# In[3]:


import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[4]:


df=pd.read_excel("Aufgabe1_data.xlsx",index_col="Index")
print(df.head())


# In[5]:


durations = df.sort_values("Duration")


# In[6]:


print(durations.head())


# In[7]:


kmf = KaplanMeierFitter()


# In[8]:


kmf.fit(durations['Duration'])


# In[9]:


kmf.plot()


# b) Maximum Likelihood Estimation (MLE) => finde Lambda für Exponentialfunktion mit lambda = n/Summe(ti)

# In[10]:


#MLE -> lambda = n/Sum(ti)
lam=1000/sum(durations['Duration'])
#x-Achse
t=np.arange(0,1.4,0.001)
#y = Exponentialfunktion
f=np.exp(-lam*t)


# In[11]:


lam


# In[12]:


plt.plot(t,f)


# A1.2: "Aufgabe1_data_cens"

# c) Kaplan-Meier (right-censored data)

# In[15]:


#In Excel zunächst zusätzlich Spalte "kaputt" hinzugefügt um die zensierten Daten (kaputt=0) zu "markern" 
df2=pd.read_excel("Aufgabe1_data_cens.xlsx",index_col="Index")


# In[16]:


print(df2.head())


# In[17]:


durations2=df2.sort_values("Duration")


# In[18]:


print(durations2.head())


# In[19]:


kmf2=KaplanMeierFitter()


# In[20]:


kmf2.fit(durations2['Duration'],durations2['Kaputt'])


# In[21]:


kmf2.plot()


# d) MLE (Vorgehen analog b))

# In[22]:


#MLE -> lambda = n/Sum(ti)
lam2=631/sum(durations2['Duration'])
#x-Achse
t2=np.arange(0,0.25,0.001)
#y = Exponentialfunktion
f2=np.exp(-lam2*t2)


# In[23]:


lam2


# In[24]:


plt.plot(t2,f2)


# In[ ]:




