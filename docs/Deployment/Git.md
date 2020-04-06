# Git 的骚操作

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
