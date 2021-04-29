# This is a Windows 10 guide to install & run PC-AVS
Codes and guides are slightly modified

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


## Quick Start: Generate Demo Results
Clone the repository
Run anaconda3 prompt and run each of these commands to setup the environment
```
cd *Path_To_PCAVS*
conda create -n PCAVS python=3.6
conda activate PCAVS
conda install pytorch==1.7.1 torchvision==0.8.2 torchaudio==0.7.2 cudatoolkit=10.2 -c pytorch
pip install -r requirements.txt
pip install lws
conda install -c menpo ffmpeg
pip install face-alignment
```

* Download the pre-trained [checkpoints](https://drive.google.com/file/d/1Zehr3JLIpzdg2S5zZrhIbpYPKF-4gKU_/view?usp=sharing).

* Create the default folder ```./checkpoints``` and 
unzip the ```demo.zip``` at ```./checkpoints/demo```. There should be 5 ```pth```s in it.

* Unzip all ```*.zip``` files within the ```misc``` folder.

* Run the demo:
``` 
python inference.py --name demo --meta_path_vox misc/demo.csv --dataset_mode voxtest --netG modulate --netA resseaudio --netA_sync ressesync --netD multiscale --netV resnext --netE fan --model av --gpu_ids 0 --clip_len 1 --batchSize 16 --style_dim 2560 --nThreads 4 --input_id_feature --generate_interval 1 --style_feature_loss --use_audio 1 --noise_pose --driving_pose --gen_video --generate_from_audio_only
```

<img src='./misc/output.gif' width=400>

From left to right are the *reference input*, the *generated results*,
the *pose source video* and the *synced original video* with the driving audio.

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

### Step up Audio_Source

* Drag and drop your mp3 at `misc/Audio_Source`
<br />

### Step up Mouth_Source **Skip this step if your Audio Source is a mp3**

* Drag and drop your mp4 at `misc/Mouth_Source` IF Audio Source was a `mp4`, and create a folder at `misc/Mouth_Source` with the name of your mp4 file
* Change the `x` (2 occurences) to your mp4's name in the command below, and enter it
```
ffmpeg -i misc/Mouth_Source/x.mp4 -vf fps=30 misc/Mouth_Source/x/%06d.jpg
```
<br />

### Step up Input

* Drag and drop your input image/video in `misc/Input`, and create a folder at `misc/Input` with the name of your mp4/jpg file
* **If your input is a video**, change the `y` (2 occurences) to your mp4's name in the command below, and enter it
```
ffmpeg -i misc/Input/y.mp4 -vf fps=30 misc/Input/y/%06d.jpg
```
* **If your input is an image**, drag and drop the image inside the folder. Rename the image to `000000.jpg`
<br />

### Step up Pose_Source

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

| description | combo | demo.csv |
| :-: | :-: | :-: |
|make 1 video talk, with head movements and extra mouth reference|**Input:** x.mp4<br>**Audio Source:** y.mp4<br>**Pose Source:** z.mp4|`misc/Input/y_cropped _y_NUMBER_OF_FRAMES_HERE_ misc/Pose_Source/z_cropped _z_NUMBER_OF_FRAMES_HERE_ misc/Audio_Source/x.mp3 misc/Mouth_Source/x_cropped _x_NUMBER_OF_FRAMES_HERE_ dummy`|
|make 1 image talk, with head movements and extra mouth reference|**Input:** x.jpg<br>**Audio Source:** y.mp4<br>**Pose Source:** z.mp4|`misc/Input/y_cropped 1 misc/Pose_Source/z_cropped _z_NUMBER_OF_FRAMES_HERE_ misc/Audio_Source/x.mp3 misc/Mouth_Source/x_cropped _x_NUMBER_OF_FRAMES_HERE_ dummy`|
|make 1 image talk, no head movements and extra mouth reference|**Input:** x.jpg<br>**Audio Source:** y.mp4<br>**Pose Source:** x.jpg|`misc/Input/y_cropped 1 misc/Pose_Source/z_cropped _z_NUMBER_OF_FRAMES_HERE_ misc/Audio_Source/x.mp3 misc/Mouth_Source/x_cropped _x_NUMBER_OF_FRAMES_HERE_ dummy`|
|make 1 image talk, no head movements|**Input:** x.jpg<br>**Audio Source:** y.mp3<br>**Pose Source:** x.jpg|`misc/Input/y_cropped 1 misc/Input/y_cropped 1 misc/Audio_Source/x.mp3 None 0 dummy`|

### Run
After demo.csv is done setting up, run the codes with this line of command:
```
python inference.py --name demo --meta_path_vox misc/demo.csv --netG modulate --netA resseaudio --netA_sync ressesync --netD multiscale --netV resnext --netE fan --model av --gpu_ids 0 --clip_len 1 --batchSize 16 --style_dim 2560 --nThreads 4 --input_id_feature --generate_interval 1 --style_feature_loss --use_audio 1 --noise_pose --gen_video --driving_pose --generate_from_audio_only
```
The results will be in the results folder. 



## Train Your Own Model
* Coming soon

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
