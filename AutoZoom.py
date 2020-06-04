from autozoom.src import zoomGUI
import subprocess

def main():
	try:
		MyOut = subprocess.Popen(['defaults','write','com.google.Chrome','ExternalProtocolDialogShowAlwaysOpenCheckbox','-bool','true'])
		# subprocess.run(['defaults','write','com.google.Chrome','ExternalProtocolDialogShowAlwaysOpenCheckbox','-bool','true'])
	finally:
		zoomGUI.main()
if __name__ == '__main__':
	main()