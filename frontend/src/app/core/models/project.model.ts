import { Activity } from './activity.model';
import { EVMIndicators } from './evm.model';

export interface Project {
  id: number;
  name: string;
  description?: string;
  created_at: Date;
  activities?: Activity[];
  evm?: EVMIndicators;
}

export interface ProjectSimple {
  id: number;
  name: string;
  description?: string;
  created_at: Date;
}

export interface ProjectCreate {
  name: string;
  description?: string;
}

export interface ProjectUpdate {
  name?: string;
  description?: string;
}