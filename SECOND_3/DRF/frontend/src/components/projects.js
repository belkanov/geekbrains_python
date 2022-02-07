import React from 'react';
import {Link} from 'react-router-dom';

const Project = ({project, deleteProject}) => {
  return (
    <tr>
      <td><Link to={`/projects/${project.id}`}>{project.projectName}</Link></td>
      <td>{project.repoUrl}</td>
      <td>{project.assignedUsers.join(', ')}</td>
      <td>
        <button onClick={() => deleteProject(project.id)} type='button'>Delete</button>
      </td>
    </tr>
  )
}
const ProjectList = ({projects, deleteProject, filterProjects}) => {

  return (
    <div>
      {/* не самое очевидное поведение.. при наличии строки фильтрации - фильтует*/}
      <form onSubmit={(event) => filterProjects(event)}>
        <input type="text" name="searchStr" placeholder="search"/>
        <input type="submit" value="Search"/>
      </form>
      <table>
        <thead>
        <tr>
          <th>Project name</th>
          <th>Repo URL</th>
          <th>Users ID</th>
          <th></th>
        </tr>
        </thead>
        <tbody>
        {projects.map((project) => <Project key={project.id} project={project} deleteProject={deleteProject}/>)}
        </tbody>
      </table>
    </div>
  )
}

export default ProjectList;