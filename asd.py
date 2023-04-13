import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
import random
fig, ax = plt.subplots()
x = []
y = []
ln, = ax.plot(x, y, '-')
 
def update(frame):
    global x, y
    ax.clear()
    current_date_and_time = datetime.now()
    a=random.randint(0,50)
    x.append(current_date_and_time)
    y.append(a)
 
    ln, = ax.plot(x, y, '-')
 
animation = FuncAnimation(fig, update, interval=2000, repeat = False)
plt.show()