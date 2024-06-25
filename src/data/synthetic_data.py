#!/usr/bin/env python3
######################################################################
# Authors:  David Anthony Parham

# Module Description: This script is meant to demonstrate
# the functionality of creating synthetic images, based on provided
# product ids, and their CAT models, sourced from the database.
######################################################################

from typing import Any, Dict, List, Tuple

import numpy as np
from tqdm import tqdm


# Placeholder function to simulate fetching product information based on product ID
def get_product_info(product_id: int) -> Any:
    """Fetch the product information based on the product ID.

    :param product_id: The product ID for which to fetch the information
    :return: Model or configuration data needed to generate the synthetic image
    """
    # Example: Returning a dummy model/config based on product ID
    return {"model": f"CAT-{product_id}", "param": 42}


def generate_synthetic_image(  # noqa
    height: int, width: int, channels: int, product_info: Any, dtype: np.dtype = np.uint8, seed: int = 42
) -> np.ndarray:
    """Generate a single synthetic image with specified dimensions and data type based on product information.

    :param height: Height of the image
    :param width: Width of the image
    :param channels: Number of channels in the image
    :param product_info: Model or configuration data needed to generate the synthetic image
    :param dtype: Data type of the image (default: np.uint8)
    :param seed: Seed for the random number generator (default: 42)
    :return: Generated synthetic image as a NumPy array
    """
    model = product_info["model"]  # noqa
    param = product_info["param"]

    # Generate a random image (use product_info to influence this)
    rng = np.random.default_rng(seed=seed)  # Set a seed for reproducibility
    image = rng.integers(0, 256, size=(height, width, channels), dtype=dtype)

    # Custom logic based on model/param can be added here
    image = (image.astype(np.int16) + param) % 256
    image = image.astype(dtype)

    return image


def generate_synthetic_data(
    product_id: int, n_images: int, dim: Tuple[int, int, int], dtype: np.dtype = np.uint8
) -> np.ndarray:
    """Generate synthetic data for a specific product ID.

    :param product_id: Product ID for which synthetic data needs to be generated
    :param n_images: Number of images to generate
    :param dim: Dimensions of each image (height, width, channels)
    :param dtype: Data type of the image (default: np.uint8)
    :return: Generated synthetic data as a NumPy array
    """
    height, width, channels = dim

    # Fetch product information based on product_id
    product_info = get_product_info(product_id)

    # Generate synthetic data
    synthetic_data = [generate_synthetic_image(height, width, channels, product_info, dtype) for _ in range(n_images)]

    # Convert synthetic_data list to a NumPy array
    return np.array(synthetic_data)


def generate_synthetic_data_for_products(
    product_ids: List[int], params: Dict[str, Any], show_progress: bool = True
) -> Dict[int, np.ndarray]:
    """Generate synthetic data for a list of product IDs.

    :param product_ids: List of product IDs for which synthetic data needs to be generated
    :param params: Dictionary containing parameters like height, width, channels, n_images, and dtype
    :param show_progress: Flag to show or suppress the progress bar (default: True)
    :return: Dictionary mapping product IDs to generated synthetic data
    """
    height = params["height"]
    width = params["width"]
    channels = params["channels"]
    n_images = params["n_images"]
    dtype = params["dtype"]

    synthetic_data: Dict[int, np.ndarray] = {}

    # Flag to display or suppress progress bar
    iterator = tqdm(product_ids, desc="Generating Synthetic Data") if show_progress else product_ids

    for product_id in iterator:
        data = generate_synthetic_data(product_id, n_images, (height, width, channels), dtype)
        synthetic_data[product_id] = data

    return synthetic_data


if __name__ == "__main__":
    # Example usage:
    product_ids = [1, 2, 3]  # Replace with actual product IDs
    params = {"height": 256, "width": 256, "channels": 3, "n_images": 10, "dtype": np.uint8}
    synthetic_data = generate_synthetic_data_for_products(product_ids, params)
    for pid, data in synthetic_data.items():
        print(f"Product ID {pid}: Data shape {data.shape}")
