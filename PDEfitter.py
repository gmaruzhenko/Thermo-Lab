def convectionPowerLoss(T, Kc, a, Tamb):
    '''
    Params:
        T: Temperature of slice
        Kc: convection coefficient
        a: surface area of slice
        Tamb: ambient temperature
    '''

    return a * Kc * (T - Tamb)

SIGMA = 5.67*10**(-8) # Stefan-Boltzmann constant, in W/m^2/K^4
def radiationPowerLoss(T, e, a, Tamb):
    '''
    Params:
        T: Temperature of slice
        e: emissivity
        a: surface area of slice
        Tamb: ambient temperature
    '''

    return a * e * SIGMA * (T**4 - Tamb**4)

RHO = 2700 # density of Al, kg/m^3
C = 900 # heat capacity of Al, J/(kg*K)
def step(Tarr, k):
    T[1:-1] = T[1:-1] + (
            # effect of surrounding segment
            ((T[0:-2] - 2*T[1:-1] + T[2:])/dx**2) * K/(C*RHO) 
            # losses to convection and radiation
            + Parr / (C*RHO*PI*radius**2*dx)
        ) * dt
    T[0] = T[0] + (
            # effect of surrounding segment
            -1*K*(T[0]-T[1]) / (C*RHO*dx**2) 
            # losses to convection and radiation
            - (2*PI*radius*dx + PI*radius**2) * ( Kc*(T[0] - Tamb) + EPSILON*SIGMA*((T[0])**4 - Tamb**4)) / (C*RHO*PI*radius**2*dx)
            # input from heat source
            + powerIn / (C*RHO*PI*radius**2*dx)
        ) * dt
    T[-1] = T[-1] + (
            # effect of surrounding segment
            K*(T[-2]-T[-1]) / (C*RHO*dx**2) 
            # losses to convection and radiation
            - (2*PI*radius*dx + PI*radius**2) * ( Kc*(T[-1] - Tamb) + EPSILON*SIGMA*((T[-1])**4 - Tamb**4)) / (C*RHO*PI*radius**2*dx)
        ) * dt
    return T