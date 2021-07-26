import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_excel('IB_Bearing_Contact_Plot_Polar_data.xlsx')

df.drop_duplicates(subset=['Magnitude'], inplace=True)
df['T Radians'] = np.radians(df['T Coord'])

theta = df['T Radians']
r = df['Magnitude']

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

ax.plot(theta, r)

ax.grid(True)

ax.set_theta_zero_location("N")

ax.set_title("Outboard Ball Bearing Contact Force", va='bottom')
plt.show()
