import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListComentariosComponent } from './list-comentarios.component';

describe('ListComentariosComponent', () => {
  let component: ListComentariosComponent;
  let fixture: ComponentFixture<ListComentariosComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ListComentariosComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ListComentariosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
