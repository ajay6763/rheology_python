import numpy as np
import sys,os,time
from datetime import date
import math

strain_rate = 1e-15 # strain rate
rheology_law = 'peridotite_dry' # rheology see CM Rheology Explorer or materials function below
model_name='Judith' # directory where output will be saved
outdir = str(model_name) 
inputfile='2_CSEMv2_XYZVs_TRho_Pr1.dat' # input file : input file name i.e. output file from the conversions
outputfile='Judith.txt'  #output rheology file name which will be saved in output folder.
# loading data
data = np.loadtxt(inputfile,delimiter=',',comments='#')
path = os.getcwd()
isExist = os.path.exists(outdir)
if not isExist:
        print('\n###########################################')
        print('Output directory does not exist. Making one for you.')
        print('\n###########################################')
        os.makedirs(outdir)
else:
        print('\n###########################################') 
        print('Output directory exists. It will be overwritted.')
        print('\n###########################################')



def materials():
    """
    Contains a list of materials used for strength computation with exodus
    module. Available properties are

    Meta properties
    ---------------
    name : str
        Name of the material
    altname : str
        Alternative name
    source : str
        Data source
    via : str
        Where this data has been used

    Byerlee's law
    -------------
    f_f_e : float
        Friction coefficient for extension
    f_f_c : float
        Friction coefficient for compression
    f_p : float
        Pore fluid factor
    rho_b : float
        Bulkd density of the rock / kg/m3

    Dislocation creep
    -----------------
    a_p : float
        Preexponential scaling factor / Pa^(-n)/s
    n : float
        Power law exponent
    q_p : float
        Activation energy / J/mol

    Diffusion creep
    ---------------
    a_f : float
        Preexponential scaling factor / 1/Pa/s
    q_f : float
        Activation energy / J/mol
    a : float
        Grain size / m
    m : float
        Grain size exponent

    Dorn's law creep
    ----------------
    sigma_d : float
        Dorn's law stress / Pa
    q_d : float
        Dorn's law activation energy / J/mol
    a_d : float
        Dorn's law strain rate
    """
    """
    Template

    r.append(dict(name='',
                    altname='',
                    source='Ranalli and Murpy (1987)',
                    via='',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=2.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=,  # Bulk density
                    # Dislocation creep
                    a_p=,   # Preexponential scaling factor / Pa^(-n)/s
                    n=,         # Power law exponent
                    q_p=,   # Activation energy J/mol
                    # Diffusion creep
                    a_f=None,      # Preexp. scaling factor / 1/Pa/s
                    q_f=None,      # Activation energy / J/mol
                    a=None,        # Grain size / m
                    m=None,        # Grain size exponent
                    # Dorn's law properties
                    sigma_d=None, # Dorn's law stress
                    q_d=None,     # Dorn's law activation energy
                    a_d=None))    # Dorn's law strain rate / 1/s
    """
    def AGPa(A,n):
        A = float(A)
        n = float(n)
        return A*10.0**(-1.0*n*9.0)

    r = list()
    r.append(dict(name='olivine',
                    altname='',
                    source='Ranalli and Murpy (1987)',
                    source_disloc='Ranalli and Murpy (1987)',
                    source_diff=None,
                    source_dorn=None,
                    via='',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=2.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=3300.0,  # Bulk density
                    # Dislocation creep
                    a_p=AGPa(4e15,3.0),   # Preexponential scaling factor / Pa^(-n)/s
                    n=3.0,         # Power law exponent
                    q_p=540.0e3))  # Activation energy J/mol
    r.append(dict(name='olivine_wet',
                    altname='',
                    source='Jackson (2002)',
                    source_disloc='Jackson (2002)',
                    source_diff=None,
                    source_dorn=None,
                    via='',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=2.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=3300.0,  # Bulk density
                    # Dislocation creep
                    a_p=5.5e-25,   # Preexponential scaling factor / Pa^(-n)/s
                    n=4.48,         # Power law exponent
                    q_p=498.0e3))  # Activation energy J/mol
    r.append(dict(name='diabase',
                    altname='',
                    source='Ranalli and Murpy (1987)',
                    source_disloc='Ranalli and Murpy (1987)',
                    source_diff=None,
                    source_dorn=None,
                    via='',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=2.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=2950.0,  # Bulk density
                    # Dislocation creep
                    a_p=AGPa(3.2e6,3.4),   # Preexponential scaling factor / Pa^(-n)/s
                    n=3.4,         # Power law exponent
                    q_p=260.0e3))  # Activation energy J/mol
    r.append(dict(name='quartz_diorite',
                    altname='',
                    source='Ranalli and Murpy (1987)',
                    source_disloc='Ranalli and Murpy (1987)',
                    source_diff=None,
                    source_dorn=None,
                    via='',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=2.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=2900.0,  # Bulk density
                    # Dislocation creep
                    a_p=AGPa(2e4,2.4),   # Preexponential scaling factor / Pa^(-n)/s
                    n=2.4,         # Power law exponent
                    q_p=219.0e3))  # Activation energy J/mol
    r.append(dict(name='anorthosite',
                    altname='',
                    source='Ranalli and Murpy (1987)',
                    source_disloc='Ranalli and Murpy (1987)',
                    source_diff=None,
                    source_dorn=None,
                    via='',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=2.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=2800.0,  # Bulk density
                    # Dislocation creep
                    a_p=AGPa(1.3e6,3.2),   # Preexponential scaling factor / Pa^(-n)/s
                    n=3.2,         # Power law exponent
                    q_p=238.0e3))  # Activation energy J/mol
    r.append(dict(name='albite_rock',
                    altname='',
                    source='Ranalli and Murpy (1987)',
                    source_disloc='Ranalli and Murpy (1987)',
                    source_diff=None,
                    source_dorn=None,
                    via='',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=2.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=2600.0,  # Bulk density
                    # Dislocation creep
                    a_p=AGPa(1.3e6,3.9),   # Preexponential scaling factor / Pa^(-n)/s
                    n=3.9,         # Power law exponent
                    q_p=234.0e3))  # Activation energy J/mol
    r.append(dict(name='quartzite_wet',
                    altname='',
                    source='Ranalli and Murpy (1987)',
                    source_disloc='Ranalli and Murpy (1987)',
                    source_diff=None,
                    source_dorn=None,
                    via='',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=2.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=2650.0,  # Bulk density
                    # Dislocation creep
                    a_p=AGPa(2e3, 2.3),   # Preexponential scaling factor / Pa^(-n)/s
                    n=2.3,         # Power law exponent
                    q_p=154.0e3))  # Activation energy J/mol
    r.append(dict(name='quartzite',
                    altname='',
                    source='Ranalli and Murpy (1987)',
                    source_disloc='Ranalli and Murpy (1987)',
                    source_diff=None,
                    source_dorn=None,
                    via='',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=2.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=2650.0,  # Bulk density
                    # Dislocation creep
                    a_p=AGPa(100,2.4),   # Preexponential scaling factor / Pa^(-n)/s
                    n=2.4,         # Power law exponent
                    q_p=156.0e3))  # Activation energy J/mol
    r.append(dict(name='granite_wet',
                    altname='',
                    source='Ranalli and Murpy (1987)',
                    source_disloc='Ranalli and Murpy (1987)',
                    source_diff=None,
                    source_dorn=None,
                    via='',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=2.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=2650.0,  # Bulk density
                    # Dislocation creep
                    a_p=AGPa(100,2.4),   # Preexponential scaling factor / Pa^(-n)/s
                    n=2.4,         # Power law exponent
                    q_p=137.0e3))  # Activation energy J/mol
    r.append(dict(name='granite',
                    altname='',
                    source='Ranalli and Murpy (1987)',
                    source_disloc='Ranalli and Murpy (1987)',
                    source_diff=None,
                    source_dorn=None,
                    via='Ranalli and Murpy (1987)',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=2.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=2650.0,  # Bulk density
                    # Dislocation creep
                    a_p=AGPa(5,3.2),     # Preexponential scaling factor / Pa^(-n)/s
                    n=3.2,         # Power law exponent
                    q_p=123.0e3))  # Activation energy J/mol
    r.append(dict(name='olivine_dry',
                    altname='Mantle',
                    source='Goetze and Evans (1979)',
                    source_disloc='Goetze and Evans (1979)',
                    source_diff=None,
                    source_dorn=None,
                    via='Sippel et al. (2016)',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=2.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=3300.0,  # Bulk density
                    # Dislocation creep
                    a_p=7.0e-14,   # Preexponential scaling factor / Pa^(-n)/s
                    n=3.0,         # Power law exponent
                    q_p=510.0e3,   # Activation energy J/mol
                    # Dorn's law properties
                    sigma_d=8.5e9, # Dorn's law stress
                    q_d=535e3,     # Dorn's law activation energy
                    a_d=5.7e11))   # Dorn's law strain rate / 1/s
    r.append(dict(name='mafic_granulite',
                    altname='Mafic granulites',
                    source='Wilks and Carter (1990)',
                    source_disloc='Wilks and Carter (1990)',
                    source_diff=None,
                    source_dorn=None,
                    via='Sippel et al. (2016)',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=2.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=3050.0,  # Bulk density
                    # Dislocation creep
                    a_p=8.83e-22,  # Preexponential scaling factor / Pa^(-n)/s
                    n=4.2,         # Power law exponent
                    q_p=445.0e3))  # Activation energy J/mol
    r.append(dict(name='diabase_dry',
                    altname='Gabbroid rocks',
                    source='Carter and Tsenn (1987)',
                    source_disloc='Carter and Tsenn (1987)',
                    source_diff=None,
                    source_dorn=None,
                    via='Sippel et al. (2016)',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=2.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=2920.0,  # Bulk density
                    # Dislocation creep
                    a_p=6.31e-20,  # Preexponential scaling factor / Pa^(-n)/s
                    n=3.05,        # Power law exponent
                    q_p=276.0e3))  # Activation energy J/mol
    r.append(dict(name='granite_dry',
                    altname='Meta-sedimentary rocks',
                    source='Carter and Tsenn (1987)',
                    source_disloc='Carter and Tsenn (1987)',
                    source_diff=None,
                    source_dorn=None,
                    via='Sippel et al. (2016)',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=2.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=2750.0,  # Bulk density
                    # Dislocation creep
                    a_p=3.16e-26,  # Preexponential scaling factor / Pa^(-n)/s
                    n=3.3,         # Power law exponent
                    q_p=186e3))    # Activation energy J/mol
    r.append(dict(name='quartzite_dry',
                    altname='Sediments',
                    source='Burov et al. (1998)',
                    source_disloc='Burov et al. (1998)',
                    source_diff=None,
                    source_dorn=None,
                    via='Sippel et al. (2016), Carter and Tsenn (1987)',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=2.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=2600,    # Bulk density
                    # Dislocation creep
                    a_p=5.0e-12,   # Preexponential scaling factor / Pa^(-n)/s
                    n=3.0,         # Power law exponent
                    q_p=190e3))    # Activation energy J/mol
    r.append(dict(name='diorite_dry',
                    altname='Meta-igneous rocks',
                    source='Burov et al. (1998)',
                    source_disloc='Burov et al. (1998)',
                    source_diff=None,
                    source_dorn=None,
                    via='Sippel et al. (2016)',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=2.0,     # Friction coefficient compression
                    f_p=0.35,      # Pore fluid factor
                    rho_b=2800,  # Bulk density
                    # Dislocation creep
                    a_p=5.2e-18,     # Preexponential scaling factor / Pa^(-n)/s
                    n=2.4,         # Power law exponent
                    q_p=219e3))    # Activation energy J/mol
    r.append(dict(name='peridotite_dry',
                    altname='Mantle lithosphere of slab and shield, \
                             dry_olivine',
                    source='Hirth and Kohlstedt (1996), Kameyama et al. (1999)',
                    source_disloc='Hirth and Kohlstedt (1996)',
                    source_diff='Kameyama et al. (1999)',
                    source_dorn='Kameyama et al. (1999)',
                    via='Sobolev et al. (2006)',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=2.0,     # Friction coefficient compression
                    f_p=0.35,         # Pore fluid factor
                    rho_b=3280.0,     # Bulk density
                    # Dislocation creep
                    a_p=5.011e-17,    # Preexponential scaling factor, -16.3
                    n=3.5,            # Power law exponent
                    q_p=535e3,        # Activation energy
                    # Diffusion creep
                    a_f=2.570e-11,    # Preexp. scaling factor / 1/Pa/s, -10.59
                    q_f=300e3,        # Activation energy / J/mol
                    a=0.1e-3,         # Grain size / m
                    m=2.5,            # Grain size exponent
                    # Dorn's law
                    sigma_d=8.5e9,    # Dorn's law stress / Pa
                    q_d=535e3,        # Dorn's law activation energy / J/mol
                    a_d=5.754e11))     # Dorn's law strain rate
    r.append(dict(name='peridotite_dry_SA',
                    altname='Mantle lithosphere of South America, not shield',
                    source='Hirth and Kohlstedt (1996), Kameyama et al. (1999)',
                    source_disloc='Hirth and Kohlstedt (1996)',
                    source_diff='Kameyama et al. (1999)',
                    source_dorn='Kameyama et al. (1999)',
                    via='Sobolev et al. (2006)',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=2.0,     # Friction coefficient compression
                    f_p=0.35,         # Pore fluid factor
                    rho_b=3280.0,     # Bulk density
                    # Dislocation creep
                    a_p=5.002e-15,      # Preexponential scaling factor
                    n=3.5,            # Power law exponent
                    q_p=515e3,        # Activation energy
                    # Diffusion creep
                    a_f=2.570e-11,     # Preexp. scaling factor / 1/Pa/s
                    q_f=300e3,        # Activation energy / J/mol
                    a=0.1e-3,         # Grain size / m
                    m=2.5,            # Grain size exponent
                    # Dorn's law
                    sigma_d=8.5e9,    # Dorn's law stress / Pa
                    q_d=535e3,        # Dorn's law activation energy / J/mol
                    a_d=5.754e11))     # Dorn's law strain rate
    r.append(dict(name='peridotite_dry_asthenosphere',
    # Difference to peridotite_dry_SA is density
                    altname='Mantle asthenosphere',
                    source='Hirth and Kohlstedt (1996), Kameyama et al. (1999)',
                    source_disloc='Hirth and Kohlstedt (1996)',
                    source_diff='Kameyama et al. (1999)',
                    source_dorn='Kameyama et al. (1999)',
                    via='Sobolev et al. (2006)',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=2.0,     # Friction coefficient compression
                    f_p=0.35,         # Pore fluid factor
                    rho_b=3300.0,     # Bulk density
                    # Dislocation creep
                    a_p=5.012e-15,      # Preexponential scaling factor
                    n=3.5,            # Power law exponent
                    q_p=515e3,        # Activation energy
                    # Diffusion creep
                    a_f=2.570e-11,     # Preexp. scaling factor / 1/Pa/s
                    q_f=300e3,        # Activation energy / J/mol
                    a=0.1e-3,         # Grain size / m
                    m=2.5,            # Grain size exponent
                    # Dorn's law
                    sigma_d=8.5e9,    # Dorn's law stress / Pa
                    q_d=535e3,        # Dorn's law activation energy / J/mol
                    a_d=5.754e11))     # Dorn's law strain rate
    r.append(dict(name='quartzite_wet_2650',
                    altname='sediments',
                    source='Gleason and Tullis (1995)',
                    source_disloc='Gleason and Tullis (1995)',
                    source_diff=None,
                    source_dorn=None,
                    via='Sobolev et al. (2006)',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=2.0,     # Friction coefficient compression
                    f_p=0.35,         # Pore fluid factor
                    rho_b=2650.0,     # Bulk density
                    # Dislocation creep
                    a_p=1e-28,        # Preexponential scaling factor
                    n=4.0,            # Power law exponent
                    q_p=223e3))       # Activation energy
    r.append(dict(name='quartzite_wet_2700',
                    altname='Uppermost crust continent',
                    source='Gleason and Tullis (1995)',
                    source_disloc='Gleason and Tullis (1995)',
                    source_diff=None,
                    source_dorn=None,
                    via='Sobolev et al. (2006)',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=2.0,     # Friction coefficient compression
                    f_p=0.35,         # Pore fluid factor
                    rho_b=2700.0,     # Bulk density
                    # Dislocation creep
                    a_p=1e-28,        # Preexponential scaling factor
                    n=4.0,            # Power law exponent
                    q_p=223e3))       # Activation energy
    r.append(dict(name='quartzite_wet_weak',
                    altname='Upper crust continent',
                    source='Gleason and Tullis (1995)',
                    source_disloc='Gleason and Tullis (1995)',
                    source_diff=None,
                    source_dorn=None,
                    via='Sobolev et al. (2006)',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=2.0,     # Friction coefficient compression
                    f_p=0.35,         # Pore fluid factor
                    rho_b=2800.0,     # Bulk density
                    # Dislocation creep
                    a_p=1e-27,        # Preexponential scaling factor
                    n=4.0,            # Power law exponent
                    q_p=223e3))       # Activation energy
    r.append(dict(name='plagioclase_wet',
    # Note: this one doesn't fit with the model parameters given in drezina.inp!
                    altname='Granulite, mafic crust continent',
                    source='Rybacki and Dresen (2000)',
                    source_disloc='Rybacki and Dresen (2000)',
                    source_diff=None,
                    source_dorn=None,
                    via='Sobolev et al. (2006)',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=2.0,     # Friction coefficient compression
                    f_p=0.35,         # Pore fluid factor
                    rho_b=2950.0,     # Bulk density
                    # Dislocation creep
                    a_p=3.981e-16,      # Preexponential scaling factor
                    n=3.0,            # Power law exponent
                    q_p=356e3))       # Activation energy
    r.append(dict(name='granulite_dry',
                    altname='Pikwetonian granulite',
                    source='UNKNOWN',
                    source_disloc='UNKNOWN',
                    source_diff=None,
                    source_dorn=None,
                    via='Sobolev et al. (2006) Drezina.inp',
                    # Byerlee's law
                    f_f_e=0.75,    # Friction coefficient extension
                    f_f_c=2.0,     # Friction coefficient compression
                    f_p=0.35,         # Pore fluid factor
                    rho_b=2950,       # Bulk density
                    # Dislocation creep
                    a_p=3.2e-21,      # Preexponential scaling factor
                    n=4.2,            # Power law exponent
                    q_p=445.0e3))     # Activation energy
    return r
