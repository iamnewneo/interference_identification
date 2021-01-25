import torch
from torch import nn
from tqdm import tqdm
import pytorch_lightning as pl

from interf_ident import config


def loss_fn(out, target):
    n_classes = len(config.CLASSES)
    return nn.CrossEntropyLoss()(out.view(-1, n_classes), target)


def evaluate_model(model, data_loader):
    all_ids = []
    all_losses = torch.FloatTensor([])
    all_predictions = torch.FloatTensor([])

    model = model.to(config.DEVICE)
    result = {}
    total = 0
    correct = 0
    total_loss = 0
    for batch in data_loader:
        X = batch["X"].to(config.DEVICE)
        targets = batch["target"]

        with torch.no_grad():
            out = model(X)
            out = out.to("cpu")
            loss = loss_fn(out, targets)
            _, predicted = torch.max(out.data, 1)

            total += targets.size(0)
            correct += (predicted == targets).sum().item()
            all_predictions = torch.cat((all_predictions, predicted), axis=0)
            total_loss += loss.item()

    result["predictions"] = all_predictions
    result["accuracy"] = (correct * 100) / total
    result["loss"] = total_loss / len(data_loader)
    return result
