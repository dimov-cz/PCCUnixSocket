if [ ! -d venv ]; then
  #apt-get install python3-venv
  python3 -m venv venv || exit 1
fi

. venv/bin/activate
pip3 install -r requirements.txt

R="eLGate/Controllers/DeviceControllers/EpsonProjController/epLocal/requirements.txt"
if [ -f "$R" ]; then
  pip3 install -r "$R"
fi