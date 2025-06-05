from dissmodel.core import Model
from dissmodel.visualization import track_plot

# utils.py
import math

# Constantes físicas
SIGMA = 5.67e-08         # Constante de Stefan-Boltzmann (W/m²·K⁴)
SOLAR_FLUX = 3668        # Fluxo solar médio usado no modelo Daisyworld (W/m²)
HEAT_TRANSFER_COEF = 2.06e9  # Coeficiente de transferência térmica (K⁴)

def daisy_growth_rate(tempK):
    """Calcula a taxa de crescimento das margaridas em função da temperatura (em Kelvin)."""
    gr = 0.0
    temp = tempK - 273.0
    if 5.0 < temp < 40.0:
        gr = 1 - 0.003265 * (22.5 - temp) ** 2
    return gr

def calc_temp(luminosity, albedo):
    """Calcula a temperatura média planetária em Kelvin."""
    return ((luminosity * SOLAR_FLUX * (1 - albedo)) / (4 * SIGMA)) ** 0.25

def temp_near_daisy(planet_temp, planet_albedo, daisy_albedo):
    """Calcula a temperatura local próxima a uma área com margaridas."""
    return (HEAT_TRANSFER_COEF * (planet_albedo - daisy_albedo) + planet_temp ** 4) ** 0.25

def growth_reduction(base_rate, empty_area):
    """Reduz a taxa de crescimento com base na área disponível (vazia)."""
    return base_rate * empty_area


@track_plot("WhiteArea", "lightgray")
@track_plot("BlackArea", "black")
@track_plot("EmptyArea", "saddlebrown")
@track_plot("PlanetAlbedo", "blue")
@track_plot("AveTemp", "red")
@track_plot("DaisyArea", "green")
class Daisyworld(Model):
    def __init__(self,
                 sun_luminosity=0.7,
                 planet_area=1.0,
                 white_area=0.40,
                 black_area=0.273,
                 empty_area=0.327,
                 white_albedo=0.75,
                 black_albedo=0.25,
                 soil_albedo=0.5,
                 decay_rate=0.3):
        super().__init__()
        self.sun_luminosity = sun_luminosity

        self.planet_area = planet_area
        self.white_area = white_area
        self.black_area = black_area
        self.empty_area = empty_area

        self.white_albedo = white_albedo
        self.black_albedo = black_albedo
        self.soil_albedo = soil_albedo
        self.decay_rate = decay_rate

        # observáveis
        self.planet_albedo = self.compute_planet_albedo()
        self.ave_temp = calc_temp(self.sun_luminosity, self.planet_albedo)
        self.daisy_area = self.white_area + self.black_area

    def compute_planet_albedo(self):
        return (self.white_area * self.white_albedo +
                self.black_area * self.black_albedo +
                self.empty_area * self.soil_albedo)

    def execute(self):
        """Executa um passo de simulação."""
        print ("passo")
        self.planet_albedo = self.compute_planet_albedo()
        self.ave_temp = calc_temp(self.sun_luminosity, self.planet_albedo)

        # White daisies
        temp_white = temp_near_daisy(self.ave_temp, self.planet_albedo, self.white_albedo)
        ind_white_growth = daisy_growth_rate(temp_white)
        white_growth = growth_reduction(ind_white_growth, self.empty_area)
        self.white_area += self.white_area * (white_growth - self.decay_rate)

        # Black daisies
        temp_black = temp_near_daisy(self.ave_temp, self.planet_albedo, self.black_albedo)
        ind_black_growth = daisy_growth_rate(temp_black)
        black_growth = growth_reduction(ind_black_growth, self.empty_area)
        self.black_area += self.black_area * (black_growth - self.decay_rate)

        # Update empty area and total daisy area
        self.empty_area = self.planet_area - (self.white_area + self.black_area)
        self.daisy_area = self.white_area + self.black_area
