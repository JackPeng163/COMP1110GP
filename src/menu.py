from enum import Enum, auto
from network import Network
from journery_generator import Generator
from ranker import Ranker
from filter import Filter

class MenuOption(Enum):
    LIST_STOPS = auto()
    QUERY_JOURNEYS = auto()
    SHOW_SUMMARY = auto()
    LOAD_NETWORK = auto()
    EXIT = auto()

class Menu:
    def __init__(self, network: Network):
        self.network = network
        self.journey_generator = Generator()
        self.journey_ranker = Ranker()
        self.filter = Filter()
        self.running = True

    def _get_user_choice(self) -> MenuOption:
        while True:
            try:
                choice = int(input("Enter your choice (1-6): "))
                options = {
                    1: MenuOption.LIST_STOPS,
                    2: MenuOption.QUERY_JOURNEYS,
                    3: MenuOption.SHOW_SUMMARY,
                    4: MenuOption.LOAD_NETWORK,
                    5: MenuOption.EXIT
                }
                return options[choice]
            except (ValueError, KeyError):
                print("Invalid choice. Please enter a number between 1 and 6.")
    
    def _display_menu(self):
        print("\nMenu:")
        print("1. List all stops")
        print("2. Query journeys")
        print("3. Show summary of a journey")
        print("4. Load network from file")
        print("5. Save network to file")
        print("6. Exit")

    def _list_stops(self):
        print("list stops stub")

    def _query_journeys(self):
        print("query journeys stub")
    
    def _show_summary(self):
        print("show summary stub")

    def _load_network(self):
        print("load network stub")

    def _exit(self):
        print("Exiting the Journey Planner. Goodbye!")
        self.running = False

    def run(self):
        print("Welcome to the Journey Planner!")
        
        while self.running:
            self._display_menu()
            choice = self._get_user_choice()
            
            if choice == MenuOption.LIST_STOPS:
                self._list_stops()
            elif choice == MenuOption.QUERY_JOURNEYS:
                self._query_journeys()
            elif choice == MenuOption.SHOW_SUMMARY:
                self._show_summary()
            elif choice == MenuOption.LOAD_NETWORK:
                self._load_network()
            elif choice == MenuOption.EXIT:
                self._exit()

            