import webbrowser
from typing import  List
from Model.City import City
import logging
import folium

class Tour:
    """
    Class which represent the tour (hamiltonian cycle) solving a TSP.
    """
    def __init__(self, tour_name: str = "Tour", verbose: bool = False):
        """
        Constructor of the tour, it will start empty if no instance is loaded.
        :param tour_name: The name of the tour
        :param verbose: Verbose mode
        """
        logging.info("Tour: Tour {tour_name} created")
        if verbose:
            print(f"Tour {tour_name} created")
        self.tour_cities= []
        self.tour_name=tour_name

    def __repr__(self):
        return str(f"Tour: {self.tour_cities}")

    def append(self, new_city: City, verbose: bool = False) -> bool:
        """
        Add at the end of the tour a new city
        :param verbose: Verbose mode
        :param new_city: The city that we want to add
        :return: True if the appending is successful, otherwise False
        """
        logging.info("Tour: Adding a new city to the tour")
        logging.info("Tour: Checking if the new city is valid..")
        if verbose:
            print("Adding a new city to the tour.")
            print("Checking if the new city is valid..")

        if type(new_city) is not City:
            raise TypeError("The city that you want to add is not a City object")

        if new_city in self.tour_cities:
            raise ValueError("The city that you want to add is already in the tour")

        if verbose:
            print("Ok")
            logging.info("Tour: Ok.")

        self.tour_cities.append(new_city)
        return True

    def add_after_city(self, new_city: City, target_city: City, verbose: bool = False) -> bool:
        """
        Add a city after a target city already in the tour
        :param new_city: The new city which we want to add
        :param target_city: The city that will be used as target
        :param verbose: Verbose mode
        :return: True if the appending is successful, otherwise False
        """
        logging.info(f"Tour: Adding a new city to the tour, after a target one.")
        logging.info(f"Tour: Checking if the target city is valid..")
        if verbose:
            logging.info(f"Tour: Adding a new city to the tour, after a target one.")
            print("Checking if the target city is valid..")
        if type(target_city) is not City:
            raise TypeError("The city target is not a City object")

        if target_city not in self.tour_cities:
            raise ValueError("The city target is not in the tour")

        logging.info("Tour: Checking if the new city is valid..")
        if verbose:
            print("Adding a new city to the tour.")
            print("Checking if the new city is valid..")

        if type(new_city) is not City:
            raise TypeError("The city that you want to add is not a City object")

        if new_city in self.tour_cities:
            raise ValueError("The city that you want to add is already in the tour")

        if verbose:
            print("Ok")
            logging.info("Tour: Ok.")

        self.tour_cities.insert(self.tour_cities.index(target_city)+1,new_city)
        return True

    def length(self, unit_of_measurement: str = "km") -> float:
        """
        Compute the length of the tour, in *unit_of_meausurement*
        :return: The length of the tour
        """
        _length = 0.0
        prev_city = self.tour_cities[0]

        for c in self.tour_cities[1:]:
            _length += prev_city.distance(c)
            prev_city = c
        # add the last arc back to the starting city
        _length += prev_city.distance(self.tour_cities[0],unit_of_measure=unit_of_measurement)
        return _length

    def is_valid(self, instance: List[City]) -> bool:
        """
        Check if a tour is valid
        :param instance: The instance with all the city on which we want create a tour
        :return: True if the statement holds, otherwise False
        """
        if (len(self.tour_cities) == len(instance)) and all(city in instance for city in self.tour_cities):
            return True
        return False

    def plot(self):
        _complete_tour = self.tour_cities.copy()
        _complete_tour.append(self.tour_cities[0])
        m = folium.Map(location=[_complete_tour[0].location.latitude,_complete_tour[0].location.longitude])
        folium.Marker([_complete_tour[0].location.latitude, _complete_tour[0].location.longitude],
                      icon=folium.Icon(color="red", prefix='fa', icon="car")).add_to(m)
        for city in _complete_tour[1:-1]:
            folium.Marker([city.location.latitude,city.location.longitude],
                      icon=folium.Icon(color="green",prefix='fa',icon="info-circle")).add_to(m)
        folium.PolyLine([(city.location.latitude,city.location.longitude) for city in _complete_tour],color="red"
                            ,weight=2).add_to(m)
        m.save(f"{self.tour_name}.html")
        webbrowser.open(f"{self.tour_name}.html", new=2)

    def position(self, position_number):
        """Return the city in the requested position"""
        if position_number < 0 or position_number >= len(self.tour_cities):
            raise Exception(f"ERROR: Accessing outside the tour ({position_number})")
        return self.tour_cities[position_number]

    def remove(self, position_number):
        """Remove a city from the tour based on the position"""
        del self.tour_cities[position_number]