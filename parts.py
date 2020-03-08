import numpy as np
import matplotlib.pyplot as plt
import itertools
import random

iterant = [[-1,0],[1,0],[0,-1],[0,1]]

def Gen(mu,initial,L,fitness,recom):

    assert(2**L == len(fitness))
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
            if ( nmutants := np.random.poisson(mu*nloci)):
                mutants = np.random.choice(
                        np.arange(nloci,dtype='int64'),
                        nmutants,
                        replace=False)
                state[x.flat[mutants],y.flat[mutants]] ^= 1<<z.flat[mutants]

            if (nrevts := np.random.poisson(recom*size)):

                revts = np.random.choice(
                        np.arange(0,size,dtype='int64'),
                        nrevts,
                        replace=False)

                mask = np.random.randint(
                        0,
                        1<<L,
                        size=nrevts,
                        dtype='int64')

                rX,rY = X.flat[revts],Y.flat[revts]
                loc = np.zeros(nrevts,dtype='int64')

                for i,j in iterant:
                    loc |= state[rX,rY] ^ state[(rX+i)%M,(rY+j)%N]

                state[rX,rY] = loc & mask

            best[:] = state
            fit[:] = ( fitness[state] + 
                    np.random.uniform(eps/4,eps/2,state.shape) )
            nfit[:] = fit
            for i,j in iterant:
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
            state[:] = best
    return gen
        
def makeframe(state,loci,img):
    img.set_data(state)
    return [img]