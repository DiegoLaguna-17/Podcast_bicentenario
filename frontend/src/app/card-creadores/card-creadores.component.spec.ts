import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CardCreadoresComponent } from './card-creadores.component';

describe('CardCreadoresComponent', () => {
  let component: CardCreadoresComponent;
  let fixture: ComponentFixture<CardCreadoresComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CardCreadoresComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CardCreadoresComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
