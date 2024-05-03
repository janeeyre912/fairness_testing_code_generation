SAMPLING="10"
STYLE="default"
DATA_PATH="../dataset/prompts_32.jsonl"
OUTPUT_PATH="../outputs/"
MODEL_NAME=$1
MODEL_DIR="$OUTPUT_PATH$MODEL_NAME"

if [ "$#" -le 0 ]; then
    echo "Usage: bash exp_by_hyp_batch.sh [model_name]"
    exit
fi

if [ "$#" -ge 2 ]; then
    SAMPLING=$2
fi

if [ "$#" -ge 3 ]; then
    STYLE=$3
fi

for i in 0.2 0.4 0.6 0.8 1.0
do
    temperature="${i/./}"
    bash gen_and_exp.sh "$SAMPLING" $i "$STYLE" $DATA_PATH "../outputs/hyp_variations/""$MODEL_NAME""$temperature""$STYLE" "$MODEL_NAME"
done
