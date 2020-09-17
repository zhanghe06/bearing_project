# Git

## Install

[安装说明](https://git-scm.com/book/zh/v2/%E8%B5%B7%E6%AD%A5-%E5%AE%89%E8%A3%85-Git)


## commit

git log prefix
```
Project Initialization
Create
Update
Delete
Fix
```

## git 开发流程

以下流程的原则：本地不能直接修改 master 分支，仅仅作为主干分支

注意`主干分支`与`开发分支`的区别

### 开新分支
```
$ git checkout master
$ git pull origin master
$ git checkout -b dev
```

### 更新本地分支
```
$ git checkout dev
$ git add .
$ git commit -m "更新dev分支"
```

### 合并分支（`本地主干分支`合并到`本地开发分支`）

#### merge 方式

合并分支
```
$ git checkout master
$ git pull origin master
$ git checkout dev
$ git merge master
```

解决冲突
```
$ git add .
$ git commit -m "合并dev分支"
```

#### rebase 方式

合并分支
```
$ git checkout master
$ git pull --rebase origin master
$ git checkout dev
$ git rebase master
```

解决冲突
```
$ git add .
$ git rebase --continue
```

注意：
使用`rebase`合并，修改冲突后的提交，`rebase --continue` 替代 `commit`

### 合并分支（`本地主干分支`合并到`远程主干分支`）
```
$ git checkout master
$ git fetch origin master
$ git rebase origin/master
```

### 演示流程

模拟 新开分支，解决冲突，合并分支

通过 graph 可以看出，主干分支不会出现交叉

```
➜  ~ cd code
➜  code git clone git@gitee.com:v__v/test.git test_rebase
Cloning into 'test_rebase'...
The authenticity of host 'gitee.com (120.55.226.24)' can't be established.
ECDSA key fingerprint is SHA256:FQGC9Kn/eye1W8icdBgrQp+KkGYoFgbVr17bmjey0Wc.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'gitee.com' (ECDSA) to the list of known hosts.
remote: Counting objects: 3, done.
remote: Total 3 (delta 0), reused 0 (delta 0)
Receiving objects: 100% (3/3), done.
➜  code cd test_rebase
➜  test_rebase git:(master) git st
On branch master
Your branch is up-to-date with 'origin/master'.
nothing to commit, working tree clean
➜  test_rebase git:(master) git br
* master
➜  test_rebase git:(master) git br -a
* master
  remotes/origin/HEAD -> origin/master
  remotes/origin/master
➜  test_rebase git:(master) git co -b dev
Switched to a new branch 'dev'
➜  test_rebase git:(dev) git br -a
* dev
  master
  remotes/origin/HEAD -> origin/master

  remotes/origin/master
➜  test_rebase git:(dev) ls
README.md
➜  test_rebase git:(dev) cat README.md
# test
git 测试%
➜  test_rebase git:(dev) echo "git 测试 dev" > README.md
➜  test_rebase git:(dev) ✗ git st
On branch dev
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

	modified:   README.md

no changes added to commit (use "git add" and/or "git commit -a")
➜  test_rebase git:(dev) ✗ git add .
➜  test_rebase git:(dev) ✗ git ci -m 'dev更新README'
[dev 087e069] dev更新README
 1 file changed, 1 insertion(+), 2 deletions(-)
➜  test_rebase git:(dev) git st
On branch dev
nothing to commit, working tree clean
➜  test_rebase git:(dev) git co master
Switched to branch 'master'
Your branch is up-to-date with 'origin/master'.
➜  test_rebase git:(master) ls
README.md
➜  test_rebase git:(master) cat README.md
# test
git 测试% 
➜  test_rebase git:(master) echo "git 测试 master" > README.md
➜  test_rebase git:(master) ✗ git add .
➜  test_rebase git:(master) ✗ git ci -m 'master更新README'
[master 030d108] master更新README
 1 file changed, 1 insertion(+), 2 deletions(-)
➜  test_rebase git:(master) git co dev
Switched to branch 'dev'
➜  test_rebase git:(dev) git log --graph | cat
* commit 6b2b6c49f0b56a6dd600dfa7d0e77e8088d4a7ff
| Author: Zhang He <zhang_he06@163.com>
| Date:   Wed Oct 11 18:20:38 2017 +0800
|
|     dev更新README
|
* commit 074cfc25cbfea99e486b57c3fdd8b2cddcd384d8
  Author: 空ping子 <zhendime@gmail.com>
  Date:   Wed Oct 11 18:15:28 2017 +0800

      Initial commit
➜  test_rebase git:(dev) git rebase master
First, rewinding head to replay your work on top of it...
Applying: dev更新README
Using index info to reconstruct a base tree...
M	README.md
Falling back to patching base and 3-way merge...
Auto-merging README.md
CONFLICT (content): Merge conflict in README.md
error: Failed to merge in the changes.
Patch failed at 0001 dev更新README
The copy of the patch that failed is found in: .git/rebase-apply/patch

When you have resolved this problem, run "git rebase --continue".
If you prefer to skip this patch, run "git rebase --skip" instead.
To check out the original branch and stop rebasing, run "git rebase --abort".

➜  test_rebase git:(030d108) ✗ git st
rebase in progress; onto 030d108
You are currently rebasing branch 'dev' on '030d108'.
  (fix conflicts and then run "git rebase --continue")
  (use "git rebase --skip" to skip this patch)
  (use "git rebase --abort" to check out the original branch)

Unmerged paths:
  (use "git reset HEAD <file>..." to unstage)
  (use "git add <file>..." to mark resolution)

	both modified:   README.md

no changes added to commit (use "git add" and/or "git commit -a")
➜  test_rebase git:(030d108) ✗ cat README.md
<<<<<<< HEAD
git 测试 master
=======
git 测试 dev
>>>>>>> dev更新README
➜  test_rebase git:(030d108) ✗ echo "git 测试 dev merge" > README.md
➜  test_rebase git:(030d108) ✗ git st
rebase in progress; onto 030d108
You are currently rebasing branch 'dev' on '030d108'.
  (fix conflicts and then run "git rebase --continue")
  (use "git rebase --skip" to skip this patch)
  (use "git rebase --abort" to check out the original branch)

Unmerged paths:

  (use "git reset HEAD <file>..." to unstage)
  (use "git add <file>..." to mark resolution)

	both modified:   README.md

no changes added to commit (use "git add" and/or "git commit -a")
➜  test_rebase git:(030d108) ✗ git add .
➜  test_rebase git:(030d108) ✗ git st
rebase in progress; onto 030d108
You are currently rebasing branch 'dev' on '030d108'.
  (all conflicts fixed: run "git rebase --continue")

Changes to be committed:
  (use "git reset HEAD <file>..." to unstage)

	modified:   README.md

➜  test_rebase git:(030d108) ✗ git rebase --continue
Applying: dev更新README
➜  test_rebase git:(dev) git st
On branch dev
nothing to commit, working tree clean
➜  test_rebase git:(dev) git log --graph | cat
* commit 6b2b6c49f0b56a6dd600dfa7d0e77e8088d4a7ff
| Author: Zhang He <zhang_he06@163.com>
| Date:   Wed Oct 11 18:20:38 2017 +0800
|
|     dev更新README
|
* commit 030d10849d1ab4163f75fdcdf030ba3aded52404
| Author: Zhang He <zhang_he06@163.com>
| Date:   Wed Oct 11 18:21:33 2017 +0800
|
|     master更新README
|
* commit 074cfc25cbfea99e486b57c3fdd8b2cddcd384d8
  Author: 空ping子 <zhendime@gmail.com>
  Date:   Wed Oct 11 18:15:28 2017 +0800

      Initial commit
➜  test_rebase git:(dev) git diff master | cat
diff --git a/README.md b/README.md
index 297160d..6fbe460 100644
--- a/README.md
+++ b/README.md
@@ -1 +1 @@
-git 测试 master
+git 测试 dev merge
➜  test_rebase git:(dev) git co master
Switched to branch 'master'
Your branch is ahead of 'origin/master' by 1 commit.
  (use "git push" to publish your local commits)
➜  test_rebase git:(master) git merge dev
Updating 030d108..6b2b6c4
Fast-forward
 README.md | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
➜  test_rebase git:(master) git log --graph | cat
* commit 6b2b6c49f0b56a6dd600dfa7d0e77e8088d4a7ff
| Author: Zhang He <zhang_he06@163.com>
| Date:   Wed Oct 11 18:20:38 2017 +0800
|
|     dev更新README
|
* commit 030d10849d1ab4163f75fdcdf030ba3aded52404
| Author: Zhang He <zhang_he06@163.com>
| Date:   Wed Oct 11 18:21:33 2017 +0800
|
|     master更新README
|
* commit 074cfc25cbfea99e486b57c3fdd8b2cddcd384d8
  Author: 空ping子 <zhendime@gmail.com>
  Date:   Wed Oct 11 18:15:28 2017 +0800

      Initial commit
```


对比一下简单粗暴的 merge 方式

产生了一个无意义的 Merge

```
➜  code git clone git@gitee.com:v__v/test.git test_merge
Cloning into 'test_merge'...
remote: Counting objects: 3, done.
remote: Total 3 (delta 0), reused 0 (delta 0)
Receiving objects: 100% (3/3), done.
➜  code cd test_merge
➜  test_merge git:(master) ls
README.md
➜  test_merge git:(master) git co -b dev
Switched to a new branch 'dev'
➜  test_merge git:(dev) cat README.md
# test
git 测试%                                                                                                                                                                         ➜  test_merge git:(dev) echo "git 测试 dev" > README.md
➜  test_merge git:(dev) ✗ git add .
➜  test_merge git:(dev) ✗ git ci -m 'dev更新README'
[dev 6c85b19] dev更新README
 1 file changed, 1 insertion(+), 2 deletions(-)
➜  test_merge git:(dev) git co master
Switched to branch 'master'
Your branch is up-to-date with 'origin/master'.
➜  test_merge git:(master) echo "git 测试 master" > README.md
➜  test_merge git:(master) ✗ git add .
➜  test_merge git:(master) ✗ git ci -m 'master更新README'
[master 44aa754] master更新README
 1 file changed, 1 insertion(+), 2 deletions(-)
➜  test_merge git:(master) git co dev
Switched to branch 'dev'
➜  test_merge git:(dev) git merge master
Auto-merging README.md
CONFLICT (content): Merge conflict in README.md
Automatic merge failed; fix conflicts and then commit the result.
➜  test_merge git:(dev) ✗ git st
On branch dev
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)

	both modified:   README.md

no changes added to commit (use "git add" and/or "git commit -a")
➜  test_merge git:(dev) ✗ echo "git 测试 dev merge" > README.md
➜  test_merge git:(dev) ✗ git st
On branch dev
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)

	both modified:   README.md

no changes added to commit (use "git add" and/or "git commit -a")
➜  test_merge git:(dev) ✗ git add .
➜  test_merge git:(dev) ✗ git st
On branch dev
All conflicts fixed but you are still merging.
  (use "git commit" to conclude merge)

Changes to be committed:

	modified:   README.md

➜  test_merge git:(dev) ✗ git ci -m 'dev Merge README'
[dev 0e8fa0e] dev Merge README
➜  test_merge git:(dev) git st
On branch dev
nothing to commit, working tree clean
➜  test_merge git:(dev) git log --graph | cat
*   commit 0e8fa0ed7ce77827cec82bdda1fcca42c3a22330
|\  Merge: 6c85b19 44aa754
| | Author: Zhang He <zhang_he06@163.com>
| | Date:   Wed Oct 11 19:14:44 2017 +0800
| |
| |     dev Merge README
| |
| * commit 44aa75419691f7496d4e2d6c37c0eb6098078ed2
| | Author: Zhang He <zhang_he06@163.com>
| | Date:   Wed Oct 11 19:12:54 2017 +0800
| |
| |     master更新README
| |
* | commit 6c85b190593fb39e6fc3490675983f04dfb10d89
|/  Author: Zhang He <zhang_he06@163.com>
|   Date:   Wed Oct 11 19:12:12 2017 +0800
|
|       dev更新README
|
* commit 074cfc25cbfea99e486b57c3fdd8b2cddcd384d8
  Author: 空ping子 <zhendime@gmail.com>
  Date:   Wed Oct 11 18:15:28 2017 +0800

      Initial commit
```

## 总结

所有直接操作`git pull origin <branch>`都有合并产生冲突的可能

拉取代码 - 终止不能快速演进的操作（即终止有冲突的操作）
```
$ git pull --ff-only origin <branch>
```

拉取代码 - 变基
```
$ git pull --rebase origin <branch>
```

协同开发规范:

当一个特性分支在`review`状态时, 开新分支需要基于远程主干分支:
```
$ git checkout -b origin/<branch>
```
假设`review`中的代码被驳回, 如果其他进行中的分支是基于`review`状态时本地分支创建的, 其他分支就带上了非期望的代码。


分支模型(master - hotfix - develop - feature - release)

参考 http://blog.csdn.net/hherima/article/details/50386011


分支类型 | 本地分支 | 创建分支 | 更新本地分支
--- | --- | --- | ---
主分支 | master | git co -b origin/master | git pull origin master --rebase
开发分支 | develop | git co -b develop origin/master | git pull origin develop --rebase
发布分支 | release | git co -b release origin/master | git pull origin release --rebase
功能分支 | feature | git co -b feature origin/master | git pull origin feature --rebase
热修复分支 | hotfix | git co -b hotfix origin/master | git pull origin master --rebase

hotfix 分支说明
```
# 除非 hotfix 分支被确认合并到 master 分支, 否则本地 hotfix 分支不要删除

# 创建新分支
git fetch origin master
git co -b hotfix origin/master

# 提交修复(防止 master 分支上带有被驳回的其它 hotfix 代码)
git br -D master
git fetch origin master
git co -b master origin/master
git co hotfix
...                             # 开发
git ci -m '初次修复'
git rebase master
git rebase --continue           # 解决冲突, 继续变基
git co master
git rebase hotfix               # 合并代码
git pull --rebase origin master # 变基远程主干
git review master               # 提交评审

# 评审驳回再次提交 方式一(假设本地 master 不存在其他未评审的提交)
git co master
git pull --rebase origin master # 变基更新主干

git co hotfix                   # 切回修复分支
git rebase master               # 变基合并主干(相当于拉取最新代码再开发)
...                             # 开发
git ci -m '再次修复' --amend     # 更新提交说明
git co master
git pull --rebase origin master # 变基更新主干
git rebase hotfix               # 变基合并修复分支
git review master               # 提交评审

# 评审驳回再次提交 方式二(假设 master 已存在本地其他未评审的提交)
git br -D master                # 删除本地主干
git fetch origin master         # 拉取远程主干
git co -b master origin/master  # 创建本地主干

git co hotfix                   # 切回修复分支
git rebase master               # 变基合并主干(相当于拉取最新代码再开发)
...                             # 开发
git ci -m '再次修复' --amend     # 更新提交说明
git co master
git pull --rebase origin master # 变基更新主干
git rebase hotfix               # 变基合并修复分支
git review master               # 提交评审

# 评审通过删除本地分支(或者重命名,表示此分支后续不用关注)
git br -D hotfix
git br -m hotfix ok_hotfix
```

评审驳回再次提交 方式一 适用于开发节奏较慢，评审较快的场景
评审驳回再次提交 方式二 适用于开发节奏较快，评审较慢的场景

为什么要用`git commit --amend`（注意不是`git commit -m 'xxxxxx' --amend`）
1. 对于开发节奏较快，评审较慢的项目经常会用到
2. 多次提交时，如果前面的提交被驳回，导致后面的commit基于历史错误的提交，

对于没有合并的提交，想继续修改且无需产生新的提交
```
# 根据需要添加新的修改，如果仅仅修改comment内容，直接通过git commit --amend进入编辑界面
git add .
git commit --amend
# 进入编辑界面，根据需要修改提交内容，保持Change-Id不变，:wq保存退出
git review <分支名称>
```

Gerrit 合并冲突（Merge Conflit）的解决办法
```
git pull orgin <分支名称> --rebase
# 修复本地冲突
git add .
git rebase --continue
git commit --amend
# 进入编辑界面，根据需要修改提交内容，保持Change-Id不变，:wq保存退出
git review <分支名称>
```

## Git 状态及版本回退

```
未修改
       原始内容
已修改    ↓   
       工 作 区
已暂存    ↓    git add
       暂 存 区
已提交    ↓    git commit
       本地仓库
已推送    ↓    git push
       远程仓库
```

丢弃修改
```
# edit file
git restore .
git restore <file>...
git checkout .
git checkout -- <file>
```

丢弃暂存
```
# git add .
git reset
git restore --staged .
git restore --staged <file>...
```

修改提交
```
# git commit -m 'update'
git commit -m 'update for xxx' --amend
```

丢弃提交
```
# git commit -m 'update'
git reset HEAD^
```
回到上一次提交，并保留工作区（保留提交前的修改）

切回提交
```
git reset --hard <commitid>
```

丢弃推送
```
git reset --hard HEAD^
git push origin <branch> -f
```
回到上一次提交，并丢弃工作区（放弃提交前的修改），强行推送


## git log 和 git reflog

- git log
可以显示所有提交过的版本信息

- git reflog
可以查看所有分支的所有操作记录（包括已经被删除的 commit 记录和 reset 的操作）


## git stash
```bash
git stash list              # 查看所有
git stash clear             # 清除所有
git stash save              # 贮藏代码，贮藏所有，带上默认信息WIP on master: <前一版本的commit msg>，也可以带上指定信息：git stash save "message"
git stash push [file ...]   # git stash push -m "message"
git stash show              # 显示改动，仅仅显示差异文件，如需显示详细代码，可以：git stash show -p
git stash pop [stash]       # 恢复贮藏
git stash drop [stash]      # 丢弃贮藏
```
说明：
`stash@{$num}`，`$num`下标从0开始，默认是`stash@{0}`


## git配置别名

```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.ci commit
git config --global alias.br branch
```

全局配置文件路径：~/.gitconfig

```
git config --global core.pager ''
git config --global core.editor vim
```

排错：$'\r': command not found

一般是Linux服务器上执行通过windows环境远程拷贝的脚本时会出错。

git默认配置：core.autocrlf=true

windows环境下，提交自动转LF，签出自动转CRLF

手动更新换行符
```
:set ff=unix
:wq
```
出现原因：windows环境下的编辑器，换行符默认是CRLF，上传到Linux服务器之后执行脚本会报错

如果你是Windows程序员，且正在开发仅运行在Windows上的项目，可以设置false取消此功能，把回车符记录在库中
```
$ git config --global core.autocrlf false
```
