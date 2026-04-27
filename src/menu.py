from enum import Enum, auto
import os
from src.network import Network
from src.journey_generator import Generator
from src.ranker import Ranker, Weight
from src.file_loader import FileLoader

class MenuOption(Enum):
    LIST_STOPS = auto()
    LEAST_TIME_JOURNEY = auto()
    LEAST_COST_JOURNEY = auto()
    BALANCED_JOURNEY = auto()
    LOAD_NETWORK = auto()
    EXIT = auto()

class Menu:
    def __init__(self, network: Network):
        self.network = network
        self.journey_generator = Generator(self.network)
        self.journey_ranker = Ranker()
        self.file_loader = FileLoader()
        self.running = True

    def _get_user_choice(self) -> MenuOption:
        while True:
            try:
                choice = int(input("Enter your choice (1-4): "))
                options = {
                    1: MenuOption.LIST_STOPS,
                    2: MenuOption.BALANCED_JOURNEY,
                    3: MenuOption.LOAD_NETWORK,
                    4: MenuOption.EXIT
                }
                return options[choice]
            except (ValueError, KeyError):
                print("Invalid choice. Please enter a number between 1 and 4.")
    
    def _display_menu(self):
        print("\nMenu:")
        print("1. List all stops")
        print("2. Query journeys")
        print("3. Load network from file")
        print("4. Exit")

    def _list_stops(self):
        print("list stops stub")
        try:
            stops = self.network.get_all_stops()
            for stop in stops:
                print(stop.get_id(), stop.get_name())
        except Exception as e:
            print(f"Error listing stops: {e}")

    def _query_journeys(self):
        start_id = input("Enter the start stop ID: ")
        end_id = input("Enter the end stop ID: ")
        preference = input("Preference (time/cost/transfer/balanced, default balanced): ").strip().lower()

        # clear the screen
        os.system('cls' if os.name == 'nt' else 'clear')

        try:
            print(f"Querying journeys from {start_id}({self.network.get_stop_by_id(start_id).get_name()}) to {end_id}({self.network.get_stop_by_id(end_id).get_name()})")
            journeys = self.journey_generator.generate(self.network.get_stop_by_id(start_id), self.network.get_stop_by_id(end_id))
            if preference == "time":
                weight = Weight.TIME_PREFERENCE
            elif preference == "cost":
                weight = Weight.COST_PREFERENCE
            elif preference in ("transfer", "transfers"):
                weight = Weight.TRANSFERS_PREFERENCE
            else:
                weight = Weight.BALANCED_PREFERENCE
            journeys = self.journey_ranker.rank(journeys, weight)
            print(f"Found {len(journeys)} journeys")
            for journey in journeys:
                print(f"Duration: {journey.total_duration()}, Cost: {journey.total_cost()}, Transfers: {journey.num_transfers()}")
                for route in journey.get_routes():
                    print(f"Route: {route.get_start().get_id()} -> {route.get_end().get_id()}, Duration: {route.get_duration()}, Cost: {route.get_cost()}, Mode: {route.get_mode()}")
                print("--------------------------------")
        except Exception as e:
            print(f"Error querying journeys: {e}")

    def _load_network(self):
        print("load network stub")
        network_file = input("Enter the network name: ")
        try:
            loaded_network = self.file_loader.build_network(
                f"test_cases/{network_file}/stops.csv",
                f"test_cases/{network_file}/routes.csv"
            )
            if loaded_network is None:
                print("Failed to load network.")
                return
            self.network = loaded_network
            # Keep generator in sync with the latest loaded network.
            self.journey_generator = Generator(self.network)
            print("Network loaded successfully.")
        except Exception as e:
            print(f"Error loading network: {e}")

    def _exit(self):
        print("Exiting the Journey Planner. Goodbye!")
        self.running = False

    def run(self):
        # clear the screen
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Welcome to the Journey Planner!")
        
        while self.running:
            self._display_menu()
            choice = self._get_user_choice()

            # clear the screen
            os.system('cls' if os.name == 'nt' else 'clear')
            
            if choice == MenuOption.LIST_STOPS:
                self._list_stops()
            elif choice == MenuOption.BALANCED_JOURNEY:
                self._query_journeys()
            elif choice == MenuOption.LOAD_NETWORK:
                self._load_network()
            elif choice == MenuOption.EXIT:
                self._exit()

            