def effective_viscosity(material,temp,strain_rate):
    """
    Compute the effective viscosity. Requires the material
    properties pre-exponetial scaling factor (a_p), Power law exponent (n),
    activation energy (q_p), and strain rate

    Parameters
    ----------
    material : dict
        Dictionary with the material properties in SI units. The
        required keys are 'a_p', 'n', and 'q_p' 
    temp : float
        temperature
    strain_rate : float
        'compression' or 'extension'

    Returns
    -------
        effec_viscosity : float
    """
    R = 8.314472 # m2kg/s2/K/mol
    a_p = material['a_p']
    n = material['n']
    q_p = material['q_p']
    f_1 = (2**(1-n)/n)/(3**(1+n)/2*n)*a_p**(-1/n)*strain_rate**(1/n-1)
    return f_1*math.exp(q_p/(n*R*temp))


def sigma_byerlee(material, z, mode):
    """
    Compute the byerlee differential stress. Requires the material
    properties friction coefficient (f_f), pore fluid factor (f_p) and
    the bulk density (rho_b).

    Parameters
    ----------
    material : dict
        Dictionary with the material properties in SI units. The
        required keys are 'f_f_e', 'f_f_c', 'f_p' and 'rho_b'
    z : float
        Depth below surface in m
    mode : str
        'compression' or 'extension'

    Returns
    -------
        sigma_d : float
    """
    if mode == 'compression':
        f_f = material['f_f_c']
    elif mode == 'extension':
        f_f = material['f_f_e']
    else:
        raise ValueError('Invalid parameter for mode:', mode)
    f_p = material['f_p']
    rho_b = material['rho_b']
    g = 9.81  # m/s2
    return f_f*rho_b*g*z*(1.0 - f_p)

