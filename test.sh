#!/bin/bash


git clone --depth=1 https://github.com/CoEDL/toy-corpora.git
p=$(pwd)
mv toy-corpora/abui-recordings-elan /recordings

mv /recordings/transcribed/abui_1.eaf /recordings/transcribed/1_1_1.eaf
mv /recordings/transcribed/abui_1.wav /recordings/transcribed/1_1_1.wav
mv /recordings/transcribed/abui_2.eaf /recordings/transcribed/1_1_2.eaf
mv /recordings/transcribed/abui_2.wav /recordings/transcribed/1_1_2.wav
mv /recordings/transcribed/abui_3.eaf /recordings/transcribed/1_1_3.eaf
mv /recordings/transcribed/abui_3.wav /recordings/transcribed/1_1_3.wav
mv /recordings/transcribed/abui_4.eaf /recordings/transcribed/1_1_4.eaf
mv /recordings/transcribed/abui_4.wav /recordings/transcribed/1_1_4.wav

cd $p