export interface EVMIndicators {
  pv: number;           // Planned Value
  ev: number;           // Earned Value
  cv: number;           // Cost Variance
  sv: number;           // Schedule Variance
  cpi: number;          // Cost Performance Index
  spi: number;          // Schedule Performance Index
  eac: number;          // Estimate at Completion
  vac: number;          // Variance at Completion
  cost_status: string;  // "bajo presupuesto" | "sobre presupuesto" | "en presupuesto"
  schedule_status: string; // "adelantado" | "atrasado" | "en cronograma"
}