def sigma_diffusion(material, temp, strain_rate):
    """
    Computes differential stress for diffusion creept at specified
    temperature and strain rate. Material properties require grain size 'd',
    grain size exponent 'm', preexponential scaling factor for diffusion
    creep 'a_f', and activation energy 'q_f'.

    For diffusion creep, n=1.

    Parameters
    ----------
    material : dict
        Dictionary with the material properties in SI units. Required
        keys are 'd', 'm', 'a_f', 'q_f'
    temp : float
        Temperature in Kelvin
    strain_rate : float
        Reference strain rate in 1/s

    Returns
    -------
        sigma_diffusion : float
    """
    R = 8.314472 #m2kg/s2/K/mol
    d = material['d']
    m = material['m']
    a_f = material['a_f']
    q_f = material['q_f']
    if a_f is None:
        return np.nan
    else:
        return d**m*strain_rate/a_f*np.exp(q_f/R/temp)

def sigma_dislocation(material, temp, strain_rate):
    """
    Compute differential stress envelope for dislocation creep at
    certain temeprature and strain rate. Requires preexponential scaling
    factor 'a_p', power law exponent 'n' and activation energy 'q_p'.

    Parameters
    ----------
    material : dict
        Dictionary with the material properties in SI units. Required
        keys are 'a_p', 'n' and 'q_p'
    temp : float
        Temperature in Kelvin
    strain_rate : float
        Reference strain rate in 1/s

    Returns
    -------
        sigma_d : float
    """
    R = 8.314472 # m2kg/s2/K/mol
    a_p = material['a_p']
    n = material['n']
    q_p = material['q_p']
    return (strain_rate/a_p)**(1.0/n)*np.exp(q_p/n/R/temp)

