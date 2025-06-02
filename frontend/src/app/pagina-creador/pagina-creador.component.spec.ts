import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PaginaCreadorComponent } from './pagina-creador.component';

describe('PaginaCreadorComponent', () => {
  let component: PaginaCreadorComponent;
  let fixture: ComponentFixture<PaginaCreadorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PaginaCreadorComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PaginaCreadorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
