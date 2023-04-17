import xml.etree.ElementTree as EL
import time
import random
import threading
import Board
import pyfirmata
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys
import serial
BOARDS = {
    'arduino': {
        'digital': tuple(x for x in range(14)),
        'analog': tuple(x for x in range(6)),
        'pwm': (3, 5, 6, 9, 10, 11),
        'use_ports': True,
        'disabled': (0, 1)  # Rx, Tx, Crystal
    }
}

class Iterator(threading.Thread):

    def __init__(self, board):
        super(Iterator, self).__init__()
        self.board = board
        self.daemon = True

    def run(self):
        while 1:
            try:
                while self.board.bytes_available():
                    self.board.iterate()
                time.sleep(0.001)
            except (AttributeError, serial.SerialException, OSError):
              
                break
            except Exception as e:
               
                if getattr(e, "errno", None) == 9:
                    break
                try:
                    if e[0] == 9:
                        break
                except (TypeError, IndexError):
                    pass
                raise
            except (KeyboardInterrupt):
                sys.exit()

class Arduino(Board):

    def __init__(self, *args, **kwargs):
        args = list(args)
        args.append(BOARDS['arduino'])
        super(Arduino, self).__init__(*args, **kwargs)

    def __str__(self):
        return "Arduino {0.name} on {0.sp.port}".format(self)


def ahiu(element,inden='  '):
    queue= [(0,element)]
    while queue:
        level , element = queue.pop(0)
        children = [(level + 1,child) for child in list(element)]
        if children:
            element.text = '\n' + inden * (level+1)
        if queue:
            element.tail = '\n' + inden * queue[0][0]
        else:
            element.tail = '\n' + inden * (level-1)
        queue[0:0]= children



def createXML(Name,ran):
    aa=0
    aaa=0
    tree = EL.Element('root')
    Sensor = EL.SubElement(tree,'Light')
    Sensor1 = EL.SubElement(tree,'TempHumi')
    current_date_and_time = datetime.now()
    # while True:
    
    EL.SubElement(Sensor,'LightSensor',id='Light-sensor',value="{}".format(ran),degree='Voltage')
    # plt.plot(current_date_and_time, ran)
    EL.SubElement(Sensor,'Time', Timearea='VietNam',Timecurrent='{}'.format(current_date_and_time))
    EL.SubElement(Sensor,'brand', model='LM393')

    EL.SubElement(Sensor1,'Temp',id='Temp-sensor',value="{}".format(aa),currency='Celsius')
    EL.SubElement(Sensor1,'Time', Timearea='VietNam',Timecurrent='{}'.format(current_date_and_time))
    EL.SubElement(Sensor1,'brand',model='DHT11')
    
    EL.SubElement(Sensor1,'Humidity',id='Hum-sensor',value="{}".format(aaa),currency='%')
    EL.SubElement(Sensor1,'Time', Timearea='VietNam',Timecurrent='{}'.format(current_date_and_time))
    EL.SubElement(Sensor1,'brand',model='DHT11')

    ahiu(tree)
    tree = EL.ElementTree(tree)
    tree.write('{}.xml'.format(Name),encoding ='utf-8',xml_declaration=False)


def adu(Name):
    board = pyfirmata.Arduino('COM5') 

    it = pyfirmata.util.Iterator(board)
    
    it.start()
    analog_0 = board.get_pin('a:1:i')

    while True:
        sensor=analog_0.read()  
        if (sensor==None):           
            continue
        sensor=sensor*10
        print(sensor*10) 
        createXML(Name,int(sensor*10))
        time.sleep(1.5)


if __name__ == "__main__":
    Name='Hoang'
   
    adu(Name)


