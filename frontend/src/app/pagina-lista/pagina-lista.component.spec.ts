import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PaginaListaComponent } from './pagina-lista.component';

describe('PaginaListaComponent', () => {
  let component: PaginaListaComponent;
  let fixture: ComponentFixture<PaginaListaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PaginaListaComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PaginaListaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
