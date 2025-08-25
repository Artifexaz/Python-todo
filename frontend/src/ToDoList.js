import "./ToDoList.css";
import { useEffect, useState, useRef } from "react";
import axios from "axios";
import { BiSolidTrash } from "react-icons/bi";

function ToDoList({
  listId,
  handleBackButton
}) {
  let labelRef = useRef(); // 用于访问新item列表名称的输入框值。
  const [listData, setListData] = useState(null);

// 获取列表数据
  useEffect(() => {
    const fetchData = async () => {
      const response = await axios.get(`/api/lists/${listId}`);
      const newData = await response.data;
      setListData(newData);
    };
    fetchData();
  }, [listId]);

// 创建新待办事项
  function handleCreateItem(label) {
    const updateData = async () => {
      const response = await axios.post(`/api/lists/${listData.id}/items/`, {
        label: label,
      });
      setListData(await response.data);
    };
    updateData();
  }

// 删除待办事项
  function handleDeleteItem(id) {
    const updateData = async () => {
      const response = await axios.delete(
        `/api/lists/${listData.id}/items/${id}`
      );
      setListData(await response.data);
    };
    updateData();
  }

// 更新项目状态
  function handleCheckToggle(itemId, newState) {
    const updateData = async () => {
      const response = await axios.patch(
        `/api/lists/${listData.id}/checked_state`,
        {
          item_id: itemId,
          checked_state: newState,
        }
      );
      setListData(await response.data);
    };
    updateData();
  }


  if (listData === null) {
    return (
      <div className="ToDoList loading">
        <button className="back" onClick={handleBackButton}>
          返回
        </button>
        正在加载待办子任务列表……
      </div>
    );
  }
  return (
    <div className="ToDoList">
      <button className="back" onClick={handleBackButton}>
        返回
      </button>
      <h1>{listData.name}</h1>
      <div className="box">
        <label>
          子任务:&nbsp;
          <input id={labelRef} type="text" />
          &nbsp;&nbsp;
        </label>
        <button
          onClick={() =>
            handleCreateItem(document.getElementById(labelRef).value)
          }
        >
          新子任务
        </button>
        {/*用户可在输入框输入内容后点击 New 按钮添加项目。*/}
      </div>
      {listData.items.length > 0 ? (
        listData.items.map((item) => {
          return (
            <div
              key={item.id}
              className={item.checked ? "item checked" : "item"}
              onClick={() => handleCheckToggle(item.id, !item.checked)}
            >
              <span>{item.checked ? "✅" : "⬜️"} </span>
              {/*复选框：使用 ✅ 和 ⬜️ 表示项目的完成状态，点击切换状态。*/}
              <span className="label">{item.label} </span>
              <span className="flex"></span>
              <span
                style={{
                  cursor: "pointer"
                }}
                className="trash"
                onClick={(evt) => {
                  evt.stopPropagation();
                  handleDeleteItem(item.id);
                }}
              >
                <BiSolidTrash /> {/*垃圾桶图标：点击删除项目。*/}
              </span>
            </div>
          );
        })
      ) : (
        <div className="box">还没有子任务</div>
      )}
    </div>
  );
}

export default ToDoList;