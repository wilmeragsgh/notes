---
description: Frequently used git snippets
---

# Git

**Commands**

`git add <file>` Add new file to stage area

`git diff` Check changes on repo

**Terms**

`HEAD` Reference to the last commit

**Check last commits**

`git log`

**Situations**

When going from develop to master tagged with release number

**When creating new features branch from develop**

`git checkout -b [name_of_your_new_branch] develop`

**Then, normally finishing with:**

`git push origin [name_of_your_new_branch]`

**Merging back to develop:**

```bash
git checkout develop
git merge --no-ff [name_of_new_branch]
git branch -d [name_of_new_branch]
git push origin develop
```

> note: `--no-ff` create new commit with the merge

**When creating a release \(branch for last minutes fixes for release from develop \)**

`git checkout -b release-[version] develop`

**Finishing with release branch**

`git checkout master`

`git merge --no-ff release-[version]`

`git tag -a [version]`

and then to develop

`git checkout develop`

`git merge --no-ff release-[version]`

finally

`git branch -d release-[version]`

**Fixing production issues:**

`git checkout -b hotfix-[version+0.0.1] master` 3 or release branch

`git commit -m 'Fixing severe bug'`

`git checkout master`

`git merge --no-ff hotfix-[version+0.0.1]`

`git branch -d hotfix-[version+0.0.1]`

**Rename branch**

`git checkout <old_name>`

`git branch -m <new_name>`

`git push origin --delete <old_name>`

`git push origin -u <new_name>`

**Check changes**

```bash
git diff HEAD [file]
```

**Undo commits**

```bash
git reset --hard HEAD^
git push origin -f
```

**Remove files from Git commit**

I think other answers here are wrong, because this is a question of moving the mistakenly committed files back to the staging area from the previous commit, without cancelling the changes done to them. This can be done like Paritosh Singh suggested:

```text
git reset --soft HEAD^
```

or

```text
git reset --soft HEAD~1
```

Then reset the unwanted files in order to leave them out from the commit:

```text
git reset HEAD path/to/unwanted_file
```

Now commit again, you can even re-use the same commit message:

```text
git commit -c ORIG_HEAD
```

**Git global setup**

```text
git config --global user.name "NAME"
git config --global user.email "EMAIL"
```

**Create a new repository**

```text
git clone repo_address
cd repo_name
touch README.md
git add README.md
git commit -m "add README"
git push -u origin master
```

**Push an existing folder**

```text
cd existing_folder
git init
git remote add origin repo_address
git add .
git commit -m "Initial commit"
git push -u origin master
```

**Push an existing Git repository**

```text
cd existing_repo
git remote rename origin old-origin
git remote add origin repo_address
git push -u origin --all
git push -u origin --tags
```

**git ignore**

```bash
folderA/ # would remove folderA anywhere in the repo
```
