
import matplotlib.pyplot as plt


from dissmodel.core import Model



class Map(Model):
    def setup(self, gdf, plot_params, pause=True, plot_area=None):
        self.fig, self.ax = plt.subplots(1, 1, figsize=(10, 6))
        self.plot_params = plot_params
        self.pause = pause
        self.gdf = gdf
        self.plot_area = plot_area

    def update(self, year, gdf):
        self.ax.clear()
        self.gdf.plot(ax=self.ax, **self.plot_params)
        self.ax.set_title(f'Map for {year}')
        plt.draw()

        if self.plot_area:
            self.plot_area.pyplot(self.fig)  # Streamlit
        elif self.pause:
            plt.pause(0.01)
            if self.env.now() == self.env.end_time:
                plt.show()  # Modo interativo local

    def execute(self):
        year = self.env.now()
        self.update(year, self.gdf)

