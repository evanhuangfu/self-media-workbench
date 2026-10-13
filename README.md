# 自媒体工作台

在本机管理选题、拍摄进度、口播稿、参考资料和各平台发布记录，支持导出 Word。

## 启动

需要 Node.js 20.19+（或 22.12+）和 Python 3.10+。

```sh
npm ci
npm run build
python3 -m pip install -r requirements.txt
python3 launch.py
```

浏览器打开 http://127.0.0.1:19826 。首次运行为空白工作台，可自行添加选题和写作偏好。

## 数据

本仓库只提供程序，不包含真实选题、稿件、个人写作偏好或发布记录。
运行后产生的资料保存在本机 `data/`，该目录及备份、导出文件均已排除 Git 跟踪。浏览器中的未保存草稿也只保存在本机。

发布台账用于登记与核对记录，不会自动向社交平台发布内容。服务仅监听本机地址，不提供公网登录功能。

## 检查

```sh
python3 -m unittest discover -s tests
npm run build
```
