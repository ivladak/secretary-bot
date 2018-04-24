dev=/dev/sda1
[ -e "$dev" ] || dev=/dev/sdb1
sudo hdparm -S 1 "$dev"
