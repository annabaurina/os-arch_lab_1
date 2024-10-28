#!/bin/bash

#делаем папку ограниченой по размеру

dir_name="$1" 
size_in_mb="$2"

touch /tmp/virtual_drive.img
truncate -s "${size_in_mb}M" /tmp/virtual_drive.img

loop_device=$(sudo losetup -f --show /tmp/virtual_drive.img)
echo ${loop_device}
sudo mkfs.ext4 ${loop_device}

sudo mount ${loop_device} ${dir_name}
sudo rm -rf ${dir_name}/lost+found

echo Virtual drive \(loopback device ${loop_device}\) created and mounted to ${dir_name} with size ${size_in_mb}MB.

