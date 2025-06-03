import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GestionCreadoresComponent } from './gestion-creadores.component';

describe('GestionCreadoresComponent', () => {
  let component: GestionCreadoresComponent;
  let fixture: ComponentFixture<GestionCreadoresComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GestionCreadoresComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GestionCreadoresComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
