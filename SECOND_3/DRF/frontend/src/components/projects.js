import React from 'react';
import {Link} from 'react-router-dom';

const Project = ({project}) => {
  return (
    <tr>
      <td><Link to={`/projects/${project.id}`}>{project.projectName}</Link></td>
      <td>{project.repoUrl}</td>
      <td>{project.assignedUsers.join(', ')}</td>
    </tr>
  )
}
const ProjectList = ({projects}) => {
  return (
    <table>
      <thead>
      <tr>
        <th>Project name</th>
        <th>Repo URL</th>
        <th>Users ID</th>
      </tr>
      </thead>
      <tbody>
        {projects.map((project) => <Project key={project.id} project={project} />)}
      </tbody>
    </table>
  )
}

export default ProjectList;