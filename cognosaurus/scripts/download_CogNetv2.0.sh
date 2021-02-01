#!/bin/bash

apt install git-lfs
git clone https://github.com/kbatsuren/CogNet.git CogNet
cd CogNet
git lfs install --local
git lfs pull -I CogNet0-v2.0.zip
