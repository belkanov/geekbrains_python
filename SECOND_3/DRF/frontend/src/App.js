import React from 'react';
import logo from './logo.svg';
import './App.css';
import UserList from './components/users.js';
import axios from 'axios';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      'authors': []
    }
  }

  componentDidMount() {
    axios.get('http://localhost:8000/api/users/')
      .then((response) => {
        const authors = response.data;
        this.setState(
          {
            'authors': authors
          }
        )
      })
      .catch(error => console.log(error))
  }

  render() {
    return (
      <div>
        <UserList users={this.state.authors}/>
      </div>
    )
  }
}

export default App;
