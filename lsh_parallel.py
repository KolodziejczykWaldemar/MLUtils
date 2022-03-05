import math
from collections import defaultdict, Counter
from typing import List

import numpy as np


class LSH:
    """Implementation of Locality Sensitive Hashing fo continuous vector spaces."""

    def __init__(self,
                 vector_dims: int,
                 max_buckets: int = 1024,
                 n_universes: int = 25) -> None:
        """Locality Sensitive Hashing's constructor.

        Args:
            vector_dims (int): Dimensionality of one sample, i.e. embedding size
            max_buckets (int): Maximal number of buckets that data will be partition into. The real
                buckets number will be between max_buckets/2 and max_buckets.
            n_universes (int): Number of parallel universes that hash values will be calculated
                independently. Increasing that value increases probability, that similar vectors
                will lie in most of the same buckets.
        """
        # number of planes is log2(number_of_buckets)
        n_planes = math.floor(np.log2(max_buckets))
        self.n_buckets = 2 ** n_planes
        self.n_universes = n_universes
        self.planes = np.random.normal(size=(self.n_universes, vector_dims, n_planes))

        self.hash_to_index_map = None

    def get_hash_values(self,
                        vectors: np.ndarray) -> np.ndarray:
        """Calculates hashes for given vectors.

        Args:
            vectors (np.ndarray): Vectors of dimensionality (samples_number, embedding_size)

        Returns:
            np.ndarray: Buket indices for each sample for all universes with dimensionality
                (samples_number, n_universes)
        """
        # expand vectors by one extra dimension to conveniently perform matrix multiplication in 3D
        vectors_expanded = np.repeat(vectors[np.newaxis, :, :], self.planes.shape[0], axis=0)

        # for the every universe containing a set of planes, calculate the dot product between
        # vectors and the matrix containing planes
        # dimensionality of operation: X@Y=Z
        # X.shape = (n_universes, samples_number, embedding_size)
        # Y.shape = (n_universes, embedding_size, n_planes)
        # Z.shape = (n_universes, samples_number, n_planes)
        dot_product = np.matmul(vectors_expanded, self.planes)

        # get the sign of the dot product, checking whether vectors are blow or above planes.
        sign_of_dot_product = np.sign(dot_product)

        # change values range from (-1)-1 to 0-1
        # if the sign is 0, i.e. the vector is in the plane, consider the sign to be positive
        is_dot_product_nonnegative = (sign_of_dot_product >= 0).astype(int)

        # calculate hashes for each sample separately for different universes
        binary_exponents = np.arange(self.planes.shape[2])
        hash_values = np.sum(np.power(2, binary_exponents) * is_dot_product_nonnegative,
                             axis=2)

        # cast hash_values as an integer
        hash_values = hash_values.astype(int)

        return hash_values

    def make_hash_table(self, vectors: np.ndarray) -> None:
        """Makes a hash table from given vectors.

        Args:
            vectors (np.ndarray): Vectors of dimensionality (samples_number, embedding_size) to be
                used for building hash map.
        """
        # create the id table as a dictionary.
        # keys are integers (0,1,2... n_buckets)
        # values are empty lists of lists
        self.hash_to_index_map = defaultdict(lambda: defaultdict(list))

        hash_values = self.get_hash_values(vectors)

        for i, sample_hashes in enumerate(hash_values.T):
            for universe_id, sample_hash_in_universe in enumerate(sample_hashes):
                # store the vector's index 'i' (each document is given a unique integer 0,1,2...)
                # the key is the h, and the 'i' is appended to the list at key h
                self.hash_to_index_map[universe_id][sample_hash_in_universe].append(i)

    def get_similar_samples_indices(self,
                                    vector: np.ndarray,
                                    n_most_common: int = 5) -> List[int]:
        """Returns indices of similar samples to the given vector.

        Args:
            vector (np.ndarray): 1D query vector
            n_most_common (int): Number of most common indices among those found in hashing buckets.

        Returns:
            List[int]: List of indices considered as similiar by LSH.
        """
        # calculate hash values for given vector for each universe
        hash_values = self.get_hash_values(vector)

        # remove unnecessary dimension from (n_universes, 1) to (n_universes,)
        hash_values = np.squeeze(hash_values)

        similar_indices = []
        # iterate over all universes
        for universe_id, hash_value in enumerate(hash_values):
            # add indices found in current bucket into similar_indices
            similar_indices.extend(self.hash_to_index_map[universe_id][hash_value])

        # count indices in similar_indices and return n most common
        counted_indices = Counter(similar_indices)
        most_common = counted_indices.most_common(n_most_common)
        return [element[0] for element in most_common]


lsh = LSH(vector_dims=300)
vec = np.random.rand(1, 300)
print(f" The hash value for this vector,",
      f"is {lsh.get_hash_values(vec)}")
vec = np.random.rand(13, 300)
print(f" The hash value for this vector,",
      f"is {lsh.get_hash_values(vec)}")
vec = np.random.rand(11130, 300)
lsh.make_hash_table(vec)
sim = lsh.get_similar_samples_indices(np.random.rand(1, 300))
print(sim)
