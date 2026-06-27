import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';
import { Project, ProjectSimple, ProjectCreate, ProjectUpdate } from '../models/project.model';

@Injectable({
  providedIn: 'root'
})
export class ProjectService extends ApiService {
  private readonly endpoint = '/projects';

  getProjects(): Observable<ProjectSimple[]> {
    return this.get<ProjectSimple[]>(this.endpoint);
  }

  getProject(id: number): Observable<Project> {
    return this.get<Project>(`${this.endpoint}/${id}`);
  }

  createProject(data: ProjectCreate): Observable<Project> {
    return this.post<Project>(this.endpoint, data);
  }

  updateProject(id: number, data: ProjectUpdate): Observable<Project> {
    return this.patch<Project>(`${this.endpoint}/${id}`, data);
  }

  deleteProject(id: number): Observable<void> {
    return this.delete<void>(`${this.endpoint}/${id}`);
  }
}