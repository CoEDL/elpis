#!/bin/bash

echo "Setting up '/recordings' directory..."
git clone --depth=1 https://github.com/CoEDL/toy-corpora.git
mv toy-corpora/abui-recordings-elan /recordings
rm -rf ./toy-corpora

mv /recordings/transcribed/abui_1.eaf /recordings/transcribed/1_1_1.eaf
mv /recordings/transcribed/abui_1.wav /recordings/transcribed/1_1_1.wav
mv /recordings/transcribed/abui_2.eaf /recordings/transcribed/1_1_2.eaf
mv /recordings/transcribed/abui_2.wav /recordings/transcribed/1_1_2.wav
mv /recordings/transcribed/abui_3.eaf /recordings/transcribed/1_1_3.eaf
mv /recordings/transcribed/abui_3.wav /recordings/transcribed/1_1_3.wav
mv /recordings/transcribed/abui_4.eaf /recordings/transcribed/1_1_4.eaf
mv /recordings/transcribed/abui_4.wav /recordings/transcribed/1_1_4.wav
echo "done."