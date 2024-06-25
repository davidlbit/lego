#!/usr/bin/env python3
######################################################################
# Author: David Anthony Parham
#
# Module Description: This script contains the implementation of the
# CustomDataset class, which is needed to create the dataset that
# trains the image recognition model.
######################################################################


from torch.utils.data import Dataset


class CustomDataset(Dataset):
    """Custom dataset for loading the synthetic generated images."""

    def __init__(self, data, targets, transform=None):
        self.data = data
        self.targets = targets
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        image = self.data[index]
        target = self.targets[index]

        if self.transform:
            image = self.transform(image)

        return image, target
