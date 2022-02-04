import React from 'react';
import {useParams} from 'react-router-dom';

const Project = ({project}) => {
  return (
    <tr>
      <td>{project.projectName}</td>
      <td>{project.repoUrl}</td>
      <td>{project.assignedUsers.join(', ')}</td>
    </tr>
  )
}

const ProjectSingle = ({projects}) => {
  const {id} = useParams();
  const filteredProjects = projects.filter((project) => project.id === Number(id))

  return (
    <table>
      <thead>
      <tr>
        <th>Project name</th>
        <th>Repo URL</th>
        <th>Users</th>
      </tr>
      </thead>
      <tbody>
        {filteredProjects.map((project) => <Project project={project} />)}
      </tbody>
    </table>
  )
}

export default ProjectSingle;