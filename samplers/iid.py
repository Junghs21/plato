"""
Samples data from a dataset in an independent and identically distributed fashion.
"""
import torch
import numpy as np

from samplers import base
from config import Config
from torch.utils.data import SubsetRandomSampler


class Sampler(base.Sampler):
    """Create a data sampler for each client to use a randomly divided partition of the
    dataset."""
    def __init__(self, datasource, client_id):
        super().__init__(datasource)
        self.client_id = client_id

        indices = list(range(self.dataset_size))
        np.random.seed(self.random_seed)
        np.random.shuffle(indices)

        partition_size = Config().data.partition_size
        total_clients = Config().clients.total_clients
        total_size = partition_size * total_clients

        # add extra samples to make it evenly divisible, if needed
        indices += indices[:(total_size - len(indices))]
        assert len(indices) == total_size

        # Compute the indices of data in the subset for this client
        self.subset_indices = indices[(int(self.client_id) -
                                       1):total_size:total_clients]
        print(len(indices))
        print(indices[:10])
        print(len(self.subset_indices))
        print(self.subset_indices[:10])

    def get(self):
        gen = torch.Generator()
        gen.manual_seed(self.random_seed)
        return SubsetRandomSampler(self.subset_indices, generator=gen)

    def trainset_size(self):
        return len(self.subset_indices)
