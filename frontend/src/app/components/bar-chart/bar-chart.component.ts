import { Component, Input, OnInit, OnDestroy, OnChanges, SimpleChanges, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Subscription } from 'rxjs';
import { ActivityService } from '../../core/services/activity.service';

import {
  Chart,
  ChartConfiguration,
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  Legend,
  Tooltip
} from 'chart.js';

Chart.register(
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  Legend,
  Tooltip
);

@Component({
  selector: 'app-bar-chart',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './bar-chart.component.html',
  styleUrls: ['./bar-chart.component.css']
})
export class BarChartComponent implements OnInit, OnDestroy, OnChanges  {
  @Input() projectId!: number;
  @ViewChild('chartCanvas') chartCanvas!: ElementRef<HTMLCanvasElement>;

  chart: Chart | null = null;
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
        if (activities.length === 0) {
          this.loading = false;
          this.hasData = false;
          return;
        }

        this.hasData = true;
        this.loading = false;
        
        setTimeout(() => {
          this.renderChart(activities);
        }, 100);
      },
      error: () => {
        this.loading = false;
        this.hasData = false;
      }
    });
  }

  renderChart(activities: any[]): void {
    if (!this.chartCanvas) return;

    const ctx = this.chartCanvas.nativeElement.getContext('2d');
    if (!ctx) return;

    if (this.chart) {
      this.chart.destroy();
      this.chart = null;
    }

    const labels = activities.map(a => a.name);
    const pvData = activities.map(a => Number(a.planned_progress) * Number(a.bac));
    const evData = activities.map(a => Number(a.actual_progress) * Number(a.bac));
    const acData = activities.map(a => Number(a.ac || a.actual_cost || 0));

    const config: ChartConfiguration = {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'PV (Planificado)',
            data: pvData,
            backgroundColor: '#185FA5',
            borderRadius: 4
          },
          {
            label: 'EV (Completado)',
            data: evData,
            backgroundColor: '#0F6E56',
            borderRadius: 4
          },
          {
            label: 'AC (Gastado)',
            data: acData,
            backgroundColor: '#993C1D',
            borderRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: 'top',
            labels: {
              font: { size: 11 },
              boxWidth: 12,
              padding: 10
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              font: { size: 10 },
              callback: function(value) {
                return '$' + Number(value).toLocaleString();
              }
            }
          },
          x: {
            ticks: {
              font: { size: 10 },
              maxRotation: 30,
              minRotation: 20
            }
          }
        }
      }
    };

    this.chart = new Chart(ctx, config);
  }

  ngOnDestroy(): void {
    if (this.chart) {
      this.chart.destroy();
      this.chart = null;
    }
    this.subscription?.unsubscribe();
  }
  ngOnChanges(changes: SimpleChanges): void {
    if (changes['projectId'] && !changes['projectId'].firstChange) {
      this.loadData();
    }
  }
}