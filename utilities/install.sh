sudo pip install --upgrade pep8
sudo pip install --upgrade pyflakes
sudo pip install --upgrade pylint

sudo apt-get install -y build-essential openssh-server python-dev \
 python-yaml python-setuptools ipython python-pip

sudo apt-get install -y dpkg-dev build-essential swig python2.7-dev \
 libwebkitgtk-dev libjpeg-dev libtiff-dev freeglut3 freeglut3-dev \
 libgtk2.0-dev libsdl1.2-dev libgstreamer-plugins-base0.10-dev

cd /tmp
wget http://downloads.sourceforge.net/project/wxpython/wxPython/3.0.0.0/wxPython-src-3.0.0.0.tar.bz2?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fwxpython%2Ffiles%2FwxPython%2F3.0.0.0%2F&ts=1407279525&use_mirror=softlayer-dal
mv wxPython-src-3.0.0.0.tar.bz2\?r\=http\:%2F%2Fsourceforge.net%2Fprojects%2Fwxpython%2Ffiles%2FwxPython%2F3.0.0.0%2F wxPythonsrc.tar.bz2

tar xjvf wxPythonsrc.tar.bz2

cd wxPython-src-3.0.0.0/wxPython/
sudo python build-wxpython.py --build_dir=../bld --install

echo "export LD_LIBRARY_PATH=\${LD_LIBRARY_PATH}:/usr/local/lib" >> ~/.bashrc 
