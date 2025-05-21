import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CardComentariosComponent } from './card-comentarios.component';

describe('CardComentariosComponent', () => {
  let component: CardComentariosComponent;
  let fixture: ComponentFixture<CardComentariosComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CardComentariosComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CardComentariosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
