import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";
import ListToDoLists from "./ListTodoLists";
import ToDoList from "./ToDoList";

function App() {
  const [listSummaries, setListSummaries] = useState(null);
  // 存储从 /api/lists 获取的所有待办事项列表的摘要。

  const [selectedItem, setSelectedItem] = useState(null);
  // 此变量用于存储当前选中的待办事项列表的 ID。

  useEffect(() => {
    reloadData().catch(console.error);
  }, []);
  // useEffect 在组件挂载时调用 reloadData 函数，从服务器加载待办事项列表的数据。

  async function reloadData() {
    const response = await axios.get("/api/lists");
    const data = await response.data;
    setListSummaries(data);
  }
  // 通过 axios.get 向 /api/lists 发送请求，从服务器获取所有待办事项列表的摘要信息。

  function handleNewToDoList(newName) {
    const updateData = async () => {
      const newListData = {
        name: newName,
      };

      await axios.post(`/api/lists`, newListData);
      reloadData().catch(console.error);
    };
    updateData();
  }
  // 接受 newName 作为新列表的名称，发送 POST 请求到 /api/lists，然后刷新数据以更新界面。

  function handleDeleteToDoList(id) {
    const updateData = async () => {
      await axios.delete(`/api/lists/${id}`);
      reloadData().catch(console.error);
    };
    updateData();
  }
  // 根据 id 向 /api/lists/{id} 发送 DELETE 请求，然后刷新数据。

  function handleSelectList(id) {
    console.log("Selecting item", id);
    setSelectedItem(id);
    // 设置 selectedItem 为选中的列表的 id。
  }

  function backToList() {
    setSelectedItem(null);
    // 清除 selectedItem 的值，将视图切换回所有待办事项列表的界面。
    reloadData().catch(console.error);
  }

  if (selectedItem === null) {
    return (
      <div className="App">
        <ListToDoLists
          listSummaries={listSummaries}
          handleSelectList={handleSelectList}
          handleNewToDoList={handleNewToDoList}
          handleDeleteToDoList={handleDeleteToDoList}
        />
      </div>
    );
  } else {
    return (
      <div className="App">
        <ToDoList
          listId={selectedItem}
          handleBackButton={backToList}
        />
      </div>
    );
  }
}

export default App;