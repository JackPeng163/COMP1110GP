from enum import Enum, auto
import os
from src.network import Network
from src.journey_generator import Generator
from src.ranker import Ranker, Weight
from src.file_loader import FileLoader
from src.dijkstra import dijkstra

class MenuOption(Enum):
    LIST_STOPS = auto()
    LEAST_TIME_JOURNEY = auto()
    LEAST_COST_JOURNEY = auto()
    BALANCED_JOURNEY = auto()
    LOAD_NETWORK = auto()
    EXIT = auto()

options = {
    1: MenuOption.LIST_STOPS,
    2: MenuOption.BALANCED_JOURNEY,
    3: MenuOption.LEAST_TIME_JOURNEY,
    4: MenuOption.LEAST_COST_JOURNEY,
    5: MenuOption.LOAD_NETWORK,
    6: MenuOption.EXIT
}

class Menu:
    def __init__(self, network: Network):
        self.network = network
        self.journey_generator = Generator(self.network)
        self.journey_ranker = Ranker()
        self.file_loader = FileLoader()
        self.running = True

    def _clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def _pause(self):
        input("\nPress enter to continue...")

    def _find_stops_by_name(self, stop_name: str):
        # User-facing input now uses stop names instead of IDs. This helper
        # performs a case-insensitive exact-name match against all loaded stops.
        target = stop_name.strip().lower()
        if not target:
            return []
        return [stop for stop in self.network.get_all_stops() if stop.get_name().strip().lower() == target]

    def _format_stop(self, stop_id: str) -> str:
        # Convert an internal stop ID back into a display-friendly stop name.
        try:
            stop = self.network.get_stop_by_id(stop_id)
            return stop.get_name()
        except Exception:
            return stop_id

    def _prompt_valid_stop_name(self, prompt: str) -> str:
        # Repeatedly ask the user for a stop name until it can be resolved to exactly one stop.
        while True:
            stop_name = input(prompt).strip()
            if not stop_name:
                print("Stop name cannot be empty.")
                continue
            matched = self._find_stops_by_name(stop_name)
            if len(matched) == 1:
                return matched[0].get_id()
            if len(matched) > 1:
                # Ambiguous names are rejected so later queries cannot silently
                # choose the wrong stop.
                print(f"Found {len(matched)} stops named '{stop_name}', please enter a unique stop name.")
                print("Matches:", ", ".join(f"{stop.get_name()}({stop.get_id()})" for stop in matched))
                continue
            print(f"Unknown stop name: {stop_name}. Please try again.")

    def _journey_signature(self, journey) -> tuple:
        # Build a stable tuple representation of a journey so the menu can
        # detect duplicates before printing. This is a presentation-layer
        # safety net in case upstream generation/ranking returns repeated paths.
        return tuple(
            (
                route.get_start().get_id(),
                route.get_end().get_id(),
                route.get_duration(),
                route.get_cost(),
                route.get_mode(),
            )
            for route in journey.get_routes()
        )

    def _get_user_choice(self) -> MenuOption:
        # Keep asking until the user enters a valid menu number. The mapping is
        # centralized here so the rest of the menu loop can work with enum
        # values instead of raw integers.
        while True:
            try:
                choice = int(input("Enter your choice (1-6): ").strip())
                options = {
                    1: MenuOption.LIST_STOPS,
                    2: MenuOption.BALANCED_JOURNEY,
                    3: MenuOption.LEAST_TIME_JOURNEY,
                    4: MenuOption.LEAST_COST_JOURNEY,
                    5: MenuOption.LOAD_NETWORK,
                    6: MenuOption.EXIT
                }
                return options[choice]
            except (ValueError, KeyError):
                print("Invalid choice. Please enter a number between 1 and 6.")
    
    def _display_menu(self):
        # Show a compact status header before the available actions so the user
        # always knows how many stops are currently loaded in memory.
        print("\n=== Journey Planner ===")
        print(f"Loaded stops: {len(self.network.get_all_stops())}")
        print("------------------------")
        print("1. List all stops")
        print("2. Query journeys (ranked)")
        print("3. Fastest path (Dijkstra)")
        print("4. Cheapest path (Dijkstra)")
        print("5. Load network from test_cases")
        print("6. Exit")

    def _list_stops(self):
        # Stop names are sorted alphabetically to make manual lookup easier
        # when the user wants to type a name in a later query.
        try:
            stops = sorted(self.network.get_all_stops(), key=lambda s: s.get_name().lower())
            if not stops:
                print("No stops loaded.")
                return
            print(f"Total stops: {len(stops)}")
            print("------------------------")
            for stop in stops:
                print(stop.get_name())
        except Exception as e:
            print(f"Error listing stops: {e}")
    
    def _get_least_journey(self, choice):
        start_id = self._prompt_valid_stop_name("Enter the start stop name: ")
        end_id = self._prompt_valid_stop_name("Enter the end stop name: ")
        if start_id == end_id:
            print("Start and end are the same stop.")
            return

        self._clear_screen()

        if choice == MenuOption.LEAST_TIME_JOURNEY:
            path, total = dijkstra(start_id, end_id, "time", self.network)
            metric_label = "Total time"
        elif choice == MenuOption.LEAST_COST_JOURNEY:
            path, total = dijkstra(start_id, end_id, "cost", self.network)
            metric_label = "Total cost"
        else:
            return

        if not path:
            print(f"No path found from {self._format_stop(start_id)} to {self._format_stop(end_id)}.")
            return

        named_path = [self._format_stop(stop_id) for stop_id in path] #Convert the path to a list of stop names.

        # Print the path in a readable format.
        print("Route: ", end="")
        for stop in named_path[:-1]:
            print(stop, end=" -> ")
        print(named_path[-1])
        print(f"{metric_label}: {total}")
        print("-" * 40)

    def _query_journeys(self):
        start_id = self._prompt_valid_stop_name("Enter the start stop name: ")
        end_id = self._prompt_valid_stop_name("Enter the end stop name: ")
        if start_id == end_id:
            print("Start and end are the same stop.")
            return

        preference = input("Preference (t: time, c: cost, r: transfer, b: balanced, default balanced): ").strip().lower()

        self._clear_screen()

        try:
            print(f"Querying journeys from {self._format_stop(start_id)} to {self._format_stop(end_id)}")
            journeys = self.journey_generator.generate(self.network.get_stop_by_id(start_id), self.network.get_stop_by_id(end_id))

            # Translate the user's preference string into a predefined weight
            # profile used by the ranking module.
            if preference in ("t", "time"):
                weight = Weight.TIME_PREFERENCE
            elif preference in ("c", "cost"):
                weight = Weight.COST_PREFERENCE
            elif preference in ("r", "transfer", "transfers"):
                weight = Weight.TRANSFERS_PREFERENC
            else:
                weight = Weight.BALANCED_PREFERENCE
            
            # Rank the journeys using the selected weight profile.
            journeys = self.journey_ranker.rank(journeys, weight)

            # If no journeys are found, print a message and return.
            if not journeys:
                print("No journeys found.")
                return

            # Print the journeys in a readable format.
            print(f"Found {len(journeys)} journeys")
            for index, journey in enumerate(journeys, start=1):
                print(f"\n[{index}] Duration: {journey.total_duration()}, Cost: {journey.total_cost()}, Transfers: {journey.num_transfers()}")
                for route in journey.get_routes():
                    # Each route is printed as one leg in the overall journey.
                    print(
                        f"  - {route.get_start().get_name()} -> {route.get_end().get_name()} ",
                        f"(Duration: {route.get_duration()}, Cost: {route.get_cost()}, Mode: {route.get_mode()})"
                    )
                print("-" * 40)
        except Exception as e:
            print(f"Error querying journeys: {e}")

    def _load_network(self):
        # Load one of the prepared CSV datasets from the test_cases folder.
        # After loading, recreate the generator so future journey queries use
        # the new network instead of the old cached reference.
        network_file = input("Enter network id under test_cases (e.g. 1, 2): ").strip()
            
        try:
            loaded_network = self.file_loader.build_network(
                f"test_cases/{network_file}/stops.csv",
                f"test_cases/{network_file}/routes.csv"
            )

            if loaded_network is None:
                print("Failed to load network.")
                return
            
            # Update the network and generator to use the new network.
            self.network = loaded_network
            self.journey_generator = Generator(self.network)

            # Print the number of stops in the new network.
            print(f"Network loaded successfully. Stops: {len(self.network.get_all_stops())}")
        except Exception as e:
            print(f"Error loading network: {e}")

    def _exit(self):
        # Mark the main loop as finished so run() can exit cleanly.
        print("Exiting the Journey Planner. Goodbye!")
        self.running = False

    def run(self):
        # Main event loop for the CLI application. Each iteration shows the
        # menu, dispatches one action, and pauses before the next iteration.
        self._clear_screen()
        print("Welcome to the Journey Planner!")
        self._pause()
        
        while self.running:
            self._clear_screen()

            self._display_menu()
            choice = self._get_user_choice()

            self._clear_screen()
            
            if choice == MenuOption.LIST_STOPS:
                self._list_stops()
            elif choice == MenuOption.BALANCED_JOURNEY:
                self._query_journeys()
            elif choice == MenuOption.LEAST_TIME_JOURNEY:
                self._get_least_journey(MenuOption.LEAST_TIME_JOURNEY)
            elif choice == MenuOption.LEAST_COST_JOURNEY:
                self._get_least_journey(MenuOption.LEAST_COST_JOURNEY)
            elif choice == MenuOption.LOAD_NETWORK:
                self._load_network()
            elif choice == MenuOption.EXIT:
                self._exit()

            if self.running:
                self._pause()