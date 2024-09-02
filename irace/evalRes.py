import os
import numpy as np
from scipy.stats import kurtosis

def read_result_file(file_path, opt):
    if file_path.endswith(".txt"):
        indices_to_pick = [i for i in range(1, 10)]
        values = []
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for index in indices_to_pick:
                try:
                    line_value = float(lines[index - 1].strip())
                    deviation = 100 * abs(opt - line_value) / opt
                    values.append(deviation)
                except IndexError:
                    print(f"Warning: Index {index} is out of range in {file_path}")

        mean_deviation = np.mean(values) if values else float('inf')
        return mean_deviation, values
    else:
        return float('inf'), []

def read_optimal_file(file_path):
    with open(file_path, 'r', encoding='utf-16') as file:
        lines = file.readlines()
        return {line.split(':')[0]: int(line.split(':')[1]) for line in lines}

def process_directory(directory_path, optimal):
    best_mean_deviation = float('inf')
    best_values = []

    for config_folder in os.listdir(directory_path):
        config_path = os.path.join(directory_path, config_folder)
        if os.path.isdir(config_path):
            for file_name in os.listdir(config_path):
                file_path = os.path.join(config_path, file_name)
                file_key = file_name[:-4]
                opt = optimal.get(file_key, 0)
                
                mean_deviation, result = read_result_file(file_path, opt)

                if mean_deviation < best_mean_deviation:
                    best_mean_deviation = mean_deviation
                    best_values = result

    return best_mean_deviation, best_values

directories = ["Subset_1", "Subset_2"]
optimal = read_optimal_file("optimsMMASQAP.txt")

for directory in directories:
    directory_path = os.path.join(os.getcwd(), directory)
    best_mean_deviation, best_values = process_directory(directory_path, optimal)

    if best_values:
        mean = np.mean(best_values)
        std_dev = np.std(best_values)
        mini = min(best_values)
        maxi = max(best_values)
        kurtosi = kurtosis(best_values)
        
        print(f'Best Values for {directory}')
        print(f'Mean: {mean}')
        print(f'Std Dev: {std_dev}')
        print(f'Min: {mini}')
        print(f'Max: {maxi}')
        print(f'Kurtosis: {kurtosi}')
    else:
        print(f'No valid results found for {directory}')
