from verl.utils.reward_score import big_math

big_math.compute_score("<answer>and</answer> <answer>3</answer> <answer>0.4</answer>", {"target":"\\frac{2}{5}"}, 0, 1)


export LD_LIBRARY_PATH=/home/zhuofeng/.local/lib/python3.10/site-packages/nvidia/cudnn/lib:$LD_LIBRARY_PATH
