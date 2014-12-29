__author__ = 'Soheil'
from localization_methods import LocationRateFactor
from localization_methods import DistanceDisplacement

import os.path


def perform_location_rate_factor():
    path = os.path.dirname(__file__)
    files_dir = path + '/saved_files'
    if not os.path.exists(files_dir):
        os.makedirs(files_dir)
    test_path = files_dir + '/test.txt'
    test = LocationRateFactor.create_problem_with_file(test_path)
    if test:
        print(test.places_factor_points)
        print(test.solve(files_dir + '/text-solution.txt'))


def perform_distance_displacement():
    path = os.path.dirname(__file__)
    files_dir = path + '/saved_files'
    if not os.path.exists(files_dir):
        os.makedirs(files_dir)
    test_path = files_dir + '/test.txt'
    test = DistanceDisplacement.create_problem_with_file(test_path)
    if test:
        print(test.solve(files_dir + '/text-solution.txt'))


def start_program():
    perform_distance_displacement()


if __name__ == "__main__":
    start_program()



