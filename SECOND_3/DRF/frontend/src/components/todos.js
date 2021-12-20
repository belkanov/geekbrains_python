import React from 'react';

const Todo = ({todo}) => {
  return (
    <tr>
      <td>{todo.id}</td>
      <td>{todo.project}</td>
      <td>{todo.todo_text.length>50 ? `${todo.todo_text.slice(0,50)}...` : todo.todo_text}</td>
    </tr>
  )
}

const TodoList = ({todos}) => {
  return (
    <table>
      <thead>
      <tr>
        <th>ID</th>
        <th>Project ID</th>
        <th>Text</th>
      </tr>
      </thead>
      <tbody>
        {todos.map((todo) => <Todo key={todo.id} todo={todo}/>)}
      </tbody>
    </table>
  )
}

export default TodoList;