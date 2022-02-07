import axios from 'axios';
import React from 'react';
import {Link, Switch, Route, BrowserRouter} from 'react-router-dom';
// import logo from './logo.svg';
import './App.css';
import UserList from './components/users.js';
import ProjectList from './components/projects.js';
import ProjectSingle from './components/projectSingle.js';
import TodoList from './components/todos.js';
import LoginForm from './components/auth.js';
import TodoForm from "./components/todoForm";

const baseUrl = 'http://localhost:8000/api';

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
      'orig_projects': [],
      'projects': [],
      'todos': []
    }
  }

  get_token(login, password) {
    axios
      .post('http://127.0.0.1:8000/api-token-auth/', {"username": login, "password": password})
      .then(response => {
        const token = response.data.token
        console.log(token)
        localStorage.setItem('token', token)
        this.setState({
          'token': token
        }, this.get_data)
      })
      .catch(error => console.log(error))
  }

  logout() {
    localStorage.setItem('token', '')
    this.setState({
      'token': ''
    }, this.get_data)
  }

  is_auth() {
    return !!this.state.token
  }

  get_headers() {
    if (this.is_auth()) {
      return {
        'Authorization': 'Token ' + this.state.token
      }
    }
    return {}
  }

  // Сделал фильтр по полученным данным,
  // т.к. фильтр по всей БД доступен из прошлых уроков (хотя доступа к нему через фронт нет):
  // http://127.0.0.1:8000/api/projects/?name=_3
  // возможно надо было это связать, но эта мысль меня посетила поздно =)
  filterProjects(event) {
    const filterStr = event.target[0].value

    if (filterStr) {
        this.setState(
          {
            projects: this.state.orig_projects.filter((item) => item.projectName.includes(filterStr))
          }
        )
      } else {
        this.setState(
          {
            projects: JSON.parse(JSON.stringify(this.state.orig_projects))
          }
        )
      }
    event.preventDefault()
  }

  get_data() {
    const headers = this.get_headers();

    axios.get(`${baseUrl}/users/`, {headers})
      .then((response) => {
        const users = response.data.results;
        this.setState(
          {
            'users': users
          }
        )
      })
      .catch(error => console.log(error));
    axios.get(`${baseUrl}/projects/`, {headers})
      .then((response) => {
        const projects = response.data.results;
        this.setState(
          {
            'orig_projects': projects,
            'projects': JSON.parse(JSON.stringify(projects))
          }
        )
      })
      .catch(error => console.log(error));
    axios.get(`${baseUrl}/todos/`, {headers})
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

  deleteProject(id) {
    const headers = this.get_headers()
    axios.delete(`${baseUrl}/projects/${id}/`, {headers})
      .then(response => {
        this.setState({projects: this.state.projects.filter((item) => item.id !== id)})
      }).catch(error => console.log(error))
  }

  createTodo(projectId, text) {
    const headers = this.get_headers()
    const data = {project: projectId, todo_text: text}
    axios.post(`${baseUrl}/todos/`, data, {headers})
      .then(response => {
        const new_todo = response.data
        // const project = this.state.projects.filter((item) => item.id === new_todo.project)[0]
        // new_todo.project = project
        this.setState({todos: [...this.state.todos, new_todo]})
      }).catch(error => console.log(error))
  }

  deleteTodo(id) {
    const headers = this.get_headers()
    axios.delete(`${baseUrl}/todos/${id}/`, {headers})
      .then(response => {
        this.setState({todos: this.state.todos.filter((item) => item.id !== id)})
      }).catch(error => console.log(error))
  }

  componentDidMount() {
    let token = localStorage.getItem('token')
    this.setState({
      'token': token
    }, this.get_data)
  }

  render() {
    return (
      <div>
        <BrowserRouter>
          <nav>
            <ul>
              {/*<li>Главная</li>*/}
              {/*<li>*/}
              {/*  <Link to='/login/'>LOGIN</Link>*/}
              {/*</li>*/}
              <li>
                <Link to='/users/'>Пользователи</Link>
              </li>
              <li>
                <Link to='/projects/'>Проекты</Link>
              </li>
              <li>
                <Link to='/todos/'>TODOs</Link>
              </li>
              <li>
                {this.is_auth() ? <button onClick={() => this.logout()}>LOGOUT</button> : <Link to="/login">LOGIN</Link>}
              </li>
            </ul>
          </nav>
          <Switch>
            <Route exact path='/login/' component={() => <LoginForm get_token={(username, password) => this.get_token(username, password)}/>}/>
            <Route exact path='/users/' component={() => <UserList users={this.state.users}/>}/>
            <Route exact path='/projects/' component={() => <ProjectList
              projects={this.state.projects}
              deleteProject={(id) => {
                this.deleteProject(id)
              }}
              filterProjects={(event) => {this.filterProjects(event)}}
            />}/>
            <Route exact path='/projects/:id'>
              <ProjectSingle projects={this.state.projects}/>
            </Route>
            <Route exact path='/todos/' component={() => <TodoList todos={this.state.todos} deleteTodo={(id) => {
              this.deleteTodo(id)
            }}/>}/>
            <Route exact path='/todos/create/' component={() => <TodoForm createTodo={(project, text) => {
              this.createTodo(project, text)
            }}/>}/>
            <Route component={NotFound404}/>
          </Switch>
        </BrowserRouter>
      </div>
    )
  }
}

export default App;
