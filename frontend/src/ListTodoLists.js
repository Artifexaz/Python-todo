import "./ListTodoLists.css";
import { useRef } from "react";
import { BiSolidTrash } from "react-icons/bi"; // 引入一个垃圾桶图标，用于删除功能的按钮。
import FileUploadButton from "./FileUploadButton";

function ListToDoLists({
  listSummaries, // 待办事项列表的概要信息数组。
  handleSelectList, // 处理用户选择特定待办事项列表的函数。
  handleNewToDoList, // 处理创建新待办事项列表的函数。
  handleDeleteToDoList, // 处理删除指定待办事项列表的函数。
}) {
  const labelRef = useRef(); // 用于访问新待办事项列表名称的输入框值。

  if (listSummaries === null) {
    return <div className="ListToDoLists loading">正在加载待办事项……</div>;
    // 如果 listSummaries 为 null，组件会显示"正在加载待办事项……"字样，表示数据正在加载。
  } else if (listSummaries.length === 0) {
    return (
      <div className="ListToDoLists">
        <h1>待办列表</h1>
        <div className="box">
        <label>
          准备做什么？&nbsp;
          <input id={labelRef} type="text" />
          &nbsp;&nbsp;
        </label>
        <button
          onClick={() =>
            handleNewToDoList(document.getElementById(labelRef).value)
            // 提交新列表名称。
          }
        >
          新待办
        </button>
        </div>
        <p>现在没有任务，放松一下吧</p>
      </div>
    );
  }
  return (
    <div className="ListToDoLists">
      <h1>待办列表</h1>
      <div className="box">
        <label>
          准备做什么？&nbsp;
          <input id={labelRef} type="text" />
          &nbsp;&nbsp;
        </label>
        <button
          onClick={() =>
            handleNewToDoList(document.getElementById(labelRef).value)
          }
        >
          新待办
        </button>
        {/*提供添加新待办事项列表的功能，输入新名称并点击"New"按钮。*/}
      </div>
      {listSummaries.map((summary) => {
        return (
          <div
            key={summary.id}
            className="summary"
          >
            <span
              className="name"
              onClick={() => handleSelectList(summary.id)}
              // 条目点击时会调用 handleSelectList 并传入 summary.id，
              // 从而选择该列表并展示详细信息。
            >
              {summary.name}
            </span>
            <span
              className="count"
              onClick={() => handleSelectList(summary.id)}
            >
              ({summary.item_count} 个子任务)
            </span>
            <span className="flex"></span>
            <FileUploadButton />
            <span
              cursor = "pointer"
              className="trash"
              onClick={(evt) => {
                evt.stopPropagation(); // 阻止事件冒泡到父元素
                handleDeleteToDoList(summary.id);
              }}
            >
              &nbsp;&nbsp;<BiSolidTrash />
              {/*<BiSolidTrash /> 是一个垃圾桶图标，*/}
              {/*点击时会触发 handleDeleteToDoList 删除该条目。*/}
            </span>
          </div>
        );
      })}
    </div>
  );
}

export default ListToDoLists;