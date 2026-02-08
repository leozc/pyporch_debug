import sys
import torch
from torchvision import datasets, transforms

from model import MNISTNet

MODEL_PATH = "mnist_model.pth"
DATA_DIR = "./data"
device = torch.device("cpu")


def load_model():
    model = MNISTNet().to(device)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device, weights_only=True))
    model.eval()
    return model


def predict_sample(model, index=0):
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,)),
    ])
    dataset = datasets.MNIST(DATA_DIR, train=False, download=True, transform=transform)
    image, label = dataset[index]
    image = image.unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(image)
        probs = torch.softmax(output, dim=1)
        pred = output.argmax(dim=1).item()
        confidence = probs[0, pred].item()

    print(f"Sample index: {index}")
    print(f"True label:   {label}")
    print(f"Predicted:    {pred}")
    print(f"Confidence:   {confidence:.4f}")
    return pred


def main():
    index = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    model = load_model()
    predict_sample(model, index)


if __name__ == "__main__":
    main()
