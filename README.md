# csrs-llm-repo

## Technical Debugging

### How to use git (windows)

1. Install git
2. Right-click inside the repo directory and click on `open Git Bash here`
	- If this doesn't show up, open Git Bash via the start menu or whatever and use `cd ~/[path_to_directory]` to get to the repo directory
3. On the github repo, click on `code` and copy the HTTPS link
4. On Git Bash, type in `git pull` and ctrl+shift+insert (this replaces ctrl+V for whatever reason)
5. Hopefully it'll pull the github over but maybe instead you'll get a `refusing to merge unrelated histories` error. In that case look at [this link](https://stackoverflow.com/questions/45272492/git-is-refusing-to-merge-unrelated-histories-what-are-unrelated-histories) and try adding `--allow-unrelated-histories` after the HTTPS link
	- I haven't actually tried this yet, maybe it doesn't work, also note that the link mentions when you should or shouldn't perform an unrelated history merge. 
	- If you download the repo zip from github and get the latest repo from that then you'll probably get this error. Worst case scenario just keep doing that and don't bother with git lmao
6. Open the Git GUI and click on `Open Existing Repository` and browse to the repo folder
7. Click on `Stage Changed` and then `Commit` to save file changes to the repo
	- It'll probably yell at you about not being able to verify your identity and not having a commit message. Write your commit message in the designated box, and it'll give you instructions on how to verify your identity via Git Bash and github
8. Click on `Push` and put the HTTPS link in `Destination Repository`
	- ****DO NOT**** check `Force overwrite existing branch`. It does exactly what it says and will overwrite the entire github repo.