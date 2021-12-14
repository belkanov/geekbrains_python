import React from 'react';

const User = ({user}) => {
  return (
    <tr>
      <td>{user.username}</td>
      <td>{user.first_name}</td>
      <td>{user.last_name}</td>
      <td>{user.email}</td>
    </tr>
  )
}
const UserList = ({users}) => {
  return (
    <table>
      <thead>
      <tr>
        <th>username</th>
        <th>first name</th>
        <th>last name</th>
        <th>email</th>
      </tr>
      </thead>
      <tbody>
        {users.map((user) => <User user={user}/>)}
      </tbody>
    </table>
  )
}

export default UserList;