## LLAMA

#!/encs/bin/bash
#SBATCH -J pass_finder --partition=pa --mem=16GB --gpus=1  --account=jinqiuy
#SBATCH --mail-type=BEGIN,END
#SBATCH --mail-user=l_ling20@encs.concordia.ca
# Specify the output file name
#SBATCH -o llama.log
module load anaconda3/2023.03/default
conda activate /speed-scratch/l_ling20/FairT

bash exp_by_hyp_batch.sh llama 5 default
bash exp_by_style_batch.sh llama 5 1.0
bash exp_by_iterations.sh llama 3 5
