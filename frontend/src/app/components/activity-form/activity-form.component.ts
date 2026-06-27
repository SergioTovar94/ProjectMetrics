import { Component, Inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatSelectModule } from '@angular/material/select';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { ActivityService } from '../../core/services/activity.service';
import { Activity, ActivityCreate, ActivityUpdate } from '../../core/models/activity.model';
import { ProjectSimple } from '../../core/models/project.model';

@Component({
  selector: 'app-activity-form',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatSelectModule,
    MatSnackBarModule
  ],
  templateUrl: './activity-form.component.html',
  styleUrls: ['./activity-form.component.css']
})
export class ActivityFormComponent implements OnInit {
  activityForm!: FormGroup;
  isEditMode = false;
  submitting = false;
  projects: ProjectSimple[] = [];

  constructor(
    private fb: FormBuilder,
    private activityService: ActivityService,
    private snackBar: MatSnackBar,
    public dialogRef: MatDialogRef<ActivityFormComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { 
      activity?: Activity; 
      projectId?: number;
      projects?: ProjectSimple[];
    }
  ) {}

  ngOnInit(): void {
    this.isEditMode = !!this.data?.activity;
    this.projects = this.data?.projects || [];

    this.activityForm = this.fb.group({
      project_id: [this.data?.activity?.project_id || this.data?.projectId || '', Validators.required],
      name: [this.data?.activity?.name || '', [Validators.required, Validators.minLength(3)]],
      bac: [this.data?.activity?.bac || '', [Validators.required, Validators.min(0.01)]],
      planned_progress: [this.data?.activity?.planned_progress || 0, [Validators.required, Validators.min(0), Validators.max(1)]],
      actual_progress: [this.data?.activity?.actual_progress || 0, [Validators.required, Validators.min(0), Validators.max(1)]],
      ac: [this.data?.activity?.ac || this.data?.activity?.ac || 0, [Validators.required, Validators.min(0)]]
    });
  }

  onSubmit(): void {
    if (this.activityForm.invalid) {
      this.snackBar.open('Por favor, completa todos los campos correctamente', 'Cerrar', { duration: 3000 });
      return;
    }

    this.submitting = true;
    const formData = this.activityForm.value;

    if (this.isEditMode && this.data.activity) {
      // Actualizar actividad existente
      const updateData: ActivityUpdate = {
        name: formData.name,
        bac: formData.bac,
        planned_progress: formData.planned_progress,
        actual_progress: formData.actual_progress,
        ac: formData.ac
      };

      this.activityService.updateActivity(this.data.activity.id, updateData).subscribe({
        next: () => {
          this.snackBar.open('Actividad actualizada exitosamente', 'Cerrar', { duration: 3000 });
          this.dialogRef.close(true);
        },
        error: (error) => {
          console.error('Error updating activity:', error);
          this.snackBar.open('❌ Error al actualizar la actividad', 'Cerrar', { duration: 3000 });
          this.submitting = false;
        }
      });
    } else {
      // Crear nueva actividad
      const createData: ActivityCreate = {
        project_id: formData.project_id,
        name: formData.name,
        bac: formData.bac,
        planned_progress: formData.planned_progress,
        actual_progress: formData.actual_progress,
        ac: formData.ac
      };

      this.activityService.createActivity(createData).subscribe({
        next: () => {
          this.snackBar.open('Actividad creada exitosamente', 'Cerrar', { duration: 3000 });
          this.dialogRef.close(true);
        },
        error: (error) => {
          console.error('Error creating activity:', error);
          this.snackBar.open('❌ Error al crear la actividad', 'Cerrar', { duration: 3000 });
          this.submitting = false;
        }
      });
    }
  }

  onCancel(): void {
    this.dialogRef.close(false);
  }

  get title(): string {
    return this.isEditMode ? 'Editar Actividad' : 'Nueva Actividad';
  }

  get submitLabel(): string {
    return this.isEditMode ? 'Actualizar' : 'Crear';
  }
}