import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProjectSelector } from './project-selector';

describe('ProjectSelector', () => {
  let component: ProjectSelector;
  let fixture: ComponentFixture<ProjectSelector>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ProjectSelector],
    }).compileComponents();

    fixture = TestBed.createComponent(ProjectSelector);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
