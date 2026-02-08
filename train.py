import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

from model import MNISTNet

BATCH_SIZE = 64
EPOCHS = 5
LR = 1e-3
DATA_DIR = "./data"
MODEL_PATH = "mnist_model.pth"

device = torch.device("cpu")


def get_data_loaders():
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,)),
    ])
    train_dataset = datasets.MNIST(DATA_DIR, train=True, download=True, transform=transform)
    test_dataset = datasets.MNIST(DATA_DIR, train=False, transform=transform)

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=1000, shuffle=False)
    return train_loader, test_loader


def train_one_epoch(model, loader, optimizer, criterion, epoch):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for batch_idx, (data, target) in enumerate(loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        pred = output.argmax(dim=1)
        correct += pred.eq(target).sum().item()
        total += target.size(0)

        if batch_idx % 200 == 0:
            print(f"  Epoch {epoch} [{batch_idx * len(data)}/{len(loader.dataset)}] "
                  f"Loss: {loss.item():.4f}")

    accuracy = 100.0 * correct / total
    avg_loss = running_loss / len(loader)
    print(f"  Train — Loss: {avg_loss:.4f}, Accuracy: {accuracy:.2f}%")


def evaluate(model, loader, criterion):
    model.eval()
    test_loss = 0.0
    correct = 0

    with torch.no_grad():
        for data, target in loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += criterion(output, target).item()
            pred = output.argmax(dim=1)
            correct += pred.eq(target).sum().item()

    test_loss /= len(loader)
    accuracy = 100.0 * correct / len(loader.dataset)
    print(f"  Test  — Loss: {test_loss:.4f}, Accuracy: {accuracy:.2f}%")
    return accuracy


def main():
    print(f"Using device: {device}")
    train_loader, test_loader = get_data_loaders()

    model = MNISTNet().to(device)
    optimizer = optim.Adam(model.parameters(), lr=LR)
    criterion = nn.CrossEntropyLoss()

    best_acc = 0.0
    for epoch in range(1, EPOCHS + 1):
        print(f"\n--- Epoch {epoch}/{EPOCHS} ---")
        train_one_epoch(model, train_loader, optimizer, criterion, epoch)
        acc = evaluate(model, test_loader, criterion)

        if acc > best_acc:
            best_acc = acc
            torch.save(model.state_dict(), MODEL_PATH)
            print(f"  Saved best model ({best_acc:.2f}%)")

    print(f"\nTraining complete. Best test accuracy: {best_acc:.2f}%")


if __name__ == "__main__":
    main()
