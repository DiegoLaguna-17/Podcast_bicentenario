import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SubirPublicidadesComponent } from './subir-publicidades.component';

describe('SubirPublicidadesComponent', () => {
  let component: SubirPublicidadesComponent;
  let fixture: ComponentFixture<SubirPublicidadesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SubirPublicidadesComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SubirPublicidadesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
