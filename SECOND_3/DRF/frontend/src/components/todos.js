import React from 'react';
import {Link} from 'react-router-dom'

const Todo = ({todo, deleteTodo}) => {
  return (
    <tr>
      <td>{todo.id}</td>
      <td>{todo.project}</td>
      <td>{todo.todo_text.length > 50 ? `${todo.todo_text.slice(0, 50)}...` : todo.todo_text}</td>
      <td>
        <button onClick={() => deleteTodo(todo.id)} type='button'>Delete</button>
      </td>
    </tr>
  )
}

const TodoList = ({todos, deleteTodo}) => {
  return (
    <div>
      <table>
        <thead>
        <tr>
          <th>ID</th>
          <th>Project ID</th>
          <th>Text</th>
          <th></th>
        </tr>
        </thead>
        <tbody>
        {todos.map((todo) => <Todo key={todo.id} todo={todo} deleteTodo={deleteTodo}/>)}
        </tbody>
      </table>
      <Link to='/todos/create/'>Create</Link>
    </div>
  )
}

export default TodoList;