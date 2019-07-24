# APscheduler for machine learning
APScheduler for deploying lots of machine learning experiments.

## Environment
- Python 3
- APScheduler 3.6.0

## How to use
1. Prepare codes for ML experiment.
<pre><code>sehkmg@local:~/experiment$ ls
train.py  utils.py</code></pre>

2. Copy deploy.py and schedule_training.
<pre><code>sehkmg@local:~/experiment$ ls
deploy.py  schedule_training  train.py  utils.py</code></pre>

3. Write command and argument information in schedule_training/cmd2exec.py.
<pre><code># base command
base_command = 'python train.py'

# arguments
onoff_args = ['--clip_gradient']

args_info = [{'arg': '--hidden_dim', 'option': [256,512]},
             {'arg': '--dropout_rate', 'option': [0.3, 0.5]}]

iteration_args_info = [{'arg': '--seed', 'start': 1, 'end': 2},
                 {'arg': '--num_layers', 'start': 1, 'end': 2}]</code></pre>
                 
4. Execute schedule_training/cmd2exec.py and check commands in schedule_training/cmd2exec.txt.
<pre><code>In cmd2exec.txt:
python train.py --hidden_dim=256 --dropout_rate=0.3 *--seed=1~2 *--num_layers=1~2
python train.py --hidden_dim=256 --dropout_rate=0.5 *--seed=1~2 *--num_layers=1~2
python train.py --hidden_dim=512 --dropout_rate=0.3 *--seed=1~2 *--num_layers=1~2
python train.py --hidden_dim=512 --dropout_rate=0.5 *--seed=1~2 *--num_layers=1~2
python train.py --clip_gradient --hidden_dim=256 --dropout_rate=0.3 *--seed=1~2 *--num_layers=1~2
python train.py --clip_gradient --hidden_dim=256 --dropout_rate=0.5 *--seed=1~2 *--num_layers=1~2
python train.py --clip_gradient --hidden_dim=512 --dropout_rate=0.3 *--seed=1~2 *--num_layers=1~2
python train.py --clip_gradient --hidden_dim=512 --dropout_rate=0.5 *--seed=1~2 *--num_layers=1~2</code></pre>

5. By using commands in schedule_training/cmd2exec.txt, write training schedule in schedule_training/cmd2deploy.txt.
<pre><code>gpu:0
python train.py --hidden_dim=256 --dropout_rate=0.3 *--seed=1~2 *--num_layers=1~2 # deploy immediately using gpu 0, you can write comment like this.

gpu:1
python train.py --clip_gradient --hidden_dim=256 --dropout_rate=0.3 --seed=1 --num_layers=1     #   deploy immediately using gpu 1.

python train.py --hidden_dim=512 --dropout_rate=0.5 --seed=2 --num_layers=1 # deploy immediately using gpu 1.
python train.py --hidden_dim=512 --dropout_rate=0.5 --seed=1 --num_layers=2 # run right after previous experiment ended.






doc
1. you can write document like this.

2.
python train.py --hidden_dim=256 --dropout_rate=0.3 *--seed=1~2 *--num_layers=1~2
is exactly equivalent to:
python train.py --hidden_dim=256 --dropout_rate=0.3 --seed=1 --num_layers=1
python train.py --hidden_dim=256 --dropout_rate=0.3 --seed=1 --num_layers=2
python train.py --hidden_dim=256 --dropout_rate=0.3 --seed=2 --num_layers=1
python train.py --hidden_dim=256 --dropout_rate=0.3 --seed=2 --num_layers=2

3. only comment after command is allowed.</code></pre>

6. Check commands list which will be deployed.
<pre><code>sehkmg@local:~/experiment$ python3 schedule_training/cmd2deploy.py
CUDA_VISIBLE_DEVICES=0 python train.py --hidden_dim=256 --dropout_rate=0.3 --num_layers=1 --seed=1
CUDA_VISIBLE_DEVICES=0 python train.py --hidden_dim=256 --dropout_rate=0.3 --num_layers=1 --seed=2
CUDA_VISIBLE_DEVICES=0 python train.py --hidden_dim=256 --dropout_rate=0.3 --num_layers=2 --seed=1
CUDA_VISIBLE_DEVICES=0 python train.py --hidden_dim=256 --dropout_rate=0.3 --num_layers=2 --seed=2

CUDA_VISIBLE_DEVICES=1 python train.py --clip_gradient --hidden_dim=256 --dropout_rate=0.3 --seed=1 --num_layers=1

CUDA_VISIBLE_DEVICES=1 python train.py --hidden_dim=512 --dropout_rate=0.5 --seed=2 --num_layers=1
CUDA_VISIBLE_DEVICES=1 python train.py --hidden_dim=512 --dropout_rate=0.5 --seed=1 --num_layers=2</code></pre>

7. Deploy!
<pre><code>sehkmg@local:~/experiment$ python3 deploy.py
Press Ctrl+C to exit
(using gpu:0) Training Experiment: clip_gradient[False], hidden_dim[256], dropout_ratep[0.3], num[1], seed[1]...
(using gpu:1) Training Experiment: clip_gradient[True], hidden_dim[256], dropout_ratep[0.3], num[1], seed[1]...
(using gpu:1) Training Experiment: clip_gradient[False], hidden_dim[512], dropout_ratep[0.5], num[2], seed[1]...
(using gpu:0) Training Experiment: clip_gradient[False], hidden_dim[256], dropout_ratep[0.3], num[1], seed[1]...ENDED
(using gpu:0) Training Experiment: clip_gradient[False], hidden_dim[256], dropout_ratep[0.3], num[2], seed[1]...
(using gpu:1) Training Experiment: clip_gradient[True], hidden_dim[256], dropout_ratep[0.3], num[1], seed[1]...ENDED
(using gpu:1) Training Experiment: clip_gradient[False], hidden_dim[512], dropout_ratep[0.5], num[2], seed[1]...ENDED
(using gpu:1) Training Experiment: clip_gradient[False], hidden_dim[512], dropout_ratep[0.5], num[1], seed[2]...
(using gpu:0) Training Experiment: clip_gradient[False], hidden_dim[256], dropout_ratep[0.3], num[2], seed[1]...ENDED
(using gpu:0) Training Experiment: clip_gradient[False], hidden_dim[256], dropout_ratep[0.3], num[1], seed[2]...
(using gpu:1) Training Experiment: clip_gradient[False], hidden_dim[512], dropout_ratep[0.5], num[1], seed[2]...ENDED
(using gpu:0) Training Experiment: clip_gradient[False], hidden_dim[256], dropout_ratep[0.3], num[1], seed[2]...ENDED
(using gpu:0) Training Experiment: clip_gradient[False], hidden_dim[256], dropout_ratep[0.3], num[2], seed[2]...
(using gpu:0) Training Experiment: clip_gradient[False], hidden_dim[256], dropout_ratep[0.3], num[2], seed[2]...ENDED
sehkmg@local:~/experiment$</code></pre>
