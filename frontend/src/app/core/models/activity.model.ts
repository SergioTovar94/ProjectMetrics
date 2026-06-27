import { EVMIndicators } from './evm.model';

export interface Activity {
  id: number;
  project_id: number;
  name: string;
  bac: number;
  planned_progress: number;
  actual_progress: number;
  ac: number;
  created_at: Date;
  updated_at?: Date;
  evm?: EVMIndicators;
}

export interface ActivityCreate {
  project_id: number;
  name: string;
  bac: number;
  planned_progress: number;
  actual_progress: number;
  ac: number;
}

export interface ActivityUpdate {
  name?: string;
  bac?: number;
  planned_progress?: number;
  actual_progress?: number;
  ac?: number;
}