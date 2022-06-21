while true
do

# //// CONFIGURABLE VARIABLES ////////////

# pausetime between iterations
sleeptime=10

# get parent folder of file and activate its path_to_wallpapers variable
# secrets.sh MUST be in the same directory as this file
cur_dir=$(dirname "$0")
source $cur_dir/secrets.sh

# location of wallpapers folder
location=$path_to_wallpapers



# ////////////////////////////////////////

array=($(ls $location*)) # populate array with directory contents
#( IFS=$'\n'; echo "${array[*]}" ) # list array content for debug

size=${#array[@]}
index=$(($RANDOM % $size)) 
wallpaper=${array[$index]} # randomly select

#echo 
#echo " || SELLECTED WALLPAPER = "$wallpaper

dbus-send --session --dest=org.kde.plasmashell --type=method_call /PlasmaShell org.kde.PlasmaShell.evaluateScript 'string:
var Desktops = desktops();                                                                                                                       
for (i=0;i<Desktops.length;i++) {
        d = Desktops[i];
        d.wallpaperPlugin = "org.kde.image";
        d.currentConfigGroup = Array("Wallpaper",
                                    "org.kde.image",
                                    "General");
        d.writeConfig("Image", "file://'${wallpaper}'");
}'
sleep $sleeptime

done
