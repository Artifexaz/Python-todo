[本todo webapp基于此](https://jishuzhan.net/article/1851519426600374273)

## 创建python环境

```cmd
conda create -n python_todo
conda activate python_todo
```

## 需要安装node.js来执行以下命令行

```cmd
npx create-react-app .
npm install axios react-icons
```
[Create React App](https://cra.nodejs.cn/docs/getting-started/) 是官方支持的创建单页 React 应用的方法。它提供了一个没有配置的现代构建设置。

## pycharm提交项目代码到github的方法

[参考这个](https://zhuanlan.zhihu.com/p/13523136490)

## 关于.env文件

[如何创建和使用`.env`文件](https://blog.csdn.net/qq_44154915/article/details/140317912)

其中MONGODB_URI字段中的?前面要加上默认的database名字，比如"todo"：
```env
MONGODB_URI=mongodb+srv://artifexaz:Bi2V1grgJecztISt@cluster-todo.c8uovpu.mongodb.net/todo?retryWrites=true&w=majority&appName=Cluster-todo
```

[MongoDB cluster](https://zhuanlan.zhihu.com/p/98916948) username:artifexaz; password: Bi2V1grgJecztISt

## 关于docker自带的源无法下载
[参考这个](https://zhuanlan.zhihu.com/p/28662850275)

## 快速开始

在[atlas](https://cloud.mongodb.com/v2/68aa8af742cc0533dc0d9caa#/security/network/accessList)的Network access中添加自己的ip地址

安装并打开docker desktop软件； 

在backend目录中的终端运行：

```powershell
docker-compose up --build
```
在docker上构建服务镜像。

之后运行：`docker-compse up`直接重新编译启动应用；

或者更改server.py保存之后自动重新编译。

