#sh run_models_batch.sh from commandline 
python check_images.py --dir pet_images/ --arch resnet  --dogfile dognames.txt > resnet.txt
python check_images.py --dir pet_images/ --arch alexnet --dogfile dognames.txt > alexnet.txt
python check_images.py --dir pet_images/ --arch vgg  --dogfile dognames.txt > vgg.txt
