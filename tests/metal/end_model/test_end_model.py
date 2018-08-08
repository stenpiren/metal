import unittest

import numpy as np
import torch

from metal.end_model import EndModel, LogisticRegression

class EndModelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set seed
        np.random.seed(1)

        N = 2000

        X = np.random.random((N,2)) * 2 - 1
        Y = (X[:,0] > X[:,1] + 0.25).astype(int) + 1

        X = torch.tensor(X, dtype=torch.float)
        Y = torch.tensor(Y, dtype=torch.long)

        Xs = [X[:1000], X[1000:1500], X[1500:]]
        Ys = [Y[:1000], Y[1000:1500], Y[1500:]]
        cls.single_problem = (Xs, Ys)

    def test_logreg(self):
        em = LogisticRegression(seed=1, input_dim=2, verbose=False)
        Xs, Ys = self.single_problem
        em.train(Xs[0], Ys[0], Xs[1], Ys[1], n_epochs=5)
        score = em.score(Xs[2], Ys[2], verbose=False)
        self.assertGreater(score, 0.95)

    def test_singletask(self):
        em = EndModel(seed=1, batchnorm=False, dropout=0.0, verbose=False, 
            layer_output_dims=[2,10])
        Xs, Ys = self.single_problem
        em.train(Xs[0], Ys[0], Xs[1], Ys[1], n_epochs=5)
        score = em.score(Xs[2], Ys[2], verbose=False)
        self.assertGreater(score, 0.95)

    def test_singletask_extras(self):
        em = EndModel(seed=1, batchnorm=True, dropout=0.01, verbose=False,
            layer_output_dims=[2,10])
        Xs, Ys = self.single_problem
        em.train(Xs[0], Ys[0], Xs[1], Ys[1], n_epochs=5)
        score = em.score(Xs[2], Ys[2], verbose=False)
        self.assertGreater(score, 0.95)
        
        
if __name__ == '__main__':
    unittest.main()        