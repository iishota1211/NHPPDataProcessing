import matplotlib.pyplot as plt
import numpy as np
from utility import *

data = load_json_data(os.path.join("filtered_data", "timed_data", "Type1", "day_scale_30_32","version_30.json"))
x=[]
y=[]
for key,i in enumerate(data):
    x.append(i)
    y.append(key)

plt.plot(x, y, label='Data',linestyle='',marker='o', color='blue')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Multiple Lines Plot')
plt.legend()
plt.show()