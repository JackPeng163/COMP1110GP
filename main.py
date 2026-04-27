from src.file_loader import FileLoader
from src.menu import Menu
from src.network import Network


def main():
    # Load default test network so the app can run immediately.
    network = FileLoader().build_network(
        "test_cases/1/stops.csv",
        "test_cases/1/routes.csv"
    )
    if network is None:
        print("Failed to load default network, starting with an empty network.")
        network = Network()

    menu: Menu = Menu(network)
    menu.run()
    
if __name__ == "__main__":
    main()