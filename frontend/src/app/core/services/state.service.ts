import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { ProjectSimple } from '../models/project.model';

@Injectable({
  providedIn: 'root'
})
export class StateService {
  // Proyecto activo
  private activeProjectSubject = new BehaviorSubject<ProjectSimple | null>(null);
  activeProject$ = this.activeProjectSubject.asObservable();

  // Loading state
  private loadingSubject = new BehaviorSubject<boolean>(false);
  loading$ = this.loadingSubject.asObservable();

  // Error state
  private errorSubject = new BehaviorSubject<string | null>(null);
  error$ = this.errorSubject.asObservable();

  setActiveProject(project: ProjectSimple | null): void {
    this.activeProjectSubject.next(project);
  }

  getActiveProject(): ProjectSimple | null {
    return this.activeProjectSubject.getValue();
  }

  setLoading(loading: boolean): void {
    this.loadingSubject.next(loading);
  }

  setError(error: string | null): void {
    this.errorSubject.next(error);
  }

  clearError(): void {
    this.errorSubject.next(null);
  }
}