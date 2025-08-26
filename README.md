# 前端

- **React**
- 实现待办列表页面，可以添加/编辑/删除待办事项；
- 支持上传大于500MB的文件。

# 后端

- **FastAPI**
- [**MongoDB**](https://www.mongodb.com/zh-cn)：为web应用程序和互联网基础设施设计的数据库管理系统。

# 操作演示视频



https://github.com/user-attachments/assets/bad9dd71-0461-448a-8bb9-83d64d850fa6



# 快速开始  


- 在[MONGODB](https://www.mongodb.com/)上建立一个集群，在.env文件中替换`MONGODB_URI=`后面的`URI`，并在`URI`中的`?`前加上todo，如：`...mongodb.net/todo?retryWrites...`
- 在[atlas](https://cloud.mongodb.com/v2/68aa8af742cc0533dc0d9caa#/security/network/accessList)的Network access中添加自己的ip地址。
- 安装并打开[docker desktop](https://docs.docker.com/)软件。
- 在frontend目录中的管理员终端运行以下命令，在本地安装完整node_module；axios用于发送HTTP请求，可以从后端API获取数据；react-icons是图标库。
	```
	npm install axios react-icons
	```
- 在backend目录中的终端运行以下命令，在docker上构建服务镜像。  
	```powershell  
	docker-compose up --build  
	```  
- 在浏览器中打开`http://localhost:8000/`，启动应用。
