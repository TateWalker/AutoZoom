from os import path
import json
import zoomGUI
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

def main(qApp,data):
	MainWindow = qApp.topLevelWidgets()[0]
	central_widget = MainWindow.centralWidget()
	tab_widget = central_widget.children()[3]
	# print('data = -------------')
	# print(data)
	# print('-------------')
	for i in data.keys():
		
		dl = data[i]['link']
		dc = i
		dd = [0]*7
		[sh, sm] = data[i]['start_time']
		ds = QTime(int(sh),int(sm))
		[eh, em] = data[i]['end_time']
		de = QTime(int(eh),int(em))

		for j in range(len(data[i]['days'])):
			dd[j] = data[i]['days'][j]
		tab = zoomGUI.Tab(dl=dl,ds=ds,de=de,dc=dc,dd=dd)
		tab_widget.addTab(tab,i)
		



if __name__ == '__main__':
	main(MainWindow)