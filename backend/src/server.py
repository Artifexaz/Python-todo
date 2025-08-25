from contextlib import asynccontextmanager
# 异步上下文管理器
from datetime import datetime
# datetime类用于处理时间和日期
import os
# python标准库Operating System管理文件和目录
import sys
# 访问解释器的变量、函数以及执行环境的相关信息

from bson import ObjectId
# ObjectId 是 MongoDB 中用于标识文档的唯一标识符（ID）
from fastapi import FastAPI, status
# 后端数据处理

from motor.motor_asyncio import AsyncIOMotorClient
# MongoDB异步客户端（motor库）来连接数据库。

from pydantic import BaseModel
# 负责数据处理部分
import uvicorn
# 是ASGI异步服务器网关接口，用于运行FastAPI应用。

from data_access_layer import ToDoDAL, ListSummary, ToDoList

import shutil # 用于流式上传复制文件
from fastapi import UploadFile, WebSocket # UploadFile上传文件，WebSocket实时更新上传进度
# from starlette.types import Receive, Scope, Send

COLLECTION_NAME = "todo_lists"
MONGODB_URI = os.environ["MONGODB_URI"]
# 从环境变量中获取MongoDB的URI连接字符串。

DEBUG = os.environ.get("DEBUG", "").strip().lower() in {"1", "true", "on", "yes"}
# 从环境变量读取调试模式，接受多种True的写法。

# 这是一个异步上下文管理器，管理FastAPI应用的启动和关闭。
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup:
    client = AsyncIOMotorClient(MONGODB_URI)
    # 创建MongoDB异步客户端实例，连接到数据库。

    database = client.get_default_database()
    # 获取MongoDB数据库实例，默认使用连接字符串中的数据库名称。

    # ping命令用于测试MongoDB连接是否正常。pong["ok"] == 1表示连接成功。
    pong = await database.command("ping")
    if int(pong["ok"]) != 1:
        raise Exception("没有连接上Cluster!")

    todo_lists = database.get_collection(COLLECTION_NAME)
    # 获取待办事项集合“todo_lists”。

    app.todo_dal = ToDoDAL(todo_lists)
    # 将ToDoDAL实例附加到FastAPI应用实例上，便于其他模块使用。

    # Yield back to FastAPI Application:
    yield
    # 暂停上下文管理器，将控制权交给应用，以继续运行其他操作。

    # Shutdown:
    client.close()
    # 应用关闭时，自动关闭MongoDB连接以释放资源。


app = FastAPI(lifespan=lifespan, debug=DEBUG)
# 使用lifespan管理器（在应用启动和关闭时管理数据库连接）。
# debug=DEBUG设定调试模式，使得在调试时更容易看到错误和详细信息。

# 流式上传大文件，内存优化
@app.post("/upload")
async def upload_file(file: UploadFile):
    file_save_path = f"{file.filename}"

    with open(file_save_path, "ab") as buffer:
        shutil.copyfileobj(file.file, buffer)

# 异步获取所有待办事项列表的摘要信息。
@app.get("/api/lists")
async def get_all_lists() -> list[ListSummary]:
    return [i async for i in app.todo_dal.list_todo_lists()]


# 用于创建新的待办事项列表，包含列表名称。
class NewList(BaseModel):
    name: str


# 用于创建操作成功后的响应，包含列表的id和name。
class NewListResponse(BaseModel):
    id: str
    name: str


# 接受NewList格式的数据，创建新的待办事项列表。
@app.post("/api/lists", status_code=status.HTTP_201_CREATED)
async def create_todo_list(new_list: NewList) -> NewListResponse:
    return NewListResponse(
        id=await app.todo_dal.create_todo_list(new_list.name),
        name=new_list.name,
    )


# 使用列表的唯一标识符list_id获取单个待办事项列表。
# 调用get_todo_list方法，返回一个包含列表详细信息的ToDoList对象。
@app.get("/api/lists/{list_id}")
async def get_list(list_id: str) -> ToDoList:
    """Get a single to-do list"""
    return await app.todo_dal.get_todo_list(list_id)


# 根据list_id删除指定的待办事项列表。
# 调用delete_todo_list方法，返回布尔值表示删除是否成功。
@app.delete("/api/lists/{list_id}")
async def delete_list(list_id: str) -> bool:
    return await app.todo_dal.delete_todo_list(list_id)


# 用于添加新待办事项的数据模型，包含label字段，表示待办事项的标签（描述）。
class NewItem(BaseModel):
    label: str


# 用于返回新添加项的响应模型，包含id和label字段。
class NewItemResponse(BaseModel):
    id: str
    label: str


# 用于向指定的待办事项列表（list_id）中添加新待办事项items。
@app.post(
    "/api/lists/{list_id}/items/",
    status_code=status.HTTP_201_CREATED,
)
# 调用create_item方法，将list_id和new_item.label传入。
# 返回更新后的完整待办事项列表ToDoList，包含新的待办事项item。
async def create_item(list_id: str, new_item: NewItem) -> ToDoList:
    return await app.todo_dal.create_item(list_id, new_item.label)


# 根据list_id和item_id删除指定待办事项列表中的特定项。
# 返回更新后的ToDoList对象，删除项后更新的列表。
@app.delete("/api/lists/{list_id}/items/{item_id}")
async def delete_item(list_id: str, item_id: str) -> ToDoList:
    return await app.todo_dal.delete_item(list_id, item_id)


# 定义更新待办事项item的完成状态所需的数据模型。
# 包含item_id（待办事项item的唯一标识符）和checked_state（布尔值，表示是否已完成）字段。
class ToDoItemUpdate(BaseModel):
    item_id: str
    checked_state: bool


# 用于更新指定待办事项列表中某个待办事项item的完成状态。
# 返回更新后的ToDoList对象，反映状态变更后的完整列表。
@app.patch("/api/lists/{list_id}/checked_state")
async def set_checked_state(list_id: str, update: ToDoItemUpdate) -> ToDoList:
    return await app.todo_dal.set_item_checked_state(list_id, update.item_id, update.checked_state)


class DummyResponse(BaseModel):
    id: str
    when: datetime


@app.get("/api/dummy")
async def get_dummy() -> DummyResponse:
    return DummyResponse(
        id=str(ObjectId()),
        when=datetime.now(),
    )
# 使用ObjectId()生成一个新的唯一标识符并转换为字符串，赋值给id。
# 每个文档在MongoDB数据库中都有一个_id字段，默认情况下，它的值是一个ObjectId。
# 使用datetime.now()获取当前时间并赋值给when。


def main(argv=sys.argv[1:]):
    try:
        # 使用uvicorn来启动FastAPI应用
        uvicorn.run("server:app", host="0.0.0.0", port=3001, reload=DEBUG)
        # host="0.0.0.0"：让应用在所有可用的网络接口上监听。
        # reload=DEBUG：如果DEBUG为True，在(开发阶段）代码更改时自动重载应用。
    except KeyboardInterrupt:
        pass
        # 使用try...except来捕获KeyboardInterrupt异常，以便在按下Ctrl+C时优雅地停止服务。


if __name__ == "__main__":
    main()