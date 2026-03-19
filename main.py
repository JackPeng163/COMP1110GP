from src.file_loader import FileLoader
from src.menu import Menu
from src.network import Network


def main():
    # Load the network from files
    # network: Network = FileLoader().build_network("stops.csv", "routes.csv")

    # Create the menu and run it
    # menu: Menu = Menu(network)
    menu: Menu = Menu(Network())
    menu.run()
    
if __name__ == "__main__":
    main()