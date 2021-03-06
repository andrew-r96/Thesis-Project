import importlib
import os
from collections import OrderedDict

import torch
import numpy as np
from torchvision.transforms import transforms

model_config = OrderedDict([
    ('arch', 'lenet5'),
    ('n_classes', 10),
    # Next entries are required for using the Wide-ResNet
    # ('depth', 28),
    # ('base_channels', 16),
    # ('widening_factor', 10),
    # ('drop_rate', 0.0),
    ('input_shape', (1, 28, 28)),
])

data_config = OrderedDict([
    ('dataset', 'SplitMNIST'),
    ('valid', 0.2),
    ('num_workers', 4),
    ('train_transform', transforms.Compose([
            lambda x: np.array(x).reshape((1, 28, 28)),
            lambda x: np.pad(x, ((0, 0), (2, 2), (2, 2)), mode='reflect'), # Padding is only required by LeNet
            lambda x: torch.FloatTensor(x),
            lambda x: x / 255.0,
            transforms.Normalize(np.array([0.1307]), np.array([0.3081]))
        ])),
    ('test_transform', transforms.Compose([
            lambda x: np.array(x).reshape((1, 28, 28)),
            lambda x: np.pad(x, ((0, 0), (2, 2), (2, 2)), mode='reflect'),
            lambda x: torch.FloatTensor(x),
            lambda x: x / 255.0,
            transforms.Normalize(np.array([0.1307]), np.array([0.3081]))
        ]))
])

run_config = OrderedDict([
    ('experiment', 'distill_fixed'),
    ('device', 'cuda'),
    ('task', [0, 9, 2, 8]),
    ('save', None),  # Path for the distilled dataset
    ('seed', 1234),
])

log_config = OrderedDict([
    ('wandb', False),
    ('wandb_name', 'distill.class1.buff1'),
    ('print', True),
    ('images', True), # Save the distilled images
])

param_config = OrderedDict([
    ('epochs', 3),  # Training epoch performed by the model on the distilled dataset
    ('meta_lr', 0.1),  # Learning rate for distilling images
    ('model_lr', 0.1),  # Base learning rate for the model
    ('lr_lr', 0.0),  # Learning rate for the lrs of the model at each optimization step
    ('outer_steps', 32),  # Distillation epochs
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
    os.environ['CUDA_VISIBLE_DEVICES'] = '1'
    experiment = importlib.import_module(config['run_config']['experiment'])
    experiment.run(config)