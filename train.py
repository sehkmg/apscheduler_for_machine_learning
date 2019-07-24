import argparse
import time
import os

from utils import write_result_to_file

# Get arguments
parser = argparse.ArgumentParser(description='apscheduler_test')
parser.add_argument(
    '--clip_gradient',
    action='store_true')
parser.add_argument(
    '--hidden_dim',
    type=int,
    default=512)
parser.add_argument(
    '--dropout_rate',
    type=float,
    default=0.5)
parser.add_argument(
    '--seed',
    type=int,
    default=1)
parser.add_argument(
    '--num_layers',
    type=int,
    default=1)
args = parser.parse_args()

# Training start
print('(using gpu:{}) Training Experiment: clip_gradient[{}], hidden_dim[{}], dropout_ratep[{}], num[{}], seed[{}]...'.format(os.environ['CUDA_VISIBLE_DEVICES'], args.clip_gradient, args.hidden_dim, args.dropout_rate, args.seed, args.num_layers))

# Training simulation
time.sleep(3)
valid_loss = 0.13321521
test_loss = 0.234212215

# Write result to file
result_dict = {'valid_loss': valid_loss, 'test_loss': test_loss}
write_result_to_file(args, result_dict, 'result.txt')

# Training end
print('(using gpu:{}) Training Experiment: clip_gradient[{}], hidden_dim[{}], dropout_ratep[{}], num[{}], seed[{}]...ENDED'.format(os.environ['CUDA_VISIBLE_DEVICES'], args.clip_gradient, args.hidden_dim, args.dropout_rate, args.seed, args.num_layers))
