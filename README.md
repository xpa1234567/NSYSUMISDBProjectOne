# MSI_DB_ProjectOne

https://medium.com/@hiimdoublej/pipenv指令大全-6e4415cc8a15
Python版本切換
https://github.com/pyenv-win/pyenv-win

>- Due Date：<font color="#f00">**2023/11/14**</font>
>- Language：Python
>- DBMS：Oracle
>- OS：Ubuntu-22.04(FROM WSL2)

## INSTALL
### 1. Get Repo From Github Organization
New Toekn(classic)[參考](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

![image](https://github.com/MISDBProject/ProjectOne/blob/main/readmepic/github_token.png)

```bash!=
# Install git
sudo apt install git 

# git editor
git config --global core.editor "vim"

# git user email
git config --global user.email "you@example.com"

# git user email
git config --global user.name "Your Name"

#Install github CLI  
sudo apt install gh
```

gh auth login  [參考](https://cli.github.com/manual/gh_auth_login)
```bash!=
#使用上述產生的token登入Github
kim@DESKTOP-I6UQI6R:~$ gh auth login

? What account do you want to log into? 
# GitHub.com

? What is your preferred protocol for Git operations?
# HTTPS

? Authenticate Git with your GitHub credentials?
# Yes

? How would you like to authenticate GitHub CLI?
# Paste an authentication token

Tip: you can generate a Personal Access Token here https://github.com/settings/tokens
The minimum required scopes are 'repo', 'read:org', 'workflow'.

# 產生的token這邊用
? Paste your authentication token: ****************************************
- gh config set -h github.com git_protocol https

# 成功認證即可看到自己的帳號名稱
✓ Configured git protocol
✓ Logged in as xpa1234567
```
即可git clone
```bash!=
git clone https://github.com/MISDBProject/ProjectOne.git
```

### 2. 建立環境
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


### 3. 環境檢查及使用
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


### 4. 啟動程式
```python=
python3 app.py
```
