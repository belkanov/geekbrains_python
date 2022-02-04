import axios from 'axios';
import React from 'react';
import {Link, Switch, Route, BrowserRouter} from 'react-router-dom';
// import logo from './logo.svg';
import './App.css';
import UserList from './components/users.js';
import ProjectList from './components/projects.js';
import ProjectSingle from './components/projectSingle.js';
import TodoList from './components/todos.js';

const NotFound404 = ({location}) => {
  return (
    <div>
      <h1>Страница по адресу '{location.pathname}' не найдена.</h1>
    </div>
  )
}

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      'users': [],
      'projects': [],
      'todos': []
    }
  }

  componentDidMount() {
    const baseUrl = 'http://localhost:8000/api';

    axios.get(`${baseUrl}/users/`)
      .then((response) => {
        const users = response.data.results;
        this.setState(
          {
            'users': users
          }
        )
      })
      .catch(error => console.log(error));
    axios.get(`${baseUrl}/projects/`)
      .then((response) => {
        const projects = response.data.results;
        this.setState(
          {
            'projects': projects
          }
        )
      })
      .catch(error => console.log(error));
    axios.get(`${baseUrl}/todos/`)
      .then((response) => {
        const todos = response.data.results;
        this.setState(
          {
            'todos': todos
          }
        )
      })
      .catch(error => console.log(error));
  }

  render() {
    return (
      <div>
        <BrowserRouter>
          <nav>
            <ul>
              {/*<li>Главная</li>*/}
              <li>
                <Link to='/users/'>Пользователи</Link>
              </li>
              <li>
                <Link to='/projects/'>Проекты</Link>
              </li>
              <li>
                <Link to='/todos/'>TODOs</Link>
              </li>
            </ul>
          </nav>
          <Switch>
            <Route exact path='/users/' component={() => <UserList users={this.state.users}/>}/>
            <Route exact path='/projects/' component={() => <ProjectList projects={this.state.projects}/>}/>
            <Route exact path='/projects/:id'>
              <ProjectSingle projects={this.state.projects}/>
            </Route>
            <Route exact path='/todos/' component={() => <TodoList todos={this.state.todos}/>}/>
            <Route component={NotFound404}/>
          </Switch>
        </BrowserRouter>
      </div>
    )
  }
}

export default App;
