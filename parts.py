import numpy as np
import matplotlib.pyplot as plt
import itertools
import random

neighbors = [[-1,0],[1,0],[0,-1],[0,1]]

def Gen(mu,initial,fitness,recom,exposure_rate,migration_rate):

    L = 1
    while 2**L < len(fitness):
        L *= 2

    if 2**L != len(fitness):
        raise ValueError(
                "`fitness' should have length a power of 2")
    
    fitness = np.asarray(fitness)

    eps = 0.5*min(abs(x-y) for x,y in 
        itertools.combinations(fitness,2)
        if x != y)

    def gen():
        M,N = initial.shape
        size = M*N
        nloci = M*N*L

        x,y,z = np.indices([M,N,L])
        X,Y = np.indices([M,N])

        state = initial[:]
        best = np.empty(state.shape,dtype='int64')
        fit  = np.empty(state.shape,dtype=float)
        nfit = np.empty(state.shape,dtype=float)
        fit_ = np.empty(state.shape,dtype=float)

        while True:
            yield state

            # Migration
            if nmigrations := np.random.poisson(migration_rate*size):
                mig_src = np.random.choice(np.arange(size),nmigrations,replace=False)
                mig_dst = np.random.choice(np.arange(size),nmigrations,replace=False)

                state.flat[mig_dst] = \
                        state.flat[mig_src]

            # Mutation
            nmutants = np.random.poisson(mu*nloci)
            if ( nmutants ):
                mutants = np.random.choice(
                        np.arange(nloci,dtype='int64'),
                        nmutants,
                        replace=False)
                state[x.flat[mutants],y.flat[mutants]] ^= 1<<z.flat[mutants]

            # Select cells to be affected by neighboring cells
            exposure_idx = np.arange(0,size)[np.random.random(size=size) < exposure_rate]

            # Recombination
            nrevts = np.random.poisson(recom*size)
            if (nrevts):
                revts = np.random.choice(
                        exposure_idx,
                        nrevts,
                        replace=False)

                mask = np.random.randint(
                        0,
                        1<<L,
                        size=nrevts,
                        dtype='int64')

                rX,rY = X.flat[revts],Y.flat[revts]
                loc = np.zeros(nrevts,dtype='int64')

                for i,j in neighbors:
                    loc |= state[rX,rY] ^ state[(rX+i)%M,(rY+j)%N]

                state[rX,rY] = loc & mask

            # Fitness
            best[:] = state
            fit[:] = ( fitness[state] + 
                    np.random.uniform(eps/4,eps/2,state.shape) )
            nfit[:] = fit
            eX,eY = X.flat[exposure_idx],Y.flat[exposure_idx]
            for i,j in neighbors:
                candidate = state[(X+i)%M,(Y+j)%N]
                fit_[:] = fit[(X+i)%M,(Y+j)%N]
                best[:] = np.choose(
                        fit_ > nfit,
                        (best,candidate)
                        )
                nfit[:] = np.choose(
                        fit_ > nfit,
                        (nfit,fit_)
                        )
            state[eX,eY] = best[eX,eY]
    return gen
