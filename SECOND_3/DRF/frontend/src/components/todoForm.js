import React from 'react'


class TodoForm extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      projectId: 0,
      text: ''}
  }

  handleChange(event) {
    this.setState(
      {
        [event.target.name]: event.target.value
      }
    );
  }

  handleSubmit(event) {
    // console.log(this.state.projectId)
    // console.log(this.state.text)
    this.props.createTodo(this.state.projectId, this.state.text)
    event.preventDefault()
  }

  render() {
    return (
      <form onSubmit={(event) => this.handleSubmit(event)}>
        <div className="form-group">
          <label for="project">project</label>
          <input type="number" className="form-control" name="projectId" value={this.state.projectId} onChange={(event) => this.handleChange(event)}/>
        </div>
        <div className="form-group">
          <label for="text">text</label>
          <input type="text" className="form-control" name="text" value={this.state.text} onChange={(event) => this.handleChange(event)}/>
        </div>
        <input type="submit" className="btn btn-primary" value="Save"/>
      </form>
    );
  }
}

export default TodoForm;

