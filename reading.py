import os
import pandas as pd
import numpy as np

class Reading:
    lines: list
    frequencies: list
    costs: dict

    def __init__(self, file_path="MCDA - AHP (Modelo 1).xlsx"):
        self.lines = pd.read_excel(file_path, sheet_name="Linhas").iloc[:, 0].values.tolist()
        self.frequencies = pd.read_excel(file_path, sheet_name="Frequencias").iloc[:, 0].values.tolist()
        self.technology = pd.read_excel(file_path, sheet_name="Tecnologia").iloc[:, 0].values.tolist()
        self.df_costs = pd.read_excel(file_path, sheet_name="Custos", decimal=",")
        self.df_costs.set_index(["LINHAS", "FREQUENCIAS"], inplace=True)
        self.costs = self.df_costs.to_dict(orient='index')
        self.availability = pd.read_excel(file_path, sheet_name="Disponibilidade").set_index("TECNOLOGIA")['DISPONIBILIDADE'].to_dict()
        # self.data = pd.read_csv(file_path)
        # self.data = self.data.reset_index(drop=True)

if __name__ == "__main__":
    data = Reading()
    print(data.availability)
    for linha in data.lines:
        for frequencia in data.frequencies:
            for tipo_combustivel in data.technology:
                valor_custo = data.costs[linha,frequencia][tipo_combustivel]
                print(f'O custo para {linha}, {frequencia}, {tipo_combustivel} é: {valor_custo}')