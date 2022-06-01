import torch
import torch.nn as nn
import torch.nn.functional as F  # noqa
import wandb
from wandb.beta.workflows import use_model
from wandb.data_types import _SavedModel


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        output = F.log_softmax(x, dim=1)
        return output


def main():
    run = wandb.init(entity="mock_server_entity", project="test")

    my_model = Net()

    sm = _SavedModel.init(my_model)
    art = wandb.Artifact("my-model", "model")
    art.add(sm, "index")

    art = run.log_artifact(art)
    art.wait()

    _ = use_model("my-model:latest")

    run.finish()


if __name__ == "__main__":
    main()
