import sys, math
import numpy as np
import pystan
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def simulate():
  print '\tGenerating simulated data...'
  N = 15
  D = 30
  exponential_scale = 10
  normal_sigma = 1

  observations = np.zeros((N, D))
  for i in range(N):
    exp_draw = np.random.exponential(scale = exponential_scale)
    print exp_draw
    for j in range(D):
      observations[i][j] = normal_sigma * np.random.randn() + exp_draw
      
  # Construct dictionary to pass to Stan
  dataset = {
    'N': N,
    'D': D,
    'observations': observations,
  }
  return dataset


def inference(dataset):
  print '\tPerforming inference...'
  NUM_ITER = 1000
  WARMUP = 500
  NUM_CHAINS = 4
  NUM_CORES = 4
  STAN_FN = 'hierarchical_model_1-1.stan'

  fit = pystan.stan(file = STAN_FN, 
                    data = dataset, 
                    iter = NUM_ITER, 
                    warmup = WARMUP, 
                    chains = NUM_CHAINS, 
                    n_jobs = NUM_CORES)
  print(fit)

  fit.plot()
  plt.tight_layout()
  plt.savefig('fit_pystan.png')

  normal_mus = fit['normal_mus'][-1]
  print normal_mus
  return


def main():
  dataset = simulate()
  inference(dataset)
  return


if __name__ == '__main__':
  main()