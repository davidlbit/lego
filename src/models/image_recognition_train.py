#!/usr/bin/env python3
######################################################################
# Author: David Anthony Parham
#
# Module Description: This script is used to train an image recognition
# model designed to detect certain LEGO bricks.
######################################################################


import os
import time
from pathlib import Path

import numpy as np
import torch
import wandb
from custom_dataset import CustomDataset
from omegaconf import OmegaConf
from torch import nn, optim
from torch.utils.data import DataLoader, random_split
from torchvision import transforms
from torchvision.models import resnet18
from tqdm import tqdm

from data.synthetic_data import generate_synthetic_data_for_products

# Load config file
config_path = Path("..") / "config" / "config.yaml"
config = OmegaConf.load(config_path)

# Initialize logging with wandb and track conf settings
WANDB_API = os.getenv("WANDB_API")
wandb.login(key=WANDB_API)
wandb.init(project="lego-image-recognition", config=dict(config))

# Set seeds for reproducibility using numpy's Generator
rng = np.random.default_rng(seed=1)

# Constants from config for model training
EPOCHS = config.EPOCHS
BATCH_SIZE = config.BATCH_SIZE
LEARNING_RATE = config.LEARNING_RATE
N_WORKERS = config.N_WORKERS

# Dynamic variable from config
best_val = config.BEST_VAL

# Constant from config for synthetic data generation
HEIGHT = config.HEIGHT
WIDTH = config.WIDTH
CHANNELS = config.CHANNELS
N_IMAGES = config.N_IMAGES
DTYPE = config.DTYPE


# Determine device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("[INFO] Using device:", device)

# Replace with actual product IDs sources from the dummy database
product_ids = [1, 2, 3]

# Generate synthetic data
params = {"height": HEIGHT, "width": WIDTH, "channels": CHANNELS, "n_images": N_IMAGES, "dtype": DTYPE}
synthetic_data = generate_synthetic_data_for_products(product_ids, params)

# Extract images and labels from synthetic data
images_train = []
labels_train = []
for key, data in synthetic_data.items():
    for image in data:
        images_train.append(image)
        labels_train.append(key)

images_train = np.array(images_train)
labels_train = np.array(labels_train)

# Prepare transformations for the dataset
transform = transforms.Compose(
    [
        transforms.ToPILImage(),
        transforms.RandomAffine(degrees=20, translate=(0.2, 0.2), scale=(0.8, 1.2), shear=0.2),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)

# Create dataset and split into train and test sets
dataset = CustomDataset(images_train, labels_train, transform=transform)
train_size = int(0.8 * len(dataset))
test_size = len(dataset) - train_size
train_dataset, test_dataset = random_split(dataset, [train_size, test_size])

# Create dataloaders
train_loader = DataLoader(train_dataset, shuffle=True, num_workers=N_WORKERS, batch_size=BATCH_SIZE)
test_loader = DataLoader(test_dataset, shuffle=False, num_workers=N_WORKERS, batch_size=BATCH_SIZE)

# Build ResNet-18 model
model = resnet18(pretrained=False, num_classes=len(np.unique(labels_train)) + 1).to(device)

# Define loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

# Training loop
print("[INFO] Started training the model...\n")
start_time = time.time()

for epoch in tqdm(range(EPOCHS), desc="Training Epochs"):
    # Training
    model.train()
    train_losses = []
    correct = 0
    total = 0

    for images, labels in train_loader:
        optimizer.zero_grad()
        images, labels = images.to(device), labels.to(device)  # noqa

        # Forward pass
        outputs = model(images)

        # Compute loss
        loss = criterion(outputs, labels)

        # Backward pass and optimization
        loss.backward()
        optimizer.step()

        train_losses.append(loss.item())

        # Calculate accuracy
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    train_loss = np.mean(train_losses)
    train_acc = 100 * correct / total

    # Log train metrics
    wandb.log({"train_loss": train_loss, "train_acc": train_acc})

    # Validation
    model.eval()
    val_losses = []
    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)  # noqa

            # Forward pass
            outputs = model(images)

            # Compute loss
            loss = criterion(outputs, labels)
            val_losses.append(loss.item())

            # Calculate accuracy
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    val_loss = np.mean(val_losses)
    val_acc = 100 * correct / total

    # Log validation metrics
    wandb.log({"val_loss": val_loss, "val_acc": val_acc})

    print(
        f"Epoch {epoch + 1}/{EPOCHS} - "
        f"Train Loss: {train_loss:.4f} - Train Acc: {train_acc:.2f}% - "
        f"Val Loss: {val_loss:.4f} - Val Acc: {val_acc:.2f}%"
    )

    # Save best model
    if val_loss < best_val:
        best_val = val_loss
        print("\n[INFO] Saving new best_model...\n")
        os.makedirs(os.path.dirname(config.BEST_MODEL_PATH), exist_ok=True)
        torch.save(
            {
                "epoch": epoch + 1,
                "model_state_dict": model.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
            },
            config.BEST_MODEL_PATH,
        )

    # Save model checkpoint based on save_after frequency
    if (epoch + 1) % 5 == 0:
        print(f"\n[INFO] Saving model as checkpoint -> epoch_{epoch + 1}.pth\n")
        checkpoint_path = os.path.join(config.CHECKPOINT_PATH, f"epoch_{epoch + 1}.pth")
        torch.save(
            {
                "epoch": epoch + 1,
                "model_state_dict": model.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
            },
            checkpoint_path,
        )

end_time = time.time()
run_time = (end_time - start_time) / 60  # in minutes

# Optionally save checkpoint folder for each experiment
# wandb.save(config.CHECKPOINT_PATH)

print(f"[INFO] Successfully completed training session. Running time: {run_time:.2f} min")
