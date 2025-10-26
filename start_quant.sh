#!/bin/bash
echo "🚀 启动量化开发环境..."

# 激活conda环境
eval "$(conda shell.bash hook)"
conda activate quant

# 进入工作目录
cd ~/quant_workspace

# 启动Jupyter Lab（后台运行）
echo "📓 启动Jupyter Lab..."
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --notebook-dir=./notebooks &

echo "✅ 环境已启动！"
echo "📊 Jupyter Lab: http://localhost:8888"
echo "📁 工作目录: ~/quant_workspace"