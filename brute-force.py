import numpy as np
import pandas as pd
import itertools
from reading import Reading


class BruteForce:
    def __init__(self, file_path="MCDA - AHP (Modelo 1).xlsx"):
        self.data = Reading(file_path)

    def get_all_combinations(self):
        
        combinations = list(itertools.product(itertools.permutations(self.data.lines), 
                                                 itertools.combinations_with_replacement(self.data.frequencies, 3), 
                                                 itertools.permutations(self.data.technology)))
        return combinations


    def build_df_combinations(self):
        combinations = self.get_all_combinations()
        df_combinations = pd.DataFrame(combinations, columns=["LINHAS", "FREQUENCIAS", "TECNOLOGIA"])
        df_combinations["CUSTO"] = df_combinations.apply(lambda row: self.calculate_cost(row), axis=1)
        df_combinations["VIAVEL"] = df_combinations.apply(lambda row: self.is_feasible(row), axis=1)
        return df_combinations

    def is_feasible(self, row):
        for r in zip(row["LINHAS"], row["FREQUENCIAS"], row["TECNOLOGIA"]):
            l = r[0]
            f = r[1]
            t = r[2]
            if f > self.data.availability[t]:
                return False
        return True

    def calculate_cost(self, row):
        c = 0
        for r in zip(row["LINHAS"], row["FREQUENCIAS"], row["TECNOLOGIA"]):
            l = r[0]
            f = r[1]
            t = r[2]
            c += self.data.costs[l,f][t]
            if t == 'GAS NATURAL' and f == 1 and l == 'Linha 1':
                print(f'CUSTO: {self.data.costs[l,f][t]}')
        return c




if __name__ == "__main__":
    brute_force = BruteForce()
    df = brute_force.build_df_combinations()
    df.sort_values(by=["CUSTO"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.to_excel("combinations.xlsx")