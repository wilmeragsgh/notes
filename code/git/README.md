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

**Adding empty folder to git**

Create a `.gitignore` at the root of such folder and place the following content there:

```bash
# Ignore everything in this directory
*
# Except this file
!.gitignore
```

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

```bash
git reset --soft HEAD^
```

or

```bash
git reset --soft HEAD~1
```

Then reset the unwanted files in order to leave them out from the commit:

```bash
git reset HEAD path/to/unwanted_file
```

Now commit again, you can even re-use the same commit message:

```bash
git commit -c ORIG_HEAD
```

**Git global setup**

```bash
git config --global user.name "NAME"
git config --global user.email "EMAIL"
```

**Create a new repository**

```bash
git clone repo_address
cd repo_name
touch README.md
git add README.md
git commit -m "add README"
git push -u origin master
```

**Push an existing folder**

```bash
cd existing_folder
git init
git remote add origin repo_address
git add .
git commit -m "Initial commit"
git push -u origin master
```

**Push an existing Git repository**

```bash
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

**Fix undesired push files**

```bash
git reset --soft HEAD~8
git reset .
git add (all the files you want to commit, excluding the secrets this time)
git commit -m "My new comment that encompasses the last 8 commits"
git push -f
```

1. Replace the example commit `04833737604b1bf98ed65cf940eb79ff069771ff` with the commit you want to revert to. This should be the commit right before you committed the secrets. This will revert all the commits up to the commit you specified, while keeping all your changes staged in local
2. Unstages all the changes you just reset
3. Add the files you want to the commit
4. Commit your changes
5. Force your new local repo changes to overwrite the remote repo, effectively getting rid of the secrets you accidentally committed


**Commit specific changes of a file**

```bash
git add -p FILE
# then select y for the wanted changes, s to split a chunk of code and n/q to skip or quit the process
```

**Remove a file to not check its update going forward**

```bash
git update-index --assume-unchanged .dvc/config
# git update-index --no-assume-unchanged # (reverse)
```

> More info on this [stackoverflow](https://stackoverflow.com/questions/3319479/can-i-git-commit-a-file-and-ignore-its-content-changes)

**commits**

Try to keep the convention:

 bug fix, a feature, change to the documentation, etc. as prefix to subject (fix, feat, doc).


## References

- https://chris.beams.io/posts/git-commit/
- https://udacity.github.io/git-styleguide/
- https://linuxhint.com/git_blame/
