# This is a Windows 11 guide to install & run PC-AVS
I have documented the exact steps that got it working for me after 2 days of struggle with different virtual environments.

# Pose-Controllable Talking Face Generation by Implicitly Modularized Audio-Visual Representation (CVPR 2021)

[Hang Zhou](https://hangz-nju-cuhk.github.io/), Yasheng Sun, [Wayne Wu](https://wywu.github.io/), [Chen Change Loy](http://personal.ie.cuhk.edu.hk/~ccloy/), [Xiaogang Wang](http://www.ee.cuhk.edu.hk/~xgwang/), and [Ziwei Liu](https://liuziwei7.github.io/).


<img src='./misc/demo.gif' width=800>

### [Project](https://hangz-nju-cuhk.github.io/projects/PC-AVS) | [Paper](https://arxiv.org/abs/2104.11116) | [Demo](https://www.youtube.com/watch?v=lNQQHIggnUg)

We propose **Pose-Controllable Audio-Visual System (PC-AVS)**, 
which achieves free pose control when driving arbitrary talking faces with audios. Instead of learning pose motions from audios, we leverage another pose source video to compensate only for head motions.
The key is to devise an implicit low-dimension pose code that is free of mouth shape or identity information. 
In this way, audio-visual representations are modularized into spaces of three key factors: speech content, head pose, and identity information.

<img src='./misc/method.png' width=800>

## Requirements
Anaconda3 Prompt is used

You can get it [here](https://www.anaconda.com/products/individual)

## Quick Start: Generate Demo Results
Clone the repository
Run anaconda3 prompt and run each of these commands to set up the environment
```
1. cd *Path_To_PCAVS*

2. conda create -n PCAVS38 python=3.8

3. conda activate PCAVS38

# If you have Nvidia RTX 4070 GPU
4. conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
#OR for CPU 
4. conda install pytorch torchvision torchaudio cpuonly -c pytorch

5.1 pip install pip-tools
5.2. I renamed the original rwquirements.txt to requirements_old.txt.
5.3. I created a new file called requirements.in at the same level as requirements_old.txt.
5.4. I copied everything in requirements_old.txt to requirements.in but without any version details (just the name of the packages).
5.5 pip-compile --upgrade
5.6. The above command will create a new file called requirements.txt at the same as requirements.in with all the packages specified in requirements.in but with the appropriate version numbers that will be compatible with other packages.
5.3. pip install --force-reinstall --no-cache-dir -r requirements.txt
# or
# 5.3. pip install -r requirements.txt

# Somehow when I executed "pip install lws" after executing "pip intalled -r requirements.txt", I got an error stating some packages are not available and then I executed "pip check" to find that mkl and fsspec were missing (no idea why and why are they not in the original requirements.txt and I did not venture on trying to add it there and retrying the steps but executed the below 2 commands)
6.1 pip install --force-reinstall --no-cache-dir "mkl>=2021.1.1,<=2021.4.0"
6.2 pip install fsspec

7. pip install lws

# The original README.md had the below command to be executed to install ffmpeg but that did not work for me and what worked for me are the steps that are given below the next line.
# 8. conda install -c conda-forge ffmpeg
8.1 Go to https://ffmpeg.org/download.html.
8.2. Select the Windows icon in the section "Get packages & executable files".
8.3 Select any of the source under the section "Windows EXE Files".
8.4. A zip file like "ffmpeg-master-latest-win64-gpl.zip" will get downloaded onto your system.
8.5. Unzip the zip file in a location of your choice. Let us say you have unzipped the zip file in C:\ffmpeg-master-latest-win64-gpl.
8.6. Add the path C:\ffmpeg-master-latest-win64-gpl\bin in the Path environment variable.
8.7. Open a new command prompt and execute the command "ffmpeg -version".
8.8. If you do not see an error, that means that ffmpeg is now ready to be used.

# The original README.md also asks the below package to be installed but the video explaining the HOW TO does not ask the below to be installed and I tried once and got an error on executing the below command so ignored it but the project finally ran alright for me so, we can ignore the package on the next line.
# 9. pip install face-alignment
```

* Download the pre-trained [checkpoints](https://drive.google.com/file/d/1Zehr3JLIpzdg2S5zZrhIbpYPKF-4gKU_/view?usp=sharing).

* Create the default folder ```./checkpoints``` and 
unzip the ```demo.zip``` at ```./checkpoints/demo```. There should be 5 ```pth```s in it.

* Go to the ```misc``` folder in the project's root folder and unzip all ```*.zip``` files within the same (```misc```) folder. There are the below 4 zip files in the ```misc``` folder:
  1. Audio_Source.zip
  2. Input.zip
  3. Mouth_Source.zip
  4. Pose_Source.zip
* Unzip the above 4 zip files and you should have 4 new folders with names as stated below. Also, please keep in mind that each of the below 4 folders should have the same folder name inside them and should have folders and/or files that start with some number/s:
  1. Audio_Source
  2. Input
  3. Mouth_Source
  4. Pose_Source
* We are all set to run the demo using the below command:
``` 
python inference.py --name demo --meta_path_vox misc/demo.csv --dataset_mode voxtest --netG modulate --netA resseaudio --netA_sync ressesync --netD multiscale --netV resnext --netE fan --model av --gpu_ids 0 --clip_len 1 --batchSize 16 --style_dim 2560 --nThreads 4 --input_id_feature --generate_interval 1 --style_feature_loss --use_audio 1 --noise_pose --driving_pose --gen_video --generate_from_audio_only
```

<img src='./misc/output.gif' width=400>

From left to right are the *reference input*, the *generated results*,
the *pose source video* and the *synced original video* with the driving audio.

# All the below content is from the original README.md.

## Prepare Testing Your Own Images/Videos

Check out this tutorial video for a clear demonstration

All of these steps can be done with the `prepare_testing_files.py`. However, the codes can't consistently run on Windows, so I suggest manually setting up. Hence, all below steps are manual setups. Please refer to the original branch for running the script `prepare_testing_files.py` if you want to do that instead. 

Example combos to run this AI:
| description | combo |
| :-: | :-: |
|make 1 video talk, with head movements and extra mouth reference|Input: x.mp4<br>Audio Source: y.mp4<br>Pose Source: z.mp4|
|make 1 image talk, with head movements and extra mouth reference|Input: x.jpg<br>Audio Source: y.mp4<br>Pose Source: z.mp4|
|make 1 image talk, no head movements and extra mouth reference|Input: x.jpg<br>Audio Source: y.mp4<br>Pose Source: x.jpg|
|make 1 image talk, no head movements|Input: x.jpg<br>Audio Source: y.mp3<br>Pose Source: x.jpg|

**If the Audio Source is `mp4`, Extract the `mp3` out of the `mp4`.** So you have 2 files.

All the following steps assume all mp4s are in 30 fps.

### Setup Audio_Source

* Drag and drop your mp3 at `misc/Audio_Source`
<br />

### Setup Mouth_Source **Skip this step if your Audio Source is a mp3**

* Drag and drop your mp4 at `misc/Mouth_Source` IF Audio Source was a `mp4`, and create a folder at `misc/Mouth_Source` with the name of your mp4 file
* Change the `x` (2 occurences) to your mp4's name in the command below, and enter it
```
ffmpeg -i misc/Mouth_Source/x.mp4 -vf fps=30 misc/Mouth_Source/x/%06d.jpg
```
<br />

### Setup Input

* Drag and drop your input image/video in `misc/Input`, and create a folder at `misc/Input` with the name of your mp4/jpg file
* **If your input is a video**, change the `y` (2 occurences) to your mp4's name in the command below, and enter it
```
ffmpeg -i misc/Input/y.mp4 -vf fps=30 misc/Input/y/%06d.jpg
```
* **If your input is an image**, drag and drop the image inside the folder. Rename the image to `000000.jpg`
<br />

### Setup Pose_Source

* Drag and drop your pose image/video `misc/Pose_Source`, and create a folder at `misc/Pose_Source` with the name of your mp4/jpg file
* **If your input is a video**, change the `z` (2 occurences) to your mp4's name in the command below, and enter it
```
ffmpeg -i misc/Pose_Source/z.mp4 -vf fps=30 misc/Pose_Source/z/%06d.jpg
```
* **If your input is an image**, drag and drop the image inside the folder. Rename the image to `000000.jpg`
<br />


### Align Frames
After the drag and drop steps, run each of these commands (replace the `x`, `y`, `z` to the right names)
```
python scripts/align_68.py --folder_path misc/Mouth_Source/x
python scripts/align_68.py --folder_path misc/Input/y
python scripts/align_68.py --folder_path misc/Pose_Source/z
```
If you get the error `preprocessing failed`, it means some of the frames can't detect faces. One way to fix it is to shorten the video where the faces are visible.

New folders called `x_cropped`, `y_cropped`, `z_cropped` will be created.

<br />

### Conditional: Stablize aligned videos
If your aligned faces are really shaky when put back into a video, you can stablize the aligned faces by putting the frames together with

Mouth_Source (replace the `x` with the corresponding name)
```
ffmpeg -i misc/Mouth_Source/x_cropped/%06d.jpg -vf fps=30 misc/Mouth_Source/x_aligned_stabled.mp4
```

Input (replace the `y` with the corresponding name)
```
ffmpeg -i misc/Input/y_cropped/%06d.jpg -vf fps=30 misc/Input/y_aligned_stabled.mp4
```

Pose_Source (replace the `z` with the corresponding name)
```
ffmpeg -i misc/Pose_Source/z_cropped/%06d.jpg -vf fps=30 misc/Pose_Source/z_aligned_stabled.mp4
```

Stablizes the videos with [this](https://www.stabilizo.com/)

After stablizing them, replace the corresponding mp4s. (eg. replace `z_aligned_stabled.mp4` with the actual stablized mp4)

Mouth_Source
```
ffmpeg -i misc/Mouth_Source/x_aligned_stabled.mp4 -vf fps=30 misc/Mouth_Source/x_aligned_stabled/%06d.jpg
```

Input
```
ffmpeg -i misc/Input/y_aligned_stabled.mp4 -vf fps=30 misc/Input/y_aligned_stabled/%06d.jpg
```

Pose_Source
```
ffmpeg -i misc/Pose_Source/z_aligned_stabled.mp4 -vf fps=30 misc/Pose_Source/z_aligned_stabled/%06d.jpg
```
<br />

### Setup demo.csv

* open the file demo.csv with notepad
* Count the amount of frames in each `x_cropped`, `y_cropped`, `z_cropped` folder
* Change the content accordingly:

| description | &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; combo &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;| demo.csv |
| :-: | :-: | :-: |
|make 1 video talk, with head movements and extra mouth reference|**Input:** x.mp4<br>**Audio Source:** y.mp4<br>**Pose Source:** z.mp4|`misc/Input/x_cropped _x_NUMBER_OF_FRAMES_HERE_ misc/Pose_Source/z_cropped _z_NUMBER_OF_FRAMES_HERE_ misc/Audio_Source/y.mp3 misc/Mouth_Source/y_cropped _y_NUMBER_OF_FRAMES_HERE_ dummy`|
|make 1 image talk, with head movements and extra mouth reference|**Input:** x.jpg<br>**Audio Source:** y.mp4<br>**Pose Source:** z.mp4|`misc/Input/x_cropped 1 misc/Pose_Source/z_cropped _z_NUMBER_OF_FRAMES_HERE_ misc/Audio_Source/y.mp3 misc/Mouth_Source/y_cropped _y_NUMBER_OF_FRAMES_HERE_ dummy`|
|make 1 image talk, no head movements and extra mouth reference|**Input:** x.jpg<br>**Audio Source:** y.mp4<br>**Pose Source:** x.jpg|`misc/Input/x_cropped 1 misc/Pose_Source/z_cropped _z_NUMBER_OF_FRAMES_HERE_ misc/Audio_Source/y.mp3 misc/Mouth_Source/y_cropped _y_NUMBER_OF_FRAMES_HERE_ dummy`|
|make 1 image talk, no head movements|**Input:** x.jpg<br>**Audio Source:** y.mp3<br>**Pose Source:** x.jpg|`misc/Input/x_cropped 1 misc/Input/x_cropped 1 misc/Audio_Source/y.mp3 None 0 dummy`|

### Run
After demo.csv is done setting up, run the codes with this line of command:
```
python inference.py --name demo --meta_path_vox misc/demo.csv --netG modulate --netA resseaudio --netA_sync ressesync --netD multiscale --netV resnext --netE fan --model av --gpu_ids 0 --clip_len 1 --batchSize 16 --style_dim 2560 --nThreads 4 --input_id_feature --generate_interval 1 --style_feature_loss --use_audio 1 --noise_pose --gen_video --driving_pose --generate_from_audio_only
```
The results will be in the results folder. 


## License and Citation

The usage of this software is under [CC-BY-4.0](https://github.com/Hangz-nju-cuhk/Talking-Face_PC-AVS/LICENSE).
```
@InProceedings{zhou2021pose,
author = {Zhou, Hang and Sun, Yasheng and Wu, Wayne and Loy, Chen Change and Wang, Xiaogang and Liu, Ziwei},
title = {Pose-Controllable Talking Face Generation by Implicitly Modularized Audio-Visual Representation},
booktitle = {Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
year = {2021}
}
```

## Acknowledgement
* The structure of this codebase is borrowed from [SPADE](https://github.com/NVlabs/SPADE).
* The generator is borrowed from [stylegan2-pytorch](https://github.com/rosinality/stylegan2-pytorch).
* The audio encoder is borrowed from [voxceleb_trainer](https://github.com/clovaai/voxceleb_trainer).