def sigma_dorn(material, temp, strain_rate):
    """
    Compute differential stress for solid state creep with Dorn's law.
    Requires Dorn's law stress 'sigma_d', Dorn's law activation energy
    'q_d' and Dorn's law strain rate 'A_p'.

    Dorn's creep is a special case of Peierl's creep with q=2

    sigma_delta = sigma_d*(1-(-R*T/Q*ln(strain_rate/A_d))^(1/q))

    Parameters
    ----------
    material : dict
        Dictionary with the material properties in SI units. Required
        keys are 'sigma_d', 'q_d' and 'A_p'
    temp : float
        Temperature in Kelvin
    strain_rate : float
        Reference strain rate in 1/s

    Returns
    -------
        sigma_d : float
    """
    R = 8.314472 # m2kg/s2/K/mol
    sigma_d = material['sigma_d']
    q_d = material['q_d']
    a_d = material['a_d']
    if q_d == 0 or a_d == 0:
        return np.nan
    dorn = sigma_d*(1.0 - np.sqrt(-1.0*R*temp/q_d*np.log(strain_rate/a_d)))
    if dorn < 0.0:
        dorn = 0
    return dorn

def sigma_d(material, z, temp, strain_rate=None,
            compute=None, mode=None):
    """
    Computes differential stress for a material at given depth, temperature
    and strain rate. Returns the minimum of Byerlee's law, dislocation creep
    or dorn's creep.

    Parametersq
    ----------
    material : dict
        Dict containing material properties required by sigma_byerlee() and
        sigma_dislocation()
    z : float
        Positive depth im m below surface
    temp : float
        Temperature in K
    strain_rate : float
        Reference strain rate in 1/s. If `None` will use self.strain_rate
    compute : list
        List of processes to compute: 'dislocation', 'diffusion', 'dorn'.
        Default is ['dislocation', 'dorn'].
    mode : str
        'compression' or 'extension'

    Returns
    -------
    Sigma : float
        Differential stress in Pa
    """
    if z < 0:
        raise ValueError('Depth must be positive. Got z =', z)
    if strain_rate is None:
        e_prime = self.strain_rate
    else:
        e_prime = strain_rate

    compute_default = ['dislocation', 'dorn']
    if compute is None:
        compute = compute_default
    else:
        # Check the keywords
        for kwd in compute:
            if kwd not in compute_default:
                raise ValueError('Unknown compute keyword', kwd)

    s_byerlee = sigma_byerlee(material, z, mode)

    proplist = list(mat.keys())
    if 'diffusion' in compute and 'a_f' in proplist:
        s_diff = sigma_diffusion(material, temp, e_prime)
    else:
        s_diff = np.nan

    if 'dislocation' in compute and 'a_p' in proplist:
        s_disloc = sigma_dislocation(material, temp, e_prime)
    else:
        s_disloc = np.nan
    if 'dorn' in compute and 'sigma_d' in proplist:
        s_dorn = sigma_dorn(material, temp, e_prime)
    else:
        s_dorn = np.nan

    if (s_disloc > 200e6) and (s_dorn > 0):
        s_creep = s_dorn
    else:
        s_creep = s_disloc

    return min([s_byerlee, s_creep, s_diff])


