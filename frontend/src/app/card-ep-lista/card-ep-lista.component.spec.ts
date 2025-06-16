import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CardEpListaComponent } from './card-ep-lista.component';

describe('CardEpListaComponent', () => {
  let component: CardEpListaComponent;
  let fixture: ComponentFixture<CardEpListaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CardEpListaComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CardEpListaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
