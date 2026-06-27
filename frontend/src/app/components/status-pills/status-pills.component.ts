import { Component, Input, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Subscription } from 'rxjs';
import { ActivityService } from '../../core/services/activity.service';
import { EVMIndicators } from '../../core/models/evm.model';

@Component({
  selector: 'app-status-pills',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './status-pills.component.html',
  styleUrls: ['./status-pills.component.css']
})
export class StatusPillsComponent implements OnInit, OnDestroy {
  @Input() projectId!: number;

  cpi: number | null = null;
  spi: number | null = null;
  cpiStatus: string = '';
  spiStatus: string = '';
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
          this.cpi = null;
          this.spi = null;
          this.cpiStatus = 'sin actividades';
          this.spiStatus = 'sin actividades';
          this.loading = false;
          return;
        }

        // Calcular EVM consolidado
        const evm = this.calculateProjectEVM(activities);
        this.cpi = evm.cpi;
        this.spi = evm.spi;
        this.cpiStatus = evm.cost_status;
        this.spiStatus = evm.schedule_status;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
      }
    });
  }

  private calculateProjectEVM(activities: any[]): EVMIndicators {
    let totalBAC = 0;
    let totalPV = 0;
    let totalEV = 0;
    let totalAC = 0;

    activities.forEach(act => {
      const bac = Number(act.bac);
      const planned = Number(act.planned_progress);
      const actual = Number(act.actual_progress);
      const cost = Number(act.actual_cost);

      totalBAC += bac;
      totalPV += planned * bac;
      totalEV += actual * bac;
      totalAC += cost;
    });

    const cv = totalEV - totalAC;
    const sv = totalEV - totalPV;
    const cpi = totalAC > 0 ? totalEV / totalAC : 1;
    const spi = totalPV > 0 ? totalEV / totalPV : 1;
    const eac = cpi > 0 ? totalBAC / cpi : totalBAC;
    const vac = totalBAC - eac;

    return {
      pv: totalPV,
      ev: totalEV,
      cv: cv,
      sv: sv,
      cpi: cpi,
      spi: spi,
      eac: eac,
      vac: vac,
      cost_status: this.interpretCPI(cpi),
      schedule_status: this.interpretSPI(spi)
    };
  }

  private interpretCPI(cpi: number): string {
    if (cpi > 1) return 'bajo presupuesto';
    if (cpi < 1) return 'sobre presupuesto';
    return 'en presupuesto';
  }

  private interpretSPI(spi: number): string {
    if (spi > 1) return 'adelantado';
    if (spi < 1) return 'atrasado';
    return 'en cronograma';
  }

  getPillClass(status: string): string {
    const map: Record<string, string> = {
      'bajo presupuesto': 'pill-green',
      'sobre presupuesto': 'pill-red',
      'en presupuesto': 'pill-amber',
      'adelantado': 'pill-green',
      'atrasado': 'pill-red',
      'en cronograma': 'pill-amber',
      'sin actividades': 'pill-neutral'
    };
    return map[status] || 'pill-neutral';
  }

  getCPIStatusText(): string {
    if (this.cpi === null) return 'sin datos';
    return `CPI ${this.cpi.toFixed(2)} — ${this.cpiStatus}`;
  }

  getSPIStatusText(): string {
    if (this.spi === null) return 'sin datos';
    return `SPI ${this.spi.toFixed(2)} — ${this.spiStatus}`;
  }

  getCPIEmoji(): string {
    if (this.cpiStatus === 'sobre presupuesto') return '📉';
    if (this.cpiStatus === 'bajo presupuesto') return '📈';
    if (this.cpiStatus === 'en presupuesto') return '➖';
    return '⏳';
  }

  getSPIEmoji(): string {
    if (this.spiStatus === 'atrasado') return '⏰';
    if (this.spiStatus === 'adelantado') return '⚡';
    if (this.spiStatus === 'en cronograma') return '✅';
    return '⏳';
  }

  ngOnDestroy(): void {
    this.subscription?.unsubscribe();
  }
}