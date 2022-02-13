#This is an example of multiple scripts used to run a complete backup of a linux and windows file share to an unmounted encrypted disk on a linux box. 


#!/bin/bash

#mount Luks encrypted disk
cryptsetup luksOpen /dev/mapper/centos-Backup--Data DATA
mount /dev/mapper/DATA /DATA

#mount Windows network shares
bash /DATA/Mount_Win_drives.sh


#rsync script
bash /DATA/Rsync_job.sh

echo ">----------- BACKUP COMPLETE ----------<"

#unmount Windows Network Drives
umount /mnt/DATA/
umount /mnt/VirtualMachine/

echo "Windows Network Drives unmounted!"

#unmount Luks Mount
umount /DATA
cryptsetup luksClose DATA

echo "Encrypted drive unmounted!"



#TARGET SCRIPTS (which exist on a encrypted and unmounted drive outside of active backup)
#Mount_Win_drives.sh

#!/bin/bash
mount -t cifs -o username=xxx,password=xxx,domain=DELLR310 //192.168.10.7/DATA /mnt/DATA/
mount -t cifs -o username=xxx,password=xxx,domain=DELLR310 //192.168.10.7/VirtualMachine /mnt/VirtualMachine/
echo "Windows Network Drives Mounted!"


#Rsync_job.sh

#!/bin/bash
#rsync job

echo "Samba Server Rsync in progress!"
sudo sshpass -p "xxx" rsync -atvp --delete --progress -e "ssh -o StrictHostKeyChecking=no" xxx@10.1.1.6:/DATA/ /DATA/UserData/
echo "Proxmox Server Rsync in progress!"
sudo sshpass -p "xxx" rsync -atvp --delete --progress -e "ssh -o StrictHostKeyChecking=no" xxx@10.1.1.3:/mnt/pve/Backup_ISO_Storage/ /DATA/ProxmoxSnapshotBackup/
sudo sshpass -p "xxx" rsync -atvp --delete --progress -e "ssh -o StrictHostKeyChecking=no" xxx@10.1.1.3:/mnt/pve/VM_Storage01/ /DATA/ProxmoxVmBackup/

