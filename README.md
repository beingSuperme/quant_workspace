一.环境部署
1. 更新系统并安装基础依赖
# 更新系统包（Ubuntu/Debian为例）
sudo apt update && sudo apt upgrade -y

# 安装编译工具和基础依赖
sudo apt install -y build-essential cmake git curl wget
sudo apt install -y libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev
sudo apt install -y libncurses5-dev libncursesw5-dev xz-utils libffi-dev liblzma-dev
sudo apt install -y tk-dev

# 安装图形库依赖（用于matplotlib等可视化）
sudo apt install -y libx11-dev libxext-dev libxrender-dev libxft-dev
sudo apt install -y libpng-dev libjpeg-dev libfreetype6-dev

2.安装Miniconda（推荐方式）
# 下载最新版Miniconda
cd /tmp
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# 安装（静默模式，安装在用户目录）
bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3

# 初始化conda
$HOME/miniconda3/bin/conda init bash

# 重新加载bash配置
source ~/.bashrc

# 验证安装
conda --version

3. 配置Conda环境
# 创建专用的量化环境
conda create -n quant python=3.10 -y

# 激活环境
conda activate quant

# 配置conda国内镜像（加速下载）
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
conda config --set show_channel_urls yes

核心量化库安装
1. 通过Conda安装基础科学计算包
conda install -y pandas numpy scipy matplotlib seaborn jupyterlab
conda install -y scikit-learn statsmodels
2. 通过pip安装量化专用库
# 配置pip国内镜像
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn

# 安装核心量化库
pip install backtrader empyrical quantstats

# 安装数据获取库
pip install akshare tushare baostock yfinance pandas-datareader

# 安装数据库支持（可选但推荐）
pip install sqlalchemy psycopg2-binary pymysql

# 安装API相关
pip install requests websocket-client python-socketio

# 安装开发工具
pip install black flake8 pylint jupyter-contrib-nbextensions

3. 安装Ta-Lib（技术分析指标库
# 安装ta-lib依赖
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
./configure --prefix=/usr
make
sudo make install

# 安装Python绑定
pip install TA-Lib

# 如果上面编译失败，可以尝试直接安装预编译版本
# conda install -c conda-forge ta-lib -y

开发环境配置
1. 安装和配置VS Code
# 下载并安装VS Code（Ubuntu/Debian）
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c echo 'deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main' > /etc/apt/sources.list.d/vscode.list
sudo apt update
sudo apt install code

# 或者使用snap安装
# sudo snap install code --classic

2. 配置VS Code扩展
安装以下扩展：

Python (Microsoft)
Jupyter (Microsoft)
Pylance
GitLens
Thunder Client
Bracket Pair Colorizer
Auto Rename Tag

3. 创建项目目录结构
# 创建量化工作区
mkdir -p ~/quant_workspace/{data,strategies,backtest,utils,notebooks,config,logs}
cd ~/quant_workspace

# 创建项目结构
mkdir -p data/{raw,processed,cache}
mkdir -p strategies/{technical,ml,basic}
mkdir -p backtest/{engines,results,reports}
mkdir -p utils/{data_loader,performance,risk_management}

# 创建基础文件
touch requirements.txt
touch README.md
touch .gitignore

4. 创建环境验证脚本
创建 ~/quant_workspace/test_environment.py：

高级配置（可选但推荐）
1. 配置Git
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
git config --global core.editor "code --wait"

2. 创建启动脚本
创建 ~/quant_workspace/start_quant.sh：

chmod +x ~/quant_workspace/start_quant.sh

3. 配置Jupyter Lab主题和扩展
# 安装Jupyter主题
pip install jupyterthemes

# 设置暗色主题
jt -t monokai -f fira -fs 12 -cellw 90% -ofs 11 -dfs 11 -T

# 安装Jupyter扩展
jupyter contrib nbextension install --user
jupyter nbextension enable codefolding/main

验证安装
运行环境测试脚本：
cd ~/quant_workspace
python test_environment.py

