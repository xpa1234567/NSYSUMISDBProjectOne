# MSI_DB_ProjectOne

>Due Date：<font color="#f00">**2023/11/14**</font>
Language：Python
DBMS：Oracle
OS：Ubuntu-22.04(FROM WSL2)

## INSTALL
### 1. Get Repo From Github Organization
New Toekn(classic)

![image](https://github.com/MISDBProject/ProjectOne/blob/main/readmepic/github_token.png)

```bash!=
sudo apt install git 
    git config --global core.editor "vim"
    git config --global user.email "you@example.com"
    git config --global user.name "Your Name"
  
sudo apt install gh

```

上述產生的Token這邊用，gh auth login  [參考](https://cli.github.com/manual/gh_auth_login)

```bash!=
kim@DESKTOP-I6UQI6R:~$ gh auth login
? What account do you want to log into? GitHub.com
? What is your preferred protocol for Git operations? HTTPS
? Authenticate Git with your GitHub credentials? Yes
? How would you like to authenticate GitHub CLI? Paste an authentication token
Tip: you can generate a Personal Access Token here https://github.com/settings/tokens
The minimum required scopes are 'repo', 'read:org', 'workflow'.
? Paste your authentication token: ****************************************
- gh config set -h github.com git_protocol https
✓ Configured git protocol
✓ Logged in as xpa1234567
```
即可git clone
```bash!=
git clone https://github.com/MISDBProject/ProjectOne.git
```