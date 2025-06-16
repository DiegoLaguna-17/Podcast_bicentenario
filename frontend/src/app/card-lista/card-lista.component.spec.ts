import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CardListaComponent } from './card-lista.component';

describe('CardListaComponent', () => {
  let component: CardListaComponent;
  let fixture: ComponentFixture<CardListaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CardListaComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CardListaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
