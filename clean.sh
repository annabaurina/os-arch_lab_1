sudo umount test_directory
sudo losetup -d /dev/loop21
sudo rm /tmp/virtual_drive.img
sudo rm -rf test_directory
sudo rm /tmp/backup*.tar.gz