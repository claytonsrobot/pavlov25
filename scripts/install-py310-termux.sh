#!/data/data/com.termux/files/usr/bin/bash
# Install Python 3.10 on Termux (local user install)

set -e

PY_VER=3.10.14
PREFIX_DIR=$HOME/.localpython310

# 1. Install dependencies
pkg update -y && pkg upgrade -y
pkg install -y build-essential git wget clang make pkg-config \
               zlib zlib-dev libffi libffi-dev bzip2 bzip2-dev xz-utils

# 2. Download Python 3.10 source
cd $HOME
wget https://www.python.org/ftp/python/$PY_VER/Python-$PY_VER.tgz
tar -xvzf Python-$PY_VER.tgz
cd Python-$PY_VER

# 3. Configure and build
./configure --prefix=$PREFIX_DIR --enable-optimizations
make -j$(nproc)
make install

# 4. Update PATH in bashrc if not already present
BASHRC=$HOME/.bashrc
LINE="export PATH=\$HOME/.localpython310/bin:\$PATH"
if ! grep -Fxq "$LINE" $BASHRC; then
    echo "" >> $BASHRC
    echo "# Added by Python 3.10 installer" >> $BASHRC
    echo "$LINE" >> $BASHRC
fi

echo
echo "✅ Python $PY_VER installed to $PREFIX_DIR"
echo "➡️  Restart Termux or run: source ~/.bashrc"
echo "➡️  Then check with: python3.10 --version"
