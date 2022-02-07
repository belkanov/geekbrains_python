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

  get_data() {
    const baseUrl = 'http://localhost:8000/api';
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
            'projects': projects
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
                { this.is_auth() ? <button onClick={() => this.logout()}>LOGOUT</button> : <Link to="/login">LOGIN</Link> }
              </li>
            </ul>
          </nav>
          <Switch>
            <Route exact path='/login/' component={() => <LoginForm get_token={(username, password) => this.get_token(username, password)}/>}/>
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
