import { Component, Input, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Subscription } from 'rxjs';
import { ActivityService } from '../../core/services/activity.service';
import { Activity } from '../../core/models/activity.model';

@Component({
  selector: 'app-activity-table',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './activity-table.component.html',
  styleUrls: ['./activity-table.component.css']
})
export class ActivityTableComponent implements OnInit, OnDestroy {
  @Input() projectId!: number;

  activities: Activity[] = [];
  loading = true;
  hasData = false;
  private subscription?: Subscription;

  constructor(private activityService: ActivityService) {}

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