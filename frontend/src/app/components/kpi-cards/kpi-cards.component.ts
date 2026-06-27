import { Component, Input, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Subscription } from 'rxjs';
import { ActivityService } from '../../core/services/activity.service';

@Component({
  selector: 'app-kpi-cards',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './kpi-cards.component.html',
  styleUrls: ['./kpi-cards.component.css']
})
export class KpiCardsComponent implements OnInit, OnDestroy {
  @Input() projectId!: number;

  totalBAC: number = 0;
  totalEV: number = 0;
  cpi: number = 0;
  spi: number = 0;
  eac: number = 0;
  vac: number = 0;
  costStatus: string = '';
  scheduleStatus: string = '';
  loading = true;
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
          this.totalBAC = 0;
          this.totalEV = 0;
          this.cpi = 0;
          this.spi = 0;
          this.loading = false;
          return;
        }

        // Calcular EVM consolidado
        const evm = this.calculateProjectEVM(activities);
        this.totalBAC = evm.totalBAC;
        this.totalEV = evm.totalEV;
        this.cpi = evm.cpi;
        this.spi = evm.spi;
        this.eac = evm.eac;
        this.vac = evm.vac;
        this.costStatus = evm.costStatus;
        this.scheduleStatus = evm.scheduleStatus;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
      }
    });
  }

  private calculateProjectEVM(activities: any[]): any {
    let totalBAC = 0;
    let totalPV = 0;
    let totalEV = 0;
    let totalAC = 0;

    activities.forEach(act => {
      const bac = Number(act.bac);
      const planned = Number(act.planned_progress);
      const actual = Number(act.actual_progress);
      const cost = Number(act.ac || act.actual_cost || 0);

      totalBAC += bac;
      totalPV += planned * bac;
      totalEV += actual * bac;
      totalAC += cost;
    });

    const cpi = totalAC > 0 ? totalEV / totalAC : 1;
    const spi = totalPV > 0 ? totalEV / totalPV : 1;
    const eac = cpi > 0 ? totalBAC / cpi : totalBAC;
    const vac = totalBAC - eac;

    const costStatus = cpi > 1 ? 'bajo presupuesto' : cpi < 1 ? 'sobre presupuesto' : 'en presupuesto';
    const scheduleStatus = spi > 1 ? 'adelantado' : spi < 1 ? 'atrasado' : 'en cronograma';

    return { totalBAC, totalEV, cpi, spi, eac, vac, costStatus, scheduleStatus };
  }

  getStatusClass(value: number, type: 'cpi' | 'spi'): string {
    if (type === 'cpi') {
      return value > 1 ? 'kpi-ok' : value < 1 ? 'kpi-bad' : '';
    }
    return value > 1 ? 'kpi-ok' : value < 1 ? 'kpi-bad' : '';
  }

  getEACLabel(): string {
    return this.cpi > 0 ? `EAC estimado $${this.eac.toLocaleString()}` : 'Sin datos';
  }

  getVACLabel(): string {
    return this.cpi > 0 ? `VAC $${this.vac.toLocaleString()}` : 'Sin datos';
  }

  ngOnDestroy(): void {
    this.subscription?.unsubscribe();
  }
}