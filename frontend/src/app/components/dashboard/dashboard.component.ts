import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Subscription } from 'rxjs';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';  

import { ProjectSimple } from '../../core/models/project.model';
import { StateService } from '../../core/services/state.service';
import { ProjectService } from '../../core/services/project.service';
import { StatusPillsComponent } from '../status-pills/status-pills.component';
import { KpiCardsComponent } from '../kpi-cards/kpi-cards.component';
import { BarChartComponent } from '../bar-chart/bar-chart.component';
import { ActivityTableComponent } from '../activity-table/activity-table.component';
import { ActivityFormComponent } from '../activity-form/activity-form.component';


@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    StatusPillsComponent,
    KpiCardsComponent,
    BarChartComponent,
    ActivityTableComponent,
    MatDialogModule,
  ],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit, OnDestroy {
  projects: ProjectSimple[] = [];
  activeProject: ProjectSimple | null = null;
  loading = false;
  error: string | null = null;
  private subscriptions: Subscription[] = [];

  constructor(
    private stateService: StateService,
    private projectService: ProjectService,
    private dialog: MatDialog 
  ) {}

  ngOnInit(): void {
    this.subscriptions.push(
      this.stateService.activeProject$.subscribe(project => {
        this.activeProject = project;
      })
    );

    this.subscriptions.push(
      this.stateService.loading$.subscribe(loading => {
        this.loading = loading;
      })
    );

    this.subscriptions.push(
      this.stateService.error$.subscribe(error => {
        this.error = error;
      })
    );

    this.loadProjects();
  }

  loadProjects(): void {
    this.stateService.setLoading(true);
    this.stateService.clearError();
    
    this.projectService.getProjects().subscribe({
      next: (projects) => {
        this.projects = projects;
        if (projects.length > 0 && !this.activeProject) {
          this.stateService.setActiveProject(projects[0]);
        }
        this.stateService.setLoading(false);
      },
      error: (error) => {
        console.error('Error loading projects:', error);
        this.stateService.setLoading(false);
        this.stateService.setError('Error al cargar los proyectos. Verifica que el backend esté corriendo.');
      }
    });
  }

  onProjectSelected(project: ProjectSimple): void {
    this.stateService.setActiveProject(project);
  }

  openActivityForm(): void {
    const dialogRef = this.dialog.open(ActivityFormComponent, {
      width: '500px',
      data: {
        activity: null,
        projectId: this.activeProject?.id,
        projects: this.projects
      }
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        // Recargar datos después de crear/editar
        this.loadProjects();
        // También recargar el proyecto activo
        if (this.activeProject) {
          this.stateService.setActiveProject(this.activeProject);
        }
      }
    });
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach(sub => sub.unsubscribe());
  }
}