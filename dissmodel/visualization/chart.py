

from dissmodel.core import Model

import matplotlib.pyplot as plt
import streamlit as st
import inspect

def Plot(plot_type, label, color):
    def decorator(func):
        # Adiciona informações de plotagem ao método
        func._plot_info = {
            "plot_type": plot_type,
            "label": label,
            "color": color,
            "data": [],  # Lista para armazenar os valores atribuídos
        }

        def wrapper(self, value):
            # Adiciona os metadados ao _plot_metadata da instância, caso ainda não existam
            if not hasattr(self.env, "_plot_metadata"):
                self.env._plot_metadata = {}

            if func.__name__ not in self.env._plot_metadata:
                self.env._plot_metadata[func._plot_info["label"]] = func._plot_info

            # Atualiza a lista de dados no _plot_metadata
            self.env._plot_metadata[func._plot_info["label"]]["data"].append(value)

            # Executa a função original
            return func(self, value)

        return wrapper
    return decorator

class Chart (Model):



    def setup(self, pause=True):
        

        """
        Configura o plotter.
        
        Args:
            variables (dict): Dicionário onde as chaves são os rótulos (labels) das variáveis 
                              e os valores são as listas do ambiente a serem monitoradas.
            interval (int): Intervalo de tempo (em unidades de tempo Salabim) para atualizar o gráfico.
        """
        self.interval = 1
        self.time_points = []  # Lista para armazenar os tempos
      

                        # Configurar o gráfico
        self.fig, self.ax = plt.subplots()        
        self.ax.set_xlabel("Tempo")
        self.ax.set_title("Histórico das Variáveis")
        
        self.pause = pause

    def execute(self):
      
            #clear_output(wait=True)  # Limpa a saída do notebook para exibir apenas o gráfico atualizado
            plt.sca(self.ax)  # Define o 'ax' como o eixo atua
            #
            self.time_points.append(self.env.now())  # Armazena o tempo atual

            for label, data_list in self.env._plot_metadata.items():
              self.ax.plot(data_list["data"], label=label, color=data_list["color"])

            if self.env.now() == 0:
                plt.legend()


            # Ajusta os limites do gráfico
            self.ax.relim()
            self.ax.autoscale_view()

            # Redesenha o gráfico
            plt.draw()
            if self.pause:
                plt.pause(0.1)
                if self.env.now() == self.env.end_time:
                    plt.show() # não fecha a janela
