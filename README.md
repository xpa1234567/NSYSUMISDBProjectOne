# MSI_DB_ProjectOne


### 1. 建立環境
```bash!	
# install package:pipenv
pip install --user pipenv

# check package loaction
python3 -m site --user-base
#/home/kim/.local

# Add package loaction path to PATH
sudo vi /etc/profile

export PATH=${PATH}:/home/kim/.local

# Restart console
# cd 至git clone資料夾內
cd ProjectOne/

# 虛擬環境建立和安裝套件
pipenv install

# 成功安裝會顯示以下內容
Creating a virtualenv for this project...
Pipfile: /home/kim/ProjectOne/Pipfile
Using /usr/bin/python3 (3.10.12) to create virtualenv...
⠙ Creating virtual environment...created virtual environment CPython3.10.12.final.0-64 in 162ms
  creator CPython3Posix(dest=/home/kim/.local/share/virtualenvs/ProjectOne-Ob362hMD, clear=False, no_vcs_ignore=False, global=False)
  seeder FromAppData(download=False, pip=bundle, setuptools=bundle, wheel=bundle, via=copy, app_data_dir=/home/kim/.local/share/virtualenv)
    added seed packages: pip==23.2.1, setuptools==68.2.0, wheel==0.41.2
  activators BashActivator,CShellActivator,FishActivator,NushellActivator,PowerShellActivator,PythonActivator
✔ Successfully created virtual environment!

```

:bulb:  pipenv install，會根據當下路徑的Pipfile內容安裝
![image](https://github.com/MISDBProject/ProjectOne/blob/main/readmepic/pipfile.png)

成功安裝截圖：
![image](https://github.com/MISDBProject/ProjectOne/blob/main/readmepic/pipfileinstallsuccess.png)


### 2. 環境檢查及使用
##### 安裝python套件

> 可先執行pip3 list，確認套件是否有差異
> pip3 list
>

![image](https://github.com/MISDBProject/ProjectOne/blob/main/readmepic/piplistbefore.png)

啟動虛擬環境
>pipenv shell
>pip3 list

確認套件是否有差異
![image](https://github.com/MISDBProject/ProjectOne/blob/main/readmepic/piplistafter.png)


### 3. 啟動程式
```python=
python3 app.py
```
