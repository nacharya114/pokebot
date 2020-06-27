export HPARAMS=$1
export MODEL_SAVE_PATH=$2

nohup python train.py $1 $2 > log.txt 2>&1 &