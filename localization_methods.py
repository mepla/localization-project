__author__ = 'Soheil'
from internal_classes import Factor
from internal_classes import Place
import math


def spaces(count):
    if count < 1:
        return ' '
    space_string = ''
    for i in range(0, count-1):
        space_string += ' '
    return space_string


def distance_of_2_points(x1, y1, x2, y2):
    distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    distance = round(float(distance), 2)
    return distance

class LocationRateFactor:
    factors = []
    places = []
    places_factor_points = []
    output_separator = '          '

    def __init__(self, factors, places, places_factors_point):
        self.factors = factors
        self.places = places
        self.places_factor_points = places_factors_point

    def write_solution_to_path(self, solution_matrix, path):
        try:
            lines_to_write = []

            first_line = self.output_separator
            for place in self.places:
                space_needed = len(self.output_separator) - len(place.name)
                first_line += '{}{}'.format(place.name, spaces(space_needed))
            lines_to_write.append(first_line + '\n')

            for i in range(0, len(self.factors)):
                space_needed = len(self.output_separator) - len(self.factors[i].name)
                line = '{}{}'.format(self.factors[i].name, spaces(space_needed))
                for j in range(0, len(self.places)):
                    item_string = str(solution_matrix[i][j])
                    space_needed = len(self.output_separator) - len(item_string)
                    line += '{}{}'.format(item_string, spaces(space_needed))

                lines_to_write.append(line + '\n')

            last_line = 'Total'
            last_line = '{}{}'.format(last_line, spaces(len(self.output_separator) - len(last_line)))
            for t in solution_matrix[len(solution_matrix)-1]:
                space_needed = len(self.output_separator) - len(str(t))
                last_line += '{}{}'.format(str(t), spaces(space_needed))
            lines_to_write.append(last_line + '\n')

            file = open(path, 'w')
            file.writelines(lines_to_write)

        except Exception as exc:
            print('Error writing to file: {}\n{}-->{}'.format(path, type(exc), exc))

    def solve(self, write_to_path=None):
        weighed_points = list(self.places_factor_points)
        i = 0
        j = 0
        try:
            for factor_row in self.places_factor_points:
                for place_point in factor_row:
                    factor = self.factors[i]
                    weighed_points[i][j] = round(factor.weight * float(place_point), 2)
                    j += 1
                i += 1
                j = 0
        except Exception as exc:
            print('Failed solving LocationRateFactor: {}-->{}\n{} {}'.format(type(exc), exc, i, j))

        i = 0
        places_result = {}
        places_result_array = []
        for place in self.places:
            sum_for_place = 0.0
            for result_row in weighed_points:
                sum_for_place += result_row[i]

            places_result['{}'.format(place.name)] = round(sum_for_place, 2)
            places_result_array.append(round(sum_for_place, 2))
            i += 1
        weighed_points.append(places_result_array)

        if write_to_path:
            self.write_solution_to_path(weighed_points, write_to_path)

        return weighed_points

    @staticmethod
    def create_problem_with_file(path):
        try:
            file = open(path, 'r')
            lines = file.read().splitlines()
        except Exception as exc:
            print('Failed reading from file: {}\n{}-->{}'.format(path, type(exc), exc))
            return

        factors = []
        places = []
        places_factors_points = []
        try:
            first_line = lines[0]
            first_line_parts = first_line.split()
            first_line_parts.pop(0)
            for first_line_part in first_line_parts:
                place = Place(first_line_part, first_line_part)
                places.append(place)

            lines.pop(0)

            for line in lines:
                parts = line.split()

                factor_name = parts[0]
                parts.pop(0)
                factor_weight = float(parts[0])
                parts.pop(0)

                factor = Factor(factor_name, factor_weight, factor_name)
                factors.append(factor)

                places_factors_points.append(parts)

            lrf = LocationRateFactor(factors, places, places_factors_points)
            return lrf

        except Exception as exc:
            print('Your file should be in proper format: {}-->{}'.format(type(exc), exc))
            return None


class DistanceDisplacement:
    existing_places = []
    existing_places_travel_times = []
    suggested_places = []

    def __init__(self, existing, travel_times, suggested):
        self.existing_places = existing
        self.existing_places_travel_times = travel_times
        self.suggested_places = suggested

    def write_solution_to_path(self, suggested_places_distances, path):
        lines_to_write = []

        i = j = 0
        for suggested_place in self.suggested_places:
            single_distances = suggested_places_distances[i]
            line = '{}: '.format(suggested_place.name)
            for distance in single_distances:
                weighed_distance = float(self.existing_places_travel_times[j]) * distance
                weighed_distance = round(float(weighed_distance))
                line += '{}*{} + '.format(self.existing_places_travel_times[j], distance,  weighed_distance)
                j += 1
            i += 1
            j = 0
            assert isinstance(line, str)
            line = line[:line.rfind('+')-1]
            total_distance = eval(line[line.find(':')+1:])
            total_distance = round(total_distance, 2)
            line += ' = {}'.format(total_distance)
            print(line)
            lines_to_write.append(line + '\n')

        file = open(path, 'w')
        file.writelines(lines_to_write)

    def solve(self, write_to_path=None):
        suggested_places_distances = []
        for suggested_place in self.suggested_places:
            distances = []
            for existing_place in self.existing_places:
                single_distance = distance_of_2_points(existing_place.x, existing_place.y, suggested_place.x, suggested_place.y)
                single_distance = round(single_distance, 2)
                distances.append(single_distance)
            suggested_places_distances.append(distances)

        if write_to_path:
            self.write_solution_to_path(suggested_places_distances, write_to_path)

    @staticmethod
    def create_problem_with_file(path):
        try:
            file = open(path, 'r')
            lines = file.read().splitlines()
        except Exception as exc:
            print('Failed reading from file: {}\n{}-->{}'.format(path, type(exc), exc))
            return

        lines.pop(0)

        try:
            existing = []
            suggested = []
            travel_times = []
            for line in lines:
                parts = line.split()
                place_name = parts[0]
                place_x = float(parts[1])
                place_y = float(parts[2])

                place = Place(place_name)
                place.x = place_x
                place.y = place_y

                if len(parts) > 3:
                    travel_time = parts[3]
                    travel_times.append(travel_time)
                    existing.append(place)
                else:
                    suggested.append(place)

            dd = DistanceDisplacement(existing, travel_times, suggested)
            return dd

        except Exception as exc:
            print('Your file should be in proper format: {}-->{}'.format(type(exc), exc))
            return None