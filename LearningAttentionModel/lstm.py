import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

torch.manual_seed(1)


lstm = nn.LSTM(3, 3)  # Input dim is 3, output dim is 3
inputs = [torch.randn(1, 3) for _ in range(5)]  # make a sequence of length 5

print(inputs)
print(inputs[0].size())
print()

# initialize the hidden state.
hidden = (torch.randn(1, 1, 3),
          torch.randn(1, 1, 3))

for i in inputs:
    # Step through the sequence one element at a time.
    # after each step, hidden contains the hidden state.

    print(i.view(1, 1, -1))

    out, hidden = lstm(i.view(1, 1, -1), hidden)