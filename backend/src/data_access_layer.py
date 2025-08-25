from bson import ObjectId
# ObjectId是MongoDB的默认主键类型，通常用于查询和处理数据库中的唯一标识符。
from motor.motor_asyncio import AsyncIOMotorCollection
# motor是MongoDB的异步驱动程序，用于与MongoDB进行异步交互。
# AsyncIOMotorCollection是一个集合（collection）对象，提供了对MongoDB集合的异步操作。
from pymongo import ReturnDocument
# ReturnDocument 是pymongo中的常量，用于在更新操作时指定返回更新前或更新后的文档。
from pydantic import BaseModel
# Pydantic的BaseModel类是一个数据验证和数据结构定义工具。
from uuid import uuid4
# 用于生成基于随机数的 UUID（通用唯一标识符）

class ListSummary(BaseModel):
  id: str # 文档的唯一标识符，将MongoDB中的ObjectId转换为字符串。
  name: str # 文档的名称字段。
  item_count: int # 文档中项目的数量字段。

  @staticmethod
  def from_doc(doc) -> "ListSummary":
      return ListSummary(
          id=str(doc["_id"]),
          name=doc["name"],
          item_count=doc["item_count"],
      )
# 这是一个静态方法，接受一个MongoDB文档（字典类型）作为参数，
# 并将该文档转换为ListSummary对象。doc通常是从MongoDB集合中查询返回的文档数据。


class ToDoListItem(BaseModel):
  id: str
  label: str
  checked: bool

  @staticmethod
  def from_doc(item) -> "ToDoListItem":
      return ToDoListItem(
          id=item["id"],
          label=item["label"],
          checked=item["checked"],
      )
# 将MongoDB中表示单个待办事项的文档（item）转换为ToDoListItem对象。
# 它提取id、label和checked字段，并使用这些字段来创建一个ToDoListItem实例。


class ToDoList(BaseModel):
  id: str
  name: str
  items: list[ToDoListItem]

  @staticmethod
  def from_doc(doc) -> "ToDoList":
      return ToDoList(
          id=str(doc["_id"]),
          name=doc["name"],
          items=[ToDoListItem.from_doc(item) for item in doc["items"]],
      )
# 接收一个待办事项列表的MongoDB文档（doc），将其转换为ToDoList对象。
# 方法从doc中提取_id和name字段，并将items字段中的每个待办事项文档
# 通过ToDoListItem.from_doc方法转换为ToDoListItem对象，最终返回一个ToDoList实例。


# 处理对MongoDB中待办事项数据的增删改查操作。
class ToDoDAL:
  def __init__(self, todo_collection: AsyncIOMotorCollection):
      self._todo_collection = todo_collection

  # 返回所有待办事项列表的简要信息（名称和项目数）
  async def list_todo_lists(self, session=None):
      async for doc in self._todo_collection.find(
          {},
          projection={
              "name": 1,
              "item_count": {"$size": "$items"},
          },
          sort={"name": 1},
          session=session,
      ):
          yield ListSummary.from_doc(doc)

  # 创建一个新的待办事项列表。
  # 插入文档的_id字符串形式。
  async def create_todo_list(self, name: str, session=None) -> str:
      response = await self._todo_collection.insert_one(
          {"name": name, "items": []},
          session=session,
      )
      return str(response.inserted_id)

  # 根据ID获取特定待办事项列表的完整信息。
  async def get_todo_list(self, id: str | ObjectId, session=None) -> ToDoList:
      doc = await self._todo_collection.find_one(
          {"_id": ObjectId(id)},
          session=session,
      )
      return ToDoList.from_doc(doc)

  # 根据ID删除一个待办事项列表。
  async def delete_todo_list(self, id: str | ObjectId, session=None) -> bool:
      response = await self._todo_collection.delete_one(
          {"_id": ObjectId(id)},
          session=session,
      )
      return response.deleted_count == 1

  # 向指定待办事项列表中添加新项目
  async def create_item(
      self,
      id: str | ObjectId,
      label: str,
      session=None,
  ) -> ToDoList | None:
      result = await self._todo_collection.find_one_and_update(
          {"_id": ObjectId(id)},
          {
              "$push": {
                  "items": {
                      "id": uuid4().hex, # 随机生成id
                      "label": label,
                      "checked": False,
                  }
              }
          },
          session=session,
          return_document=ReturnDocument.AFTER,
      )
      if result:
          return ToDoList.from_doc(result)

  # 设置待办事项item的checked状态。
  async def set_item_checked_state(
      self,
      doc_id: str | ObjectId,
      item_id: str,
      checked_state: bool,
      session=None,
  ) -> ToDoList | None:
      result = await self._todo_collection.find_one_and_update(
          {"_id": ObjectId(doc_id), "items.id": item_id},
          {"$set": {"items.$.checked": checked_state}},
          session=session,
          return_document=ReturnDocument.AFTER,
      )
      if result:
          return ToDoList.from_doc(result)

  # 从指定待办事项列表中删除一个项目。
  async def delete_item(
      self,
      doc_id: str | ObjectId,
      item_id: str,
      session=None,
  ) -> ToDoList | None:
      result = await self._todo_collection.find_one_and_update(
          {"_id": ObjectId(doc_id)},
          {"$pull": {"items": {"id": item_id}}},
          session=session,
          return_document=ReturnDocument.AFTER,
      )
      if result:
          return ToDoList.from_doc(result)