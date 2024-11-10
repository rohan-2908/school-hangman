import efx
from sides import LoginSetup
from game import Menu
from data import setup

def main():				#THE ORIGIN
	input(efx.Printer(efx.intro,delay=0.0005))

	setup()

	LoginSetup()

	Menu()

main()
