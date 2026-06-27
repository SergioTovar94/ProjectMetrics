import { Component, Input, OnInit, OnDestroy, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Subscription } from 'rxjs';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { ActivityService } from '../../core/services/activity.service';
import { Activity } from '../../core/models/activity.model';
import { ActivityFormComponent } from '../activity-form/activity-form.component';

@Component({
  selector: 'app-activity-table',
  standalone: true,
  imports: [CommonModule, MatSnackBarModule],
  templateUrl: './activity-table.component.html',
  styleUrls: ['./activity-table.component.css']
})
export class ActivityTableComponent implements OnInit, OnDestroy {
  @Input() projectId!: number;
  @Output() dataChanged = new EventEmitter<void>();

  activities: Activity[] = [];
  loading = true;
  hasData = false;
  private subscription?: Subscription;

  constructor(
    private activityService: ActivityService,
    private dialog: MatDialog,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    if (this.projectId) {
      this.loadData();
    }
  }
  loadData(): void {
    this.loading = true;
    this.subscription = this.activityService.getActivitiesByProject(this.projectId).subscribe({
      next: (activities) => {
        this.activities = activities;
        this.hasData = activities.length > 0;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
        this.hasData = false;
      }
    });
  }
 editActivity(activity: Activity): void {
    const dialogRef = this.dialog.open(ActivityFormComponent, {
      width: '500px',
      data: {
        activity: activity,
        projectId: this.projectId,
        projects: []
      }
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this.loadData();
        this.dataChanged.emit();
      }
    });
  }

  deleteActivity(activity: Activity): void {
    if (confirm(`¿Estás seguro de eliminar la actividad "${activity.name}"?`)) {
      this.activityService.deleteActivity(activity.id).subscribe({
        next: () => {
          this.snackBar.open('✅ Actividad eliminada exitosamente', 'Cerrar', { duration: 3000 });
          this.loadData();
          this.dataChanged.emit();
        },
        error: (error) => {
          console.error('Error deleting activity:', error);
          this.snackBar.open('❌ Error al eliminar la actividad', 'Cerrar', { duration: 3000 });
        }
      });
    }
  }

  getStatusBadge(cpi: number, spi: number): string {
    if (cpi < 0.8 || spi < 0.8) return 'badge-red';
    if (cpi < 1 || spi < 1) return 'badge-amber';
    return 'badge-green';
  }

  getStatusText(cpi: number, spi: number): string {
    if (cpi < 0.8 || spi < 0.8) return 'crítico';
    if (cpi < 1 || spi < 1) return 'en riesgo';
    return 'al día';
  }

  formatCurrency(value: number): string {
    if (value === 0) return '$0';
    return '$' + value.toLocaleString();
  }

  formatNumber(value: number): string {
    if (value === 0) return '—';
    return value.toFixed(2);
  }

  getCVClass(value: number): string {
    if (value > 0) return 'text-success';
    if (value < 0) return 'text-danger';
    return 'text-muted';
  }

  getSVClass(value: number): string {
    if (value > 0) return 'text-success';
    if (value < 0) return 'text-danger';
    return 'text-muted';
  }

  getCPIClass(value: number): string {
    if (value > 1) return 'text-success';
    if (value < 1) return 'text-danger';
    return 'text-muted';
  }

  getSPIClass(value: number): string {
    if (value > 1) return 'text-success';
    if (value < 1) return 'text-danger';
    return 'text-muted';
  }

  getStatusClass(cpi: number, spi: number): string {
    if (cpi < 0.8 || spi < 0.8) return 'badge-red';
    if (cpi < 1 || spi < 1) return 'badge-amber';
    return 'badge-green';
  }

  ngOnDestroy(): void {
    this.subscription?.unsubscribe();
  }
}