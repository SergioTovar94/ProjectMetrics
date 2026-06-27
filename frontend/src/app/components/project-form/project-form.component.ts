import { Component, Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { ProjectService } from '../../core/services/project.service';

@Component({
  selector: 'app-project-form',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatSnackBarModule
  ],
  templateUrl: './project-form.component.html',
  styleUrls: ['./project-form.component.css']
})
export class ProjectFormComponent {
  projectForm: FormGroup;
  submitting = false;

  constructor(
    private fb: FormBuilder,
    private projectService: ProjectService,
    private snackBar: MatSnackBar,
    public dialogRef: MatDialogRef<ProjectFormComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { project?: any }
  ) {
    this.projectForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(3)]],
      description: ['']
    });
  }

  onSubmit(): void {
    if (this.projectForm.invalid) {
      this.snackBar.open('Por favor, completa el nombre del proyecto', 'Cerrar', { duration: 3000 });
      return;
    }

    this.submitting = true;
    const formData = this.projectForm.value;

    this.projectService.createProject(formData).subscribe({
      next: () => {
        this.snackBar.open('✅ Proyecto creado exitosamente', 'Cerrar', { duration: 3000 });
        this.dialogRef.close(true);
      },
      error: (error) => {
        console.error('Error creating project:', error);
        this.snackBar.open('❌ Error al crear el proyecto', 'Cerrar', { duration: 3000 });
        this.submitting = false;
      }
    });
  }

  onCancel(): void {
    this.dialogRef.close(false);
  }
}