import importlib
import os
from collections import OrderedDict

import torch
import numpy as np
from torchvision.transforms import transforms

model_config = OrderedDict([
    ('arch', 'mlp1'),
    ('n_classes', 10),
    ('dropout', 0.0)
    # Next entries are required for using the Wide-ResNet
    # ('depth', 28),
    # ('base_channels', 16),
    # ('widening_factor', 10),
    # ('drop_rate', 0.0),
    # ('input_shape', (1, 28, 28)),
])

data_config = OrderedDict([
    ('dataset', 'PermutedMNIST'),
    ('valid', 0.2),
    ('num_workers', 4),
    ('train_transform', transforms.Compose([
            lambda x: torch.FloatTensor(x),
            lambda x: x / 255.0,
            lambda x: (x - 0.1307) / 0.3081,
        ])),
    ('test_transform', transforms.Compose([
            lambda x: torch.FloatTensor(x),
            lambda x: x / 255.0,
            lambda x: (x - 0.1307) / 0.3081,
        ]))
])


run_config = OrderedDict([
    ('experiment', 'mlp_train'),  # This configuration will be executed by distill.py
    ('device', 'cuda'),
    ('tasks', [0]),  # , [4, 5], [6, 7], [8, 9]
    ('save', 'task1.distilled'),  # Path for the distilled dataset
    ('seed', 1234),
])

log_config = OrderedDict([
    ('wandb', True),
    ('wandb_name', 'model_lr0.1.no_dropout.outer320'),
    ('print', True),
    ('images', True),  # Save the distilled images
])

param_config = OrderedDict([
    ('epochs', 20),  # Training epoch performed by the model on the distilled dataset
    ('meta_lr', 0.1),  # Learning rate for distilling images
    ('model_lr', 0.1),  # Base learning rate for the model
    ('lr_lr', 0.0),  # Learning rate for the lrs of the model at each optimization step
    ('outer_steps', 320),  # Distillation epochs
    ('inner_steps', 3),  # Optimization steps of the model
    ('batch_size', 128),  # Minibatch size used during distillation
    ('buffer_size', 1),  # Number of examples per class kept in the buffer
])

config = OrderedDict([
    ('model_config', model_config),
    ('param_config', param_config),
    ('data_config', data_config),
    ('run_config', run_config),
    ('log_config', log_config),
])

if __name__ == '__main__':
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    experiment = importlib.import_module(config['run_config']['experiment'])
    experiment.run(config)