def compute_dsigma(mat, z, T, strain_rate):
    """
    Compute differential stress for a given material at depths z and
    temperatures T. Comptues for both compression and extension and
    therefore the output depths array is a concatenation of z:z[::-1].

    Parameters
    ----------
    mat : dict
        Dict of type as defined in def materials()
    z : np.array
        1D array of increasing depth values in positive m
    T : np.array
        1D array of same shape as z with T in Kelvin
    strain_rate : float
        Strain rate in 1/s

    Returns
    -------
    dsigma : np.array
        1D array with computed differential stress.
    depths : np.array
        1D array with corresponding depth values
    """
    s_d_c = -1*sigma_d(mat, z, T, strain_rate=strain_rate,
                              mode='compression')
    s_d_e = sigma_d(mat, z, T, strain_rate=strain_rate,
                           mode='extension')
    return s_d_c, s_d_e



################################
### Calculating viscosity and strength
mat_dbase = sorted(materials(), key=lambda k:k['name'] )
mat=mat_dbase['name'==rheology_law]
dsigma_c = np.empty_like(data[:,1])
dsigma_e = np.empty_like(data[:,1])
eff_vis = np.empty_like(data[:,1])

## looping through alll points
for i in range(len(data)):
    dsigma_c[i],dsigma_e[i] = compute_dsigma(mat,data[i,2]*1e3,data[i,4],strain_rate)
    eff_vis[i] =  effective_viscosity(mat,data[i,4]+273,strain_rate) 

