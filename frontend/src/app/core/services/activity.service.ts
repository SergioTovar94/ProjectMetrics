import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';
import { Activity, ActivityCreate, ActivityUpdate } from '../models/activity.model';

@Injectable({
  providedIn: 'root'
})
export class ActivityService extends ApiService {
  private readonly endpoint = '/activities';

  getActivitiesByProject(projectId: number): Observable<Activity[]> {
    return this.get<Activity[]>(`${this.endpoint}/project/${projectId}`);
  }

  getActivity(id: number): Observable<Activity> {
    return this.get<Activity>(`${this.endpoint}/${id}`);
  }

  createActivity(data: ActivityCreate): Observable<Activity> {
    return this.post<Activity>(this.endpoint, data);
  }

  updateActivity(id: number, data: ActivityUpdate): Observable<Activity> {
    return this.patch<Activity>(`${this.endpoint}/${id}`, data);
  }

  deleteActivity(id: number): Observable<void> {
    return this.delete<void>(`${this.endpoint}/${id}`);
  }
}