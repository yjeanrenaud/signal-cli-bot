#! /bin/sh

set -e

echo "Installing yj_signalbot_regular\n"
sudo cp yj_signalbot_regular.py /usr/local/bin/
sudo chmod a+x /usr/local/bin/yj_signalbot_regular.py
sudo cp yj_signal_bot_wrapper.sh /usr/local/bin/
sudo chmod a+x /usr/local/bin/yj_signal_bot_wrapper.sh


echo "installing init.d script\n"
sudo cp yj_signal_bot_init.sh /etc/init.d/
sudo chmod a+x /etc/init.d/yj_signal_bot_init.sh

echho "starting signalbot in a separate screen\n"
sudo update-rc.dyj_signal_bot_init.sh defaults
sudo /etc/init.d/yj_signal_bot_init.sh start

echo "all done\n"