data=np.column_stack((data,dsigma_c))
data=np.column_stack((data,dsigma_e))
data=np.column_stack((data,np.log10(eff_vis)))
## saving the output
meta_data = "#Created on: " + str(date.today()) +"\n#Input file is: " + str(inputfile) +"\n#Output file is: " \
      	    + str(outputfile) +"\n#Material is: " + str(rheology_law) + "\n#Strain rate is :" + str(strain_rate) + "\n" + "#\n"
#np.savetxt(str(outdir)+'/'+str(outputfile),data,delimiter=',',header="#x(km) y(km) depth(km) Pressure(bar) Temperature(oC) Density(kg/m3) Vp(km/s) Vs(km/s) Vs_diff(%) Pseudo-melts(%) dsigma_c(Pascal) dsigma_e(Pascal) Viscosity(Pas)",comments=meta_data,fmt='%10.3f')
np.savetxt(str(outdir)+'/'+str(outputfile),data,delimiter=',',header="#x(km) y(km) depth(km) Pressure(bar) Temperature(oC) Density(kg/m3)\
 Vp(km/s) Vs(km/s) Vs_diff(%) Pseudo-melts(%) dsigma_c(Pascal) dsigma_e(Pascal) Viscosity(log10Pas)",comments=meta_data,fmt='%10.3